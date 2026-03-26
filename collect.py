import requests
import re

# المصادر العالمية - هذي المصادر "تفلتر" الروابط وتخلي بس الشغال
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u", # أفلام ومسلسلات عربية مباشرة
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u", # قنوات رياضية
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u" # مكتبة VOD
]

def main():
    final_data = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    added_links = set()
    
    print("🚀 جاري صيد القنوات والأفلام من السيرفرات العالمية...")
    
    for url in SOURCES:
        try:
            # إضافة User-Agent عشان المواقع ما تحظرك
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=20)
            
            if r.status_code == 200:
                # صيد الروابط والبيانات
                items = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                
                for info, link in items:
                    link = link.strip()
                    if link not in added_links:
                        # تصنيف ذكي للمجلدات
                        info_lower = info.lower()
                        if any(x in info_lower for x in ["bein", "sport", "ssc", "kora"]):
                            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="🔥 SPORTS LIVE"', info)
                        elif any(x in info_lower for x in ["movie", "فيلم", "egybest", "netflix"]):
                            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="🎬 MOVIES LIBRARY"', info)
                        elif any(x in info_lower for x in ["series", "مسلسل", "episode", "season"]):
                            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="📺 SERIES LIBRARY"', info)
                        else:
                            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="🌍 GLOBAL TV"', info)
                        
                        final_data += f"{info}\n{link}\n"
                        added_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
        
    print(f"✅ تم بنجاح! جمعنا {len(added_links)} مادة ترفيهية.")

if __name__ == "__main__":
    main()
