"""
app.py - Flask 後端
"""
import json
import os
from flask import Flask, request, jsonify, render_template, send_from_directory

from country_resolver import resolve_groups, cache_key
from map_renderer import render as render_map
from storage import upload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, 'cache.json')

app = Flask(__name__, template_folder='templates')


def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    raw = data.get('countries', '').strip()
    if not raw:
        return jsonify({"error": "請輸入國家名稱"}), 400

    # 解析國家（群組結構）
    groups = resolve_groups(raw)
    if not groups:
        return jsonify({"error": "找不到任何有效的國家名稱，請確認輸入"}), 400

    key = cache_key(groups)

    # 查快取
    cache = load_cache()
    if key in cache:
        all_isos = [iso for g in groups for iso in g['isos']]
        return jsonify({
            "url": cache[key],
            "countries": all_isos,
            "labels": [g['label'] for g in groups],
            "cached": True
        })

    # 生成地圖
    try:
        img_bytes = render_map(groups)
    except Exception as e:
        return jsonify({"error": f"地圖生成失敗：{e}"}), 500

    # 上傳
    try:
        labels = ', '.join(g['label'] for g in groups)
        url = upload(img_bytes, title=f"World Map: {labels}")
    except Exception as e:
        return jsonify({"error": f"上傳失敗：{e}"}), 500

    # 存快取
    cache[key] = url
    save_cache(cache)

    all_isos = [iso for g in groups for iso in g['isos']]
    return jsonify({
        "url": url,
        "countries": all_isos,
        "labels": [g['label'] for g in groups],
        "cached": False
    })


@app.route('/cache', methods=['GET'])
def list_cache():
    cache = load_cache()
    return jsonify(cache)


if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'templates'), exist_ok=True)
    app.run(debug=True, port=5050)
