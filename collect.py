import requests
import re
import urllib3
from urllib.parse import unquote

# تعطيل تحذيرات SSL لضمان استمرار السكربت
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# قائمة جميع المواقع التي أرسلتها (لايف + سينما)
MY_ALL_SITES = [
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
    "https://iptv-kw.com/%D9%82%D9%86%D9%88%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D8%A8%D8%AB-%D9%85%D8%A8%D8%A7%D8%B4%D8%B1/", 
    "https://www.dazn.com/ar-MA/sport/Sport:9kn3pow0we2r8hna2p0k4m2ff", 
    "https://tviraq.net/", 
    "https://cinema.shashety.com/", 
    "https://cimanow.cc/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/page/28/", 
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
    # مصادر احتياطية لضمان عمل الرابط دائماً
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"
]

def get_display_name(link, site_url):
    # محاولة استخراج اسم ذكي من الرابط
    try:
        name = unquote(link.split('/')[-1].split('?')[0])
        name = name.replace('.m3u8','').replace('.mp4','').replace('.mkv','').replace('-',' ').replace('_',' ')
        if len(name) < 4:
            name = site_url.split('//')[-1].split('.')[0].upper()
        return name.title()
    except:
        return "Arabic Content"

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    final_m3u = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    unique_links = set()
    
    print(f"🚀 البدء بسحب الروابط من {len(MY_ALL_SITES)} موقع...")

    for site in MY_ALL_SITES:
        try:
            r = requests.get(site, headers=headers, timeout=15, verify=False)
            if r.status_code == 200:
                # البحث عن روابط m3u8 و mp4 و mkv و ts
                found = re.findall(r'(http[s]?://[^\s"\'<>]+(?:\.m3u8|\.mp4|\.mkv|\.ts)[^\s"\'<>]*)', r.text)
                
                for link in found:
                    link = link.strip().split('"')[0].split("'")[0]
                    if link not in unique_links:
                        # تصنيف المجموعات
                        group = "🌍 GENERAL"
                        link_lower = link.lower()
                        site_lower = site.lower()
                        
                        if any(x in link_lower or x in site_lower for x in ["sport", "bein", "kora", "live"]):
                            group = "⚽ LIVE SPORTS"
                        elif any(x in link_lower or x in site_lower for x in ["cinema", "movie", "egybest", "film", "shashety"]):
                            group = "🎬 MOVIES"
                        elif any(x in link_lower or x in site_lower for x in ["series", "ramadan", "مسلسل"]):
                            group = "📺 SERIES"
                        
                        name = get_display_name(link, site)
                        final_m3u += f'#EXTINF:-1 group-title="{group}",{name}\n{link}\n'
                        unique_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    
    print(f"✅ تم الانتهاء! تم العثور على {len(unique_links)} رابط فريد.")

if __name__ == "__main__":
    main()
