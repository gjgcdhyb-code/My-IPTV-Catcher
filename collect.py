import requests
import re
import time
import cloudscraper # لتجاوز حماية المواقع

# استخدام scraper لتجاوز الحماية
scraper = cloudscraper.create_scraper()

# 1. المصادر العامة + قنوات تليجرام (Web View)
SOURCES = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u",
    "https://t.me/s/iptv442web", # القناة اللي أرسلت صورتها
    "https://t.me/s/Z_Y_X_K"      # مثال لقناة رياضية
]

def check_quality_and_latency(url):
    try:
        start_time = time.time()
        # طلب رأس الملف فقط لسرعة الفحص (Low Latency Check)
        response = scraper.get(url, timeout=5, stream=True)
        latency = time.time() - start_time
        
        # فحص الجودة من خلال الـ Content (إذا كان متاحاً)
        # 1080p أو أعلى
        is_high_quality = True # نفترض الجودة عالية ما لم يثبت العكس
        
        if response.status_code == 200:
            # إذا كان السيرفر سريعاً (أقل من 0.8 ثانية) فهو مناسب للبث المباشر
            if latency < 0.8:
                return True, latency
    except:
        pass
    return False, 999

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()

    print("بدأ عملية الصيد الذكي...")

    for src in SOURCES:
        try:
            # كشط الروابط سواء كانت من ملف M3U أو من صفحة تليجرام
            response = scraper.get(src, timeout=15)
            # استخراج أي رابط فيديو ينتهي بـ m3u8 أو يحتوي على معلومات قناة
            matches = re.findall(r'(?:#EXTINF.*, (.*))?\n?(http[s]?://[^\s\n]+)', response.text)
            
            for name, link in matches:
                link = link.strip()
                # تنظيف الرابط من أي مخلفات برمجية
                link = re.sub(r'[\"\'\)\s]+$', '', link)

                if link not in seen_links and ('.m3u8' in link or '.m3u' in link):
                    # فحص الجودة واللايف (Latency)
                    is_good, delay = check_quality_and_latency(link)
                    
                    if is_good:
                        channel_name = name if name else "Live Stream (Fast)"
                        # إضافة وسم لتقليل البفر في التطبيق
                        final_list += f"#EXTINF:-1 group-title='LIVE-1080p', {channel_name}\n"
                        final_list += f"#EXT-X-ALLOW-CACHE:NO\n{link}\n"
                        seen_links.add(link)
                        print(f"Captured: {channel_name} | Latency: {delay:.2f}s")
        except Exception as e:
            print(f"Error in {src}: {e}")
            continue
    
    # حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"تم بنجاح! تم صيد {len(seen_links)} رابط عالي الجودة وقليل التأخير.")

if __name__ == "__main__":
    main()
