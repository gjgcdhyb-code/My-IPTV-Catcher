import requests
import re
import os

# 1. قائمة المصادر (IPTV + VOD Libraries)
# أضفت لك روابط تحتوي على آلاف الأفلام والمسلسلات المحدثة
M3U_SOURCES = [
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/freetv-app/freetv-app/master/playlists/playlist_ar.m3u"
]

# 2. مواقع الأفلام للزحف (EgyBest, Akwam, إلخ)
# ملاحظة: هذه المواقع تغير نطاقاتها (Domains) دائماً، لذا نعتمد على روابط الـ API والـ Raw المتجددة
VOD_SITES = [
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic_movies.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic_series.m3u"
]

def main():
    # الهيدر ليدعم البوسترات والترتيب
    final_list = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    seen_links = set()

    print("🚀 Starting the Global Scraper...")

    # دمج كل المصادر في قائمة واحدة
    all_sources = M3U_SOURCES + VOD_SITES

    for src in all_sources:
        try:
            print(f"🔍 Scraping: {src}")
            r = requests.get(src, timeout=20)
            if r.status_code == 200:
                # استخراج البيانات بدقة (اسم المحتوى، اللوجو، الرابط)
                matches = re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
                
                for info, link in matches:
                    link = link.strip()
                    if link not in seen_links:
                        info_lower = info.lower()
                        
                        # --- تصنيف المجلدات (Folders) لترتيب التطبيق ---
                        if any(x in info_lower for x in ["bein", "ssc", "sport", "كأس"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"⚽ SPORTS LIVE\"")
                        elif any(x in info_lower for x in ["movie", "فيلم", "film", "netflix", "ايجي بيست", "egybest"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🍿 MOVIES LIBRARY\"")
                        elif any(x in info_lower for x in ["series", "مسلسل", "حلقة", "season", "episode"]):
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"📺 SERIES LIBRARY\"")
                        elif "cinema" in info_lower or "سينمانا" in info_lower:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🎬 CINEMANA VOD\"")
                        else:
                            info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🌍 GENERAL TV\"")
                        
                        final_list += f"{info}\n{link}\n"
                        seen_links.add(link)
        except Exception as e:
            print(f"⚠️ Error in source {src}: {e}")
            continue

    # حفظ الملف النهائي في المستودع
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    
    print(f"✅ Finished! Total unique items found: {len(seen_links)}")

if __name__ == "__main__":
    main()
