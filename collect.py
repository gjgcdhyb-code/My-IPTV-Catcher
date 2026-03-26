import requests
import re
import cloudscraper

# قائمة المواقع اللي دزيتها (اللايف والسينما)
MY_SITES = [
    "https://news1.site88.top/koranews/",
    "https://www.new-yalla-shot.com/",
    "https://www.elahmad.com/tv/live-arabic-channels.php",
    "https://livetv.aflam4you.net/",
    "https://hyzrsport.com/channel/",
    "http://tv.shabakaty.com/",
    "http://azrotv.com/iphone/arabic/",
    "https://habbabihd.com/tv/",
    "https://www.qanwatlive.com/",
    "https://iptv-kw.com/",
    "https://tviraq.net/",
    "https://cinema.shashety.com/",
    "https://cimanow.cc/",
    "https://cinemana.shabakaty.com/",
    "https://egibest.my/",
    "https://i-egybest.com/",
    "https://hd1.brstej.com/",
    "https://www.farfeshplus.com/",
    "https://watanflix.com/ar",
    "https://ramadan-series.com/",
    "https://cimafree.info/",
    "https://w7.almstba.tv/",
    "https://asd.pics/",
    "https://larozaa.website/",
    "https://topcinema.fan/"
]

def scrape_target(url):
    results = []
    try:
        # استخدام cloudscraper لتجاوز حماية Cloudflare الموجودة في إيجي بيست وغيره
        scraper = cloudscraper.create_scraper()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = scraper.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            # صيد روابط البث المباشر (m3u8)
            streams = re.findall(r'(http[s]?://[^\s"\']+\.m3u8[^\s"\']*)', r.text)
            for s in streams:
                results.append(("LIVE", s))
            
            # صيد روابط الأفلام والمسلسلات (mp4 / mkv)
            vods = re.findall(r'(http[s]?://[^\s"\']+\.(?:mp4|mkv))', r.text)
            for v in vods:
                results.append(("VOD", v))
    except:
        pass
    return results

def main():
    final_content = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    unique_links = set()
    
    print(f"🚀 البدء بفحص {len(MY_SITES)} موقع من اختيارك...")

    for site in MY_SITES:
        print(f"🔍 فحص: {site}")
        found_items = scrape_target(site)
        
        for type, link in found_items:
            if link not in unique_links:
                # ترتيب المجموعات بناءً على محتوى الرابط أو الموقع
                if "shabakaty" in link or "cinemana" in link:
                    group = "🇮🇶 SHABAKATY & CINEMANA"
                elif type == "LIVE" or "sport" in link.lower() or "bein" in link.lower():
                    group = "⚽ LIVE & SPORTS"
                else:
                    group = "🎬 MOVIES & SERIES"
                
                # تنظيف الاسم (أخذ آخر جزء من الرابط كإسم)
                name = link.split('/')[-1].split('?')[0][:40]
                
                final_content += f'#EXTINF:-1 group-title="{group}",{name}\n{link}\n'
                unique_links.add(link)

    # حفظ النتيجة في ملفك الموحد
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ تم بنجاح! السكربت جمع {len(unique_links)} رابط مباشر من مواقعك.")

if __name__ == "__main__":
    main()
