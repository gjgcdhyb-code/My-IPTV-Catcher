import requests
import re
import urllib3

# تعطيل تحذيرات SSL لضمان عدم توقف السكربت عند المواقع الضعيفة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# قائمة كل أهدافك بدون استثناء
TARGETS = [
    "https://news1.site88.top/koranews/", "https://www.new-yalla-shot.com/",
    "https://www.elahmad.com/tv/__aljazeera_sport.php", 
    "https://livetv.aflam4you.net/beinsports-free-qatar-kora-direct-online_117.html",
    "https://hyzrsport.com/channel/%D8%A8%D8%AB-%D9%85%D8%A8%D8%A7%D8%B4%D8%B1-%D9%82%D9%86%D9%88%D8%A7%D8%AA-bein-sports/",
    "http://tv.shabakaty.com/", "https://www.elahmad.com/tv/live-arabic-channels.php",
    "http://azrotv.com/iphone/arabic/", "https://habbabihd.com/tv/", 
    "https://www.qanwatlive.com/", "https://iptv-kw.com/", "https://tviraq.net/",
    "https://cinema.shashety.com/", "https://cimanow.cc/", "https://cinemana.shabakaty.cc/CTV/#/home",
    "https://cinemana.shabakaty.com/home", "https://egibest.my/", "https://i-egybest.com/",
    "https://hd1.brstej.com/cat45.php?cat=ramdan2026", "https://www.farfeshplus.com/Rmd45.asp",
    "https://watanflix.com/ar", "https://ramadan-series.com/", "https://cimafree.info/",
    "https://w7.almstba.tv/", "https://asd.pics/main4/", "https://larozaa.website/home.24", "https://topcinema.fan/",
    # مصادر عالمية احتياطية لضمان القنوات الرياضية 24/7
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u"
]

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }

    final_content = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    unique_links = set()
    count = 0

    print(f"🕵️ Starting Deep Scrape on {len(TARGETS)} targets...")

    for site in TARGETS:
        try:
            r = requests.get(site, headers=headers, timeout=20, verify=False)
            if r.status_code == 200:
                # صيد كل الصيغ الممكنة (بث مباشر + ملفات فيديو)
                links = re.findall(r'(http[s]?://[^\s"\'<>]+(?:\.m3u8|\.mp4|\.mkv|\.ts))', r.text)
                
                for link in links:
                    clean_link = link.strip().split('"')[0].split("'")[0]
                    if clean_link not in unique_links:
                        # تصنيف ذكي جداً
                        info_low = clean_link.lower()
                        site_low = site.lower()
                        
                        if any(x in info_low or x in site_low for x in ["sport", "bein", "live", "tv", "kora", "ssc"]):
                            group = "⚽ LIVE SPORTS"
                        elif any(x in info_low or x in site_low for x in ["movie", "cinema", "film", "فيلم", "egybest"]):
                            group = "🎬 MOVIES"
                        elif any(x in info_low or x in site_low for x in ["series", "مسلسل", "ramadan"]):
                            group = "📺 SERIES"
                        else:
                            group = "🌍 GENERAL CHANNELS"
                        
                        final_content += f'#EXTINF:-1 group-title="{group}",Channel-{count}\n{clean_link}\n'
                        unique_links.add(clean_link)
                        count += 1
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ DONE! Total unique items: {len(unique_links)}")

if __name__ == "__main__":
    main()
