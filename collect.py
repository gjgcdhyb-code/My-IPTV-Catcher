import requests
import re
import urllib3

# تعطيل تحذيرات SSL لضمان عدم توقف السكربت
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# قائمة كل المواقع التي أرسلتها (لايف + سينما)
ALL_MY_TARGETS = [
    "https://news1.site88.top/koranews/", "https://www.new-yalla-shot.com/",
    "https://www.elahmad.com/tv/__aljazeera_sport.php", "https://livetv.aflam4you.net/beinsports-free-qatar-kora-direct-online_117.html",
    "https://hyzrsport.com/channel/%D8%A8%D8%AB-%D9%85%D8%A8%D8%A7%D8%B4%D8%B1-%D9%82%D9%86%D9%88%D8%A7%D8%AA-bein-sports/",
    "http://tv.shabakaty.com/", "https://www.elahmad.com/tv/live-arabic-channels.php",
    "http://azrotv.com/iphone/arabic/", "https://habbabihd.com/tv/", "https://www.qanwatlive.com/",
    "https://iptv-kw.com/%D9%82%D9%86%D9%88%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8Current%D8%A9-%D8%A8%D8%AB-%D9%85%D8%A8%D8%A7%D8%B4%D8%B1/",
    "https://www.dazn.com/ar-MA/sport/Sport:9kn3pow0we2r8hna2p0k4m2ff", "https://tviraq.net/",
    "https://cinema.shashety.com/", "https://cimanow.cc/", "https://cinemana.shabakaty.cc/CTV/#/home",
    "https://cinemana.shabakaty.com/home", "https://egibest.my/", "https://i-egybest.com/",
    "https://hd1.brstej.com/cat45.php?cat=ramdan2026", "https://www.farfeshplus.com/Rmd45.asp",
    "https://watanflix.com/ar", "https://ramadan-series.com/", "https://cimafree.info/",
    "https://w7.almstba.tv/", "https://asd.pics/main4/", "https://larozaa.website/home.24", "https://topcinema.fan/"
]

def main():
    final_content = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    unique_links = set()
    count = 0
    
    print(f"🚀 Starting the Big Scan on {len(ALL_MY_TARGETS)} sites...")

    for site in ALL_MY_TARGETS:
        try:
            # محاكاة متصفح حقيقي لتجنب الحجب
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(site, headers=headers, timeout=15, verify=False)
            
            if r.status_code == 200:
                # صيد كل أنواع روابط البث والافلام (m3u8, mp4, mkv)
                links = re.findall(r'(http[s]?://[^\s"\']+\.(?:m3u8|mp4|mkv|ts)[^\s"\']*)', r.text)
                
                for link in links:
                    link = link.strip()
                    if link not in unique_links:
                        # تصنيف ذكي للمجموعات
                        group = "🎬 CINEMA & VOD"
                        if "m3u8" in link or "tv" in site or "live" in site:
                            group = "⚽ LIVE & SPORTS"
                        
                        # اسم تلقائي بسيط
                        name = f"Item-{count}"
                        if "bein" in link.lower(): name = f"beIN-Sport-{count}"
                        
                        final_content += f'#EXTINF:-1 group-title="{group}",{name}\n{link}\n'
                        unique_links.add(link)
                        count += 1
        except Exception as e:
            print(f"⚠️ Error in {site}: {e}")
            continue

    # حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ Success! Found {len(unique_links)} working links.")

if __name__ == "__main__":
    main()
