import requests
import re

# مصادر عالمية ضخمة (Live + VOD)
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u", # قنوات لايف
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u", # أفلام ومسلسلات
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u", # تحديث يومي رياضي
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u" # مكتبة متنوعة
]

def clean_info(info):
    # وظيفة لتنظيم التصنيفات لكي تظهر في التطبيق بشكل مرتب (Folders)
    if "bein" in info.lower() or "ssc" in info.lower():
        return info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="SPORTS"")
    elif "film" in info.lower() or "movie" in info.lower() or "فيلم" in info:
        return info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="MOVIES"")
    elif "series" in info.lower() or "مسلسل" in info:
        return info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="SERIES"")
    else:
        return info.replace("#EXTINF:-1", "#EXTINF:-1 group-title="ARABIC TV"")

def main():
    final_list = "#EXTM3U x-tvg-url="http://epg.itv.re/epg.xml.gz"\n"
    seen_links = set()

    for src in SOURCES:
        try:
            # زيادة وقت الانتظار لأن المصادر ضخمة
            response = requests.get(src, timeout=30)
            if response.status_code == 200:
                matches = re.findall(r'(#EXTINF.*)\n(http.*)', response.text)
                for info, link in matches:
                    link = link.strip()
                    if link not in seen_links:
                        organized_info = clean_info(info)
                        final_list += f"{organized_info}\n{link}\n"
                        seen_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)

if __name__ == "__main__":
    main()
