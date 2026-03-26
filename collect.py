import requests
import re
import urllib3
from urllib.parse import unquote

# تعطيل تحذيرات SSL لضمان عدم توقف السكربت
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# القائمة الكاملة لكل الروابط اللي دزيتها أنت (لايف وسينما)
MY_FULL_LIST = [
    "https://news1.site88.top/koranews/", 
    "https://www.new-yalla-shot.com/",
    "https://www.elahmad.com/tv/__aljazeera_sport.php", 
    "https://livetv.aflam4you.net/beinsports-free-qatar-kora-direct-online_117.html",
    "https://hyzrsport.com/channel/%D8%A8%D8%AB-%D9%85%D8%A8%D8%A7%D8%B4%D8%B1-%D9%82%D9%86%D9%88%D8%A7%D8%AA-bein-sports/",
    "http://tv.shabakaty.com/", 
    "https://www.elahmad.com/tv/live-arabic-channels.php",
    "http://azrotv.com/iphone/arabic/", 
    "https://habbabihd.com/tv/", 
    "https://www.qanwatlive.com/", 
    "https://iptv-kw.com/", 
    "https://tviraq.net/", 
    "https://cinema.shashety.com/", 
    "https://cimanow.cc/", 
    "https://cinemana.shabakaty.cc/CTV/#/home",
    "https://cinemana.shabakaty.com/home", 
    "https://egibest.my/", 
    "https://i-egybest.com/", 
    "https://hd1.brstej.com/cat45.php?cat=ramdan2026", 
    "https://www.farfeshplus.com/Rmd45.asp",
    "https://watanflix.com/ar", 
    "https://ramadan-series.com/", 
    "https://cimafree.info/",
    "https://w7.almstba.tv/", 
    "https://asd.pics/main4/", 
    "https://larozaa.website/home.24", 
    "https://topcinema.fan/",
    # إضافة مصادر احتياطية لضمان عدم فراغ الملف
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u"
]

def get_clean_name(url):
    try:
        path = unquote(url.split('/')[-1])
        name = path.split('?')[0].replace('.m3u8','').replace('.mp4','').replace('.mkv','').replace('.ts','')
        name = name.replace('-', ' ').replace('_', ' ').replace('.', ' ')
        if len(name) < 3:
            name = url.split('/')[-2]
        return name.title()
    except:
        return "Premium Channel"

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    final_m3u = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    unique_links = set()
    
    print(f"🚀 صيد الروابط من {len(MY_FULL_LIST)} هدف...")

    for site in MY_FULL_LIST:
        try:
            r = requests.get(site, headers=headers, timeout=15, verify=False)
            if r.status_code == 200:
                # صيد m3u8 (لايف) و mp4/mkv (أفلام)
                links = re.findall(r'(http[s]?://[^\s"\'<>]+(?:\.m3u8|\.mp4|\.mkv|\.ts))', r.text)
                
                for link in links:
                    link = link.strip().split('"')[0].split("'")[0]
                    if link not in unique_links:
                        # تصنيف ذكي
                        group = "🌍 GENERAL"
                        link_low = link.lower()
                        site_low = site.lower()
                        
                        if any(x in link_low or x in site_low for x in ["sport", "bein", "kora", "live"]):
                            group = "⚽ LIVE SPORTS"
                        elif any(x in link_low or x in site_low for x in ["cinema", "movie", "film", "egybest", "shashety"]):
                            group = "🎬 MOVIES"
                        elif any(x in link_low or x in site_low for x in ["series", "ramadan", "مسلسل"]):
                            group = "📺 SERIES"
                        
                        name = get_clean_name(link)
                        final_m3u += f'#EXTINF:-1 group-title="{group}",{name}\n{link}\n'
                        unique_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print(f"✅ Success! Found {len(unique_links)} items.")

if __name__ == "__main__":
    main()
