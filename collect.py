import requests
import re

# مصادر ضخمة ومفتوحة
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u"
]

def main():
    final_data = '#EXTM3U x-tvg-url="http://epg.itv.re/epg.xml.gz"\n'
    added_links = set()
    
    print("🚀 جاري صيد القنوات والأفلام...")
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # ريجيكس متطور لصيد الاسم والرابط معاً
                matches = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                for info, link in matches:
                    link = link.strip()
                    if link not in added_links:
                        # تصنيف ذكي للمجلدات
                        info_lower = info.lower()
                        if "bein" in info_lower or "sport" in info_lower:
                            info = info.replace("#EXTINF:-1", '#EXTINF:-1 group-title="⚽ SPORTS"')
                        elif "movie" in info_lower or "فيلم" in info_lower:
                            info = info.replace("#EXTINF:-1", '#EXTINF:-1 group-title="🎬 MOVIES"')
                        
                        final_data += f"{info}\n{link}\n"
                        added_links.add(link)
        except: continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print(f"✅ تم جمع {len(added_links)} رابط.")

if __name__ == "__main__":
    main()
