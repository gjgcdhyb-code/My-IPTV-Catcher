import requests
import re
import os
import asyncio

# --- الإعدادات والمصادر ---
LIVE_SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u"
]

VOD_SOURCES = [
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

# قائمة بمعرفات قنوات تليجرام القوية (ضع اليوزرنيم بدون @)
TG_CHANNELS = ['Bein_Live_Links', 'IPTV_Arabic_Free', 'Sport_Links_M3U']

def check_link(url):
    try:
        r = requests.head(url, timeout=3)
        return r.status_code == 200
    except:
        return False

def main():
    final_list = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    seen_links = set()

    print("Starting the hunt...")

    # 1. صيد الروابط من GitHub (Live + VOD)
    all_sources = LIVE_SOURCES + VOD_SOURCES
    for src in all_sources:
        try:
            r = requests.get(src, timeout=20)
            if r.status_code == 200:
                matches = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                for info, link in matches:
                    link = link.strip()
                    if link not in seen_links:
                        # تنظيم الجروبات (Sport, Movies, etc.)
                        if "bein" in info.lower() or "ssc" in info.lower():
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"SPORTS LIVE\"")
                        elif "movie" in info.lower() or "فيلم" in info:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"MOVIES VOD\"")
                        elif "series" in info.lower() or "مسلسل" in info:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"SERIES VOD\"")
                        else:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"GENERAL ARABIC\"")
                        
                        final_list += f"{info}\n{link}\n"
                        seen_links.add(link)
        except: continue

    # 2. حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    
    print(f"Done! Captured {len(seen_links)} links.")

if __name__ == "__main__":
    main()
