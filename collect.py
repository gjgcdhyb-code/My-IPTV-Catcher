import requests
import re

# مصادر بحث عالمية ضخمة
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def main():
    final_data = "#EXTM3U\n"
    links_found = set()
    
    print("🔍 Searching the web for links...")
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # صيد الروابط باستخدام Regex
                matches = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                for info, link in matches:
                    if link.strip() not in links_found:
                        # تصنيف ذكي
                        if "bein" in info.lower() or "sport" in info.lower():
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"⚽ SPORTS\"")
                        elif "movie" in info.lower() or "فيلم" in info:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🎬 MOVIES\"")
                        
                        final_data += f"{info}\n{link.strip()}\n"
                        links_found.add(link.strip())
        except: continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print(f"✅ Success! Captured {len(links_found)} links.")

if __name__ == "__main__":
    main()
