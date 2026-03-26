import requests
import re
import os

# مصادر ثابتة وموثوقة
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def main():
    final_list = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    seen_links = set()

    print("Hunting for Links...")
    for src in SOURCES:
        try:
            r = requests.get(src, timeout=15)
            if r.status_code == 200:
                matches = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                for info, link in matches:
                    link = link.strip()
                    if link not in seen_links:
                        # تنظيم المجموعات تلقائياً
                        if any(x in info.lower() for x in ["bein", "ssc", "sport"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"SPORTS LIVE\"")
                        elif any(x in info.lower() for x in ["movie", "فيلم", "film"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"MOVIES VOD\"")
                        elif any(x in info.lower() for x in ["series", "مسلسل"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"SERIES VOD\"")
                        else:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"ARABIC TV\"")
                        
                        final_list += f"{info}\n{link}\n"
                        seen_links.add(link)
        except: continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"Success! Found {len(seen_links)} items.")

if __name__ == "__main__":
    main()
