import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np

# Use a CJK-compatible font
plt.rcParams['font.family'] = 'Noto Sans TC'

# Load world data
world = gpd.read_file('r:/我的雲端硬碟/ClaudeWorkspace/tools/world-map/data/world_110m.geojson')

# Countries to highlight: USA, China, Taiwan
highlight = {
    'USA': {'color': '#E85D5D', 'label': '美國'},
    'CHN': {'color': '#5DA8E8', 'label': '中國'},
    'TWN': {'color': '#5DE88A', 'label': '台灣'},
}

# Small countries threshold (area in square degrees)
SMALL_COUNTRY_THRESHOLD = 5.0

# Color palette
BACKGROUND = '#1a1a2e'
BASE_COLOR = '#2d3561'
BORDER_COLOR = '#3d4f8a'
OCEAN_COLOR = '#0f1429'

fig, ax = plt.subplots(1, 1, figsize=(16, 9), facecolor=BACKGROUND)
ax.set_facecolor(OCEAN_COLOR)

# Draw all base countries
world.plot(
    ax=ax,
    color=BASE_COLOR,
    edgecolor=BORDER_COLOR,
    linewidth=0.4,
    zorder=1
)

# Draw highlighted countries
small_countries = []

for iso, info in highlight.items():
    country = world[world['ISO_A3'] == iso]
    if country.empty:
        # Try ADM0_A3
        country = world[world['ADM0_A3'] == iso]

    if country.empty:
        print(f"Warning: {iso} not found")
        continue

    # Check if country is small
    area = country.geometry.area.sum()
    print(f"{iso}: area = {area:.4f}")

    if area < SMALL_COUNTRY_THRESHOLD:
        small_countries.append((iso, info, country))
    else:
        country.plot(
            ax=ax,
            color=info['color'],
            edgecolor='white',
            linewidth=0.8,
            alpha=0.9,
            zorder=2
        )

# Handle small countries with pin markers
for iso, info, country in small_countries:
    centroid = country.geometry.centroid.iloc[0]
    ax.plot(centroid.x, centroid.y, 'o',
            color=info['color'],
            markersize=10,
            markeredgecolor='white',
            markeredgewidth=1.5,
            zorder=5)
    ax.annotate(info['label'],
                xy=(centroid.x, centroid.y),
                xytext=(8, 8),
                textcoords='offset points',
                color='white',
                fontsize=8,
                fontweight='bold',
                zorder=6)

# Legend
legend_patches = []
for iso, info in highlight.items():
    country = world[world['ISO_A3'] == iso]
    if country.empty:
        country = world[world['ADM0_A3'] == iso]
    area = country.geometry.area.sum() if not country.empty else 0

    if area < SMALL_COUNTRY_THRESHOLD:
        patch = mpatches.Patch(color=info['color'], label=f"● {info['label']}")
    else:
        patch = mpatches.Patch(color=info['color'], label=info['label'])
    legend_patches.append(patch)

legend = ax.legend(
    handles=legend_patches,
    loc='lower left',
    framealpha=0.3,
    facecolor='#1a1a2e',
    edgecolor='#3d4f8a',
    labelcolor='white',
    fontsize=11,
    title_fontsize=12,
)

# Title area
ax.set_title('世界地圖 · 國家標註', color='white', fontsize=16, pad=12,
             fontweight='bold', loc='left')

# Remove axes
ax.set_axis_off()

# Tight layout
plt.tight_layout(pad=0.5)
plt.savefig('r:/我的雲端硬碟/ClaudeWorkspace/tools/world-map/preview_USA_CHN_TWN.png',
            dpi=150, bbox_inches='tight',
            facecolor=BACKGROUND)
print("Saved preview!")
plt.close()
