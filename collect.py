from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from urllib.parse import unquote

# 1. قائمة جميع الأهداف التي أرسلتها (لايف + سينما + مسلسلات)
TARGETS = [
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
    # مصادر إضافية لضمان المحتوى المباشر
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/IptvFree7/Iptv-Arabic/main/Movies.m3u"
]

def main():
    # 2. إعدادات المتصفح المخفي (Headless Chrome) لتجاوز الحماية
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # تشغيل الدرايفر تلقائياً
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    all_links = set()
    print(f"🚀 Starting Extraction on {len(TARGETS)} targets...")

    for site in TARGETS:
        try:
            print(f"📡 Penetrating: {site}")
            driver.get(site)
            
            # انتظار كافٍ لتشغيل الـ JavaScript وفك تشفير الروابط
            time.sleep(12) 

            html = driver.page_source
            # صيد الروابط (Regex) التي تنتهي بـ m3u8, mp4, mkv, ts
            links = re.findall(r'(https?://[^\s"\'<>]+(?:\.m3u8|\.mp4|\.mkv|\.ts)[^\s"\'<>]*)', html)

            for link in links:
                clean_link = unquote(link).replace('\\/', '/')
                # استثناء الروابط غير الصالحة أو الإعلانية
                if not any(x in clean_link for x in ["facebook", "google", "ads", "analytics", "twitter"]):
                    all_links.add(clean_link)
        except Exception as e:
            print(f"⚠️ Skip {site}: {e}")

    driver.quit()

    # 3. إنشاء ملف الـ M3U النهائي وتصنيفه
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n")
        for i, link in enumerate(all_links):
            link_low = link.lower()
            
            # تصنيف المحتوى بناءً على الرابط
            if any(x in link_low for x in [".mp4", ".mkv", "cinema", "movie", "egybest", "film"]):
                group = "🎬 MOVIES & SERIES"
            elif any(x in link_low for x in ["sport", "bein", "kora", "live", "tv"]):
                group = "⚽ SPORTS & LIVE"
            else:
                group = "🌍 CHANNELS"
            
            # استخراج اسم نظيف من الرابط
            name = link.split('/')[-1].split('?')[0].replace('.mp4','').replace('.mkv','').replace('.m3u8','').replace('-',' ').replace('_',' ')
            if len(name) < 5: 
                name = f"Premium-Channel-{i}"
            
            f.write(f'#EXTINF:-1 group-title="{group}",{name.title()}\n{link}\n')

    print(f"✅ Mission Accomplished: {len(all_links)} links captured and saved to playlist.m3u")

if __name__ == "__main__":
    main()
