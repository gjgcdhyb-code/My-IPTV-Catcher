from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from urllib.parse import unquote

# الأهداف التي اكتشفتها أنت (الروابط التي تعطي Amazon S3 و HLS)
TARGETS = [
    "https://rwtiaaaaaaaa.kora-live-live.info/", # المصدر الأول
    "https://s3.eu-north-1.amazonaws.com/"      # المصدر الثاني (Amazon S3)
]

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    final_links = set()

    print(f"🎯 Targeted Extraction Started on your discovered links...")

    for site in TARGETS:
        try:
            print(f"📡 Accessing: {site}")
            driver.get(site)
            time.sleep(10) # وقت كافٍ لجلب الـ m3u8

            html = driver.page_source
            # صيد روابط البث المباشر فقط m3u8
            links = re.findall(r'(https?://[^\s"\'<>]+(?:\.m3u8))', html)

            for link in links:
                clean_link = unquote(link).replace('\\/', '/')
                # فلترة لضمان الحصول على روابط شبيهة بالتي أرسلتها
                if "amazon" in clean_link or "live" in clean_link:
                    final_links.add(clean_link)
        except:
            continue

    driver.quit()

    # كتابة الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # إضافة الروابط التي دزيتها أنت يدوياً لضمان وجودها دائماً
        f.write(f'#EXTINF:-1 group-title="PREMIUM", My Discovered Stream 1\nhttps://rwtiaaaaaaaa.kora-live-live.info/hls/ch3/live/index.m3u8\n')
        f.write(f'#EXTINF:-1 group-title="PREMIUM", Amazon S3 Storage\nhttps://s3.eu-north-1.amazonaws.com/196.a33/hls/1/stream.m3u8\n')
        
        # إضافة أي روابط جديدة يجدها السكربت من نفس المصادر
        for i, link in enumerate(final_links):
            if "index.m3u8" not in link and "stream.m3u8" not in link: # تجنب التكرار
                f.write(f'#EXTINF:-1 group-title="AUTO-DETECT", New Stream {i}\n{link}\n')

    print(f"✅ Finished! Your links are locked in playlist.m3u")

if __name__ == "__main__":
    main()
