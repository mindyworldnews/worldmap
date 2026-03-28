"""
country_resolver.py
把使用者輸入的國家名稱（中文/英文/縮寫）解析成群組結構。
每個群組有 label（顯示名稱）和 isos（成員 ISO 代碼清單）。
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'data', 'groups.json'), encoding='utf-8') as f:
    GROUPS = json.load(f)

COUNTRY_MAP = {
    # 中文
    "美國": "USA", "中國": "CHN", "台灣": "TWN", "日本": "JPN",
    "韓國": "KOR", "南韓": "KOR", "北韓": "PRK", "俄羅斯": "RUS",
    "英國": "GBR", "法國": "FRA", "德國": "DEU", "義大利": "ITA",
    "西班牙": "ESP", "葡萄牙": "PRT", "荷蘭": "NLD", "比利時": "BEL",
    "瑞士": "CHE", "奧地利": "AUT", "瑞典": "SWE", "挪威": "NOR",
    "丹麥": "DNK", "芬蘭": "FIN", "冰島": "ISL", "愛爾蘭": "IRL",
    "波蘭": "POL", "捷克": "CZE", "匈牙利": "HUN", "羅馬尼亞": "ROU",
    "保加利亞": "BGR", "希臘": "GRC", "土耳其": "TUR", "烏克蘭": "UKR",
    "白俄羅斯": "BLR", "立陶宛": "LTU", "拉脫維亞": "LVA", "愛沙尼亞": "EST",
    "斯洛伐克": "SVK", "斯洛維尼亞": "SVN", "克羅埃西亞": "HRV",
    "塞爾維亞": "SRB", "阿爾巴尼亞": "ALB", "北馬其頓": "MKD",
    "蒙特內哥羅": "MNE", "盧森堡": "LUX", "塞普勒斯": "CYP", "馬爾他": "MLT",
    "加拿大": "CAN", "墨西哥": "MEX", "巴西": "BRA", "阿根廷": "ARG",
    "智利": "CHL", "秘魯": "PER", "哥倫比亞": "COL", "委內瑞拉": "VEN",
    "古巴": "CUB", "澳洲": "AUS", "紐西蘭": "NZL", "印度": "IND",
    "巴基斯坦": "PAK", "孟加拉": "BGD", "斯里蘭卡": "LKA",
    "阿富汗": "AFG", "伊朗": "IRN", "伊拉克": "IRQ", "敘利亞": "SYR",
    "以色列": "ISR", "巴勒斯坦": "PSE", "黎巴嫩": "LBN", "約旦": "JOR",
    "沙烏地阿拉伯": "SAU", "阿聯酋": "ARE", "卡達": "QAT", "科威特": "KWT",
    "巴林": "BHR", "阿曼": "OMN", "葉門": "YEM", "土庫曼": "TKM",
    "哈薩克": "KAZ", "烏茲別克": "UZB", "吉爾吉斯": "KGZ",
    "塔吉克": "TJK", "亞塞拜然": "AZE", "亞美尼亞": "ARM", "喬治亞": "GEO",
    "印尼": "IDN", "越南": "VNM", "泰國": "THA", "菲律賓": "PHL",
    "馬來西亞": "MYS", "新加坡": "SGP", "緬甸": "MMR", "柬埔寨": "KHM",
    "寮國": "LAO", "汶萊": "BRN", "蒙古": "MNG", "尼泊爾": "NPL",
    "埃及": "EGY", "利比亞": "LBY", "突尼西亞": "TUN", "摩洛哥": "MAR",
    "阿爾及利亞": "DZA", "蘇丹": "SDN", "衣索比亞": "ETH", "索馬利亞": "SOM",
    "肯亞": "KEN", "坦尚尼亞": "TZA", "南非": "ZAF", "奈及利亞": "NGA",
    "剛果": "COD", "安哥拉": "AGO", "莫三比克": "MOZ", "辛巴威": "ZWE",
    "迦納": "GHA", "盧安達": "RWA", "烏干達": "UGA",
    # 英文全名
    "United States": "USA", "United States of America": "USA",
    "China": "CHN", "People's Republic of China": "CHN",
    "Taiwan": "TWN", "Japan": "JPN", "South Korea": "KOR",
    "North Korea": "PRK", "Russia": "RUS", "United Kingdom": "GBR",
    "France": "FRA", "Germany": "DEU", "Italy": "ITA", "Spain": "ESP",
    "Portugal": "PRT", "Netherlands": "NLD", "Belgium": "BEL",
    "Switzerland": "CHE", "Austria": "AUT", "Sweden": "SWE",
    "Norway": "NOR", "Denmark": "DNK", "Finland": "FIN", "Iceland": "ISL",
    "Ireland": "IRL", "Poland": "POL", "Czech Republic": "CZE",
    "Czechia": "CZE", "Hungary": "HUN", "Romania": "ROU",
    "Bulgaria": "BGR", "Greece": "GRC", "Turkey": "TUR", "Ukraine": "UKR",
    "Canada": "CAN", "Mexico": "MEX", "Brazil": "BRA", "Argentina": "ARG",
    "Australia": "AUS", "New Zealand": "NZL", "India": "IND",
    "Pakistan": "PAK", "Iran": "IRN", "Iraq": "IRQ", "Syria": "SYR",
    "Israel": "ISR", "Palestine": "PSE", "Saudi Arabia": "SAU",
    "UAE": "ARE", "United Arab Emirates": "ARE", "Qatar": "QAT",
    "Indonesia": "IDN", "Vietnam": "VNM", "Thailand": "THA",
    "Philippines": "PHL", "Malaysia": "MYS", "Singapore": "SGP",
    "Myanmar": "MMR", "Cambodia": "KHM", "Egypt": "EGY",
    "South Africa": "ZAF", "Nigeria": "NGA", "Ethiopia": "ETH",
    # 常見縮寫
    "US": "USA", "UK": "GBR", "PRC": "CHN", "ROC": "TWN",
    "ROK": "KOR", "DPRK": "PRK",
}

COUNTRY_ZH = {
    "USA":"美國","CHN":"中國","TWN":"台灣","JPN":"日本","KOR":"韓國",
    "PRK":"北韓","RUS":"俄羅斯","GBR":"英國","FRA":"法國","DEU":"德國",
    "ITA":"義大利","ESP":"西班牙","PRT":"葡萄牙","NLD":"荷蘭","BEL":"比利時",
    "CHE":"瑞士","AUT":"奧地利","SWE":"瑞典","NOR":"挪威","DNK":"丹麥",
    "FIN":"芬蘭","ISL":"冰島","IRL":"愛爾蘭","POL":"波蘭","CZE":"捷克",
    "HUN":"匈牙利","ROU":"羅馬尼亞","BGR":"保加利亞","GRC":"希臘",
    "TUR":"土耳其","UKR":"烏克蘭","BLR":"白俄羅斯","LTU":"立陶宛",
    "LVA":"拉脫維亞","EST":"愛沙尼亞","SVK":"斯洛伐克","SVN":"斯洛維尼亞",
    "HRV":"克羅埃西亞","SRB":"塞爾維亞","ALB":"阿爾巴尼亞","MKD":"北馬其頓",
    "MNE":"蒙特內哥羅","LUX":"盧森堡","CYP":"塞普勒斯","MLT":"馬爾他",
    "CAN":"加拿大","MEX":"墨西哥","BRA":"巴西","ARG":"阿根廷","CHL":"智利",
    "PER":"秘魯","COL":"哥倫比亞","VEN":"委內瑞拉","CUB":"古巴",
    "AUS":"澳洲","NZL":"紐西蘭","IND":"印度","PAK":"巴基斯坦",
    "BGD":"孟加拉","AFG":"阿富汗","IRN":"伊朗","IRQ":"伊拉克","SYR":"敘利亞",
    "ISR":"以色列","PSE":"巴勒斯坦","LBN":"黎巴嫩","JOR":"約旦",
    "SAU":"沙烏地阿拉伯","ARE":"阿聯酋","QAT":"卡達","KWT":"科威特",
    "BHR":"巴林","OMN":"阿曼","YEM":"葉門","KAZ":"哈薩克","UZB":"烏茲別克",
    "KGZ":"吉爾吉斯","TJK":"塔吉克","TKM":"土庫曼","AZE":"亞塞拜然",
    "ARM":"亞美尼亞","GEO":"喬治亞","IDN":"印尼","VNM":"越南","THA":"泰國",
    "PHL":"菲律賓","MYS":"馬來西亞","SGP":"新加坡","MMR":"緬甸",
    "KHM":"柬埔寨","LAO":"寮國","BRN":"汶萊","MNG":"蒙古","NPL":"尼泊爾",
    "EGY":"埃及","LBY":"利比亞","TUN":"突尼西亞","MAR":"摩洛哥",
    "DZA":"阿爾及利亞","SDN":"蘇丹","ETH":"衣索比亞","SOM":"索馬利亞",
    "KEN":"肯亞","TZA":"坦尚尼亞","ZAF":"南非","NGA":"奈及利亞",
    "COD":"剛果","AGO":"安哥拉","MOZ":"莫三比克","ZWE":"辛巴威",
    "GHA":"迦納","RWA":"盧安達","UGA":"烏干達","PNG":"巴布亞紐幾內亞",
    "HKG":"香港",
}


def build_group_lookup():
    lookup = {}
    for key, info in GROUPS.items():
        lookup[key.upper()] = key
        for name in info.get('zh', []):
            lookup[name] = key
        for name in info.get('en', []):
            lookup[name.upper()] = key
    return lookup

GROUP_LOOKUP = build_group_lookup()


def _token_to_iso(token: str) -> str | None:
    """單一 token 轉 ISO，非群組。回傳 None 表示找不到。"""
    iso = COUNTRY_MAP.get(token) or COUNTRY_MAP.get(token.title())
    if iso:
        return iso
    upper = token.upper()
    if len(upper) == 3 and upper.isalpha():
        return upper
    token_lower = token.lower()
    return next(
        (v for k, v in COUNTRY_MAP.items() if k.lower() == token_lower),
        None
    )


def resolve_groups(raw_input: str) -> list[dict]:
    """
    解析輸入，回傳群組清單。每個群組是：
      {"label": "北約", "isos": ["ALB", "BEL", ...]}

    群組（NATO/EU 等）→ 一個 entry，label 為組織中文名
    個別國家 → 每個國家一個 entry，label 為國家中文名

    已被前面群組佔用的 ISO 不會重複出現在後面的群組中。
    """
    tokens = [t.strip() for t in raw_input.replace('，', ',').split(',') if t.strip()]
    groups = []
    claimed = set()  # 已被分配的 ISO

    for token in tokens:
        group_key = GROUP_LOOKUP.get(token.upper()) or GROUP_LOOKUP.get(token)
        if group_key:
            info = GROUPS[group_key]
            label = info['zh'][0] if info.get('zh') else group_key
            isos = [iso for iso in info['members'] if iso not in claimed]
            claimed.update(isos)
            groups.append({"label": label, "isos": isos})
            continue

        iso = _token_to_iso(token)
        if iso:
            if iso not in claimed:
                label = COUNTRY_ZH.get(iso, iso)
                claimed.add(iso)
                groups.append({"label": label, "isos": [iso]})
        else:
            print(f"[Warning] 找不到國家：{token!r}")

    return groups


def cache_key(groups: list[dict]) -> str:
    """快取鍵：群組 label 排序後 join（順序無關）"""
    labels = sorted(g["label"] for g in groups)
    return "|".join(labels)


if __name__ == "__main__":
    for test in ["美國, 中國, 台灣", "NATO", "北約, 中國, 俄羅斯"]:
        groups = resolve_groups(test)
        print(f"輸入：{test}")
        for g in groups:
            print(f"  {g['label']}：{len(g['isos'])} 國")
        print(f"  快取鍵：{cache_key(groups)}\n")
