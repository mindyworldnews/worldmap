"""
storage.py
把圖片上傳到 Catbox.moe，回傳永久圖片 URL。
不需要帳號或 API key。
"""
import requests

CATBOX_URL = "https://catbox.moe/user/api.php"


def upload(image_bytes: bytes, title: str = "") -> str:
    """
    上傳圖片到 Catbox.moe，回傳圖片直連 URL（https://files.catbox.moe/xxxxx.png）。
    """
    resp = requests.post(
        CATBOX_URL,
        data={"reqtype": "fileupload", "userhash": ""},
        files={"fileToUpload": ("map.png", image_bytes, "image/png")},
        timeout=30,
    )
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"Catbox 上傳失敗：{url}")
    return url
