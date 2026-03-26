import requests
import re
import time
from bs4 import BeautifulSoup

# 1. قائمة المصادر الثابتة (العملاقة)
STATIC_SOURCES = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

# 2. وظيفة البحث التلقائي عن روابط جديدة (Google Dorking Simulation)
def search_new_sources():
    new_links = []
    # محاكاة البحث عن روابط m3u8 منشورة حديثاً في مواقع برمجية
    search_urls = [
        "https://github.com/search?q=iptv+arabic+m3u8&type=code&s=indexed&o=desc",
        "https://www.google.com/search?q=filetype:m3u+arabic+2026"
    ]
    # ملاحظة: جيت هاب يمنع الكشط المباشر أحياناً، لذا سنعتمد على روابط الـ Raw المشهورة
    return new_links

def is_working(url):
    """فحص الرابط: هل هو حي (Alive) أم ميت؟"""
    try:
        # نطلب فقط رأس الملف (Header) لسرعة الفحص
        r = requests.head(url, timeout=3, allow_redirects=True)
        return r.status_code == 200
    except:
        return False

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print("🚀 انطلاق الرادار العالمي للصيد...")

    # جمع كل المصادر
    all_sources = STATIC_SOURCES + search_new_sources()

    for src in all_sources:
        try:
            print(f"🔎 فحص المصدر: {src}")
            response = requests.get(src, timeout=15, headers=headers)
            
            # البحث عن أي رابط بث (m3u8, mp4, ts)
            pattern = r'(?:#EXTINF:.*,(.*)\n|([^>\n]+)\s*<a[^>]+href=")?(https?://[^\s<>"]+\.(?:m3u8|mp4|mkv|ts)[^\s<>"]*)'
            matches = re.findall(pattern, response.text)

            for m3u_name, tg_name, link in matches:
                link = link.strip()
                if link not in seen_links:
                    # --- الفحص الجوهري (شغال لو لا؟) ---
                    if is_working(link):
                        name = m3u_name if m3u_name else tg_name
                        name = re.sub(r'[^\w\s]', '', str(name)) if name else "Fast Stream"
                        
                        # تصنيف ذكي
                        if ".mp4" in link or ".mkv" in link: group = "MOVIES/SERIES"
                        elif "sport" in name.lower() or "bein" in name.lower(): group = "LIVE SPORTS"
                        else: group = "CHANNELS"

                        final_list += f'#EXTINF:-1 group-title="{group}", {name}\n{link}\n'
                        seen_links.add(link)
                        print(f"✅ تم صيد رابط شغال: {name}")
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"🏁 المهمة تمت! المجموع: {len(seen_links)} رابط مفحوص وشغال 100%.")

if __name__ == "__main__":
    main()
