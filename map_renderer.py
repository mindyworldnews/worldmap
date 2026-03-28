"""
map_renderer.py
接收群組清單，生成世界地圖圖片，回傳 PNG bytes。
"""
import io
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEOJSON_PATH = os.path.join(BASE_DIR, 'data', 'world_110m.geojson')

_world = None

def get_world():
    global _world
    if _world is None:
        _world = gpd.read_file(GEOJSON_PATH)
    return _world

STYLE = {
    'fig_bg':       '#1a1a2e',
    'ocean':        '#0f1429',
    'base_country': '#2d3561',
    'border':       '#3d4f8a',
    'border_width': 0.4,
    'highlight_border': 'white',
    'highlight_border_width': 0.8,
    'highlight_alpha': 0.92,
    'font_family':  'Noto Sans TC',
    'fig_size':     (16, 9),
    'dpi':          150,
}

SMALL_THRESHOLD = 0.05  # 單位：百萬 km²（約 50,000 km²，小於此值用圓點）

PALETTE = [
    '#E85D5D',  # 紅
    '#5DA8E8',  # 藍
    '#5DE88A',  # 綠
    '#F0C060',  # 黃
    '#C87BE8',  # 紫
    '#E8975D',  # 橘
    '#5DE8D8',  # 青
    '#E85DB0',  # 粉
    '#A8E85D',  # 黃綠
    '#5D8AE8',  # 靛
]


def render(groups: list[dict]) -> bytes:
    """
    groups: [{"label": "北約", "isos": ["ALB", ...]}, ...]
    回傳 PNG bytes。
    """
    plt.rcParams['font.family'] = STYLE['font_family']
    world = get_world()

    fig, ax = plt.subplots(1, 1, figsize=STYLE['fig_size'], facecolor=STYLE['fig_bg'])
    ax.set_facecolor(STYLE['ocean'])

    world.plot(ax=ax, color=STYLE['base_country'],
               edgecolor=STYLE['border'], linewidth=STYLE['border_width'], zorder=1)

    small_pins = []   # (color, label, centroid_x, centroid_y) — 只有群組唯一成員才標文字
    legend_patches = []

    for i, group in enumerate(groups):
        color = PALETTE[i % len(PALETTE)]
        label = group['label']
        isos = group['isos']
        is_group = len(isos) > 1  # 多個國家的群組不顯示小國標籤

        for iso in isos:
            country = world[world['ISO_A3'] == iso]
            if country.empty:
                country = world[world['ADM0_A3'] == iso]
            if country.empty:
                continue

            area = country.to_crs(epsg=6933).geometry.area.sum() / 1e12  # 百萬 km²

            if area < SMALL_THRESHOLD:
                centroid = country.geometry.centroid.iloc[0]
                # 群組模式下小國只顯示圓點，不顯示文字標籤
                show_label = not is_group
                small_pins.append((color, label if show_label else None,
                                   centroid.x, centroid.y))
            else:
                country.plot(ax=ax, color=color,
                             edgecolor=STYLE['highlight_border'],
                             linewidth=STYLE['highlight_border_width'],
                             alpha=STYLE['highlight_alpha'], zorder=2)

        legend_patches.append(mpatches.Patch(color=color, label=label))

    # 繪製小國圓點
    for color, pin_label, cx, cy in small_pins:
        ax.plot(cx, cy, 'o', color=color, markersize=9,
                markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        if pin_label:
            ax.annotate(pin_label, xy=(cx, cy), xytext=(9, 6),
                        textcoords='offset points', color='white',
                        fontsize=8, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=color,
                                  alpha=0.7, edgecolor='none'),
                        zorder=6)

    # 圖例
    if legend_patches:
        legend = ax.legend(
            handles=legend_patches,
            loc='lower left',
            framealpha=0.5,
            facecolor='#1a1a2e',
            edgecolor='#3d4f8a',
            labelcolor='white',
            fontsize=18,
            handlelength=2.2,
            handleheight=1.6,
            borderpad=1.0,
            labelspacing=0.7,
        )
        for text in legend.get_texts():
            text.set_fontweight('bold')

    ax.set_axis_off()
    plt.tight_layout(pad=0.3)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=STYLE['dpi'],
                bbox_inches='tight', facecolor=STYLE['fig_bg'])
    plt.close(fig)
    buf.seek(0)
    return buf.read()


if __name__ == "__main__":
    from country_resolver import resolve_groups
    for test in ["北約, 中國, 俄羅斯", "美國, 日本, 台灣"]:
        groups = resolve_groups(test)
        img = render(groups)
        fname = test.replace(', ', '_').replace(',', '_') + '.png'
        with open(fname, 'wb') as f:
            f.write(img)
        print(f"Saved {fname} ({len(img)//1024} KB)")
