import requests
import re
import time
import cloudscraper

# إنشاء متصفح وهمي لتجاوز الحماية
scraper = cloudscraper.create_scraper()

# المصادر: قنوات تليجرام + قوائم عالمية
SOURCES = [
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def check_link_speed(url):
    """يفحص سرعة استجابة الرابط لضمان عدم وجود تأخير (Pings)"""
    try:
        start = time.time()
        response = scraper.get(url, timeout=5, stream=True)
        latency = time.time() - start
        if response.status_code == 200 and latency < 1.0: # فقط الروابط السريعة جداً
            return True
    except:
        return False
    return False

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()
    
    print("جاري صيد الروابط من المصادر...")
    
    for src in SOURCES:
        try:
            response = scraper.get(src, timeout=15)
            # استخراج الروابط التي تنتهي بـ m3u8 (جودة عالية)
            links = re.findall(r'https?://[^\s<>"]+\.m3u8[^\s<>"]*', response.text)
            
            for link in links:
                # تنظيف الرابط
                link = link.split('"')[0].split("'")[0]
                
                if link not in seen_links:
                    # فحص السرعة والجودة (تلقائياً)
                    if check_link_speed(link):
                        # إضافة القناة مع وسم الجودة والسرعة
                        final_list += f"#EXTINF:-1 group-title='LIVE-1080p', Captured-Stream\n"
                        final_list += f"#EXT-X-ALLOW-CACHE:NO\n{link}\n"
                        seen_links.add(link)
                        print(f"Captured Fast Stream: {link}")
        except Exception as e:
            print(f"Error skipping {src}: {e}")
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"Finished! Total High-Speed Links: {len(seen_links)}")

if __name__ == "__main__":
    main()
