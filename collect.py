import requests
from bs4 import BeautifulSoup
import re

# مصادر قنوات البث المباشر (Live)
LIVE_SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u"
]

# مصادر مكتبات الأفلام والمسلسلات (VOD)
VOD_SOURCES = [
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def clean_name(name):
    # وظيفة لتنظيف الأسماء وترتيبها
    return name.strip().replace('"', '')

def main():
    final_list = "#EXTM3U\n"
    
    # 1. صيد القنوات المباشرة
    for src in LIVE_SOURCES:
        try:
            r = requests.get(src, timeout=15)
            matches = re.findall(r'(#EXTINF.*)\n(http.*)', r.text)
            for info, link in matches:
                # تصنيف الرياضة
                if "bein" in info.lower() or "ssc" in info.lower() or "sport" in info.lower():
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="LIVE SPORTS"")
                else:
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="ARABIC CHANNELS"")
                final_list += f"{info}\n{link.strip()}\n"
        except: continue

    # 2. صيد مكتبة الأفلام والمسلسلات
    for src in VOD_SOURCES:
        try:
            r = requests.get(src, timeout=20)
            matches = re.findall(r'(#EXTINF.*)\n(http.*)', r.text)
            for info, link in matches:
                if "movie" in info.lower() or "فيلم" in info:
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="MOVIES LIBRARY"")
                elif "series" in info.lower() or "مسلسل" in info:
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="SERIES LIBRARY"")
                final_list += f"{info}\n{link.strip()}\n"
        except: continue

    # حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print("Successfully updated the playlist!")

if __name__ == "__main__":
    main()
