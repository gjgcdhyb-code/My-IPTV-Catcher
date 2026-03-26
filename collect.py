import requests
import re

# مصادر متنوعة: تليجرام، جيت هاب، وقوائم عالمية محدثة
SOURCES = [
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://t.me/s/M_IPTV",
    "https://t.me/s/DailyIPTV",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/yoyoshira/iptv/main/movies.m3u", # مصدر أفلام
    "https://raw.githubusercontent.com/yoyoshira/iptv/main/series.m3u"  # مصدر مسلسلات
]

def detect_category(url, name):
    """تصنيف الرابط تلقائياً بناءً على محتواه واسمه"""
    url_u = url.upper()
    name_u = name.upper()
    
    # تصنيف الأفلام والمسلسلات (VOD)
    if any(x in url_u for x in [".MP4", ".MKV", ".AVI", "/MOVIES/", "/SERIES/"]):
        if "SERIES" in url_u or "مسلسل" in name_u:
            return "SERIES"
        return "MOVIES"
    
    # تصنيف الرياضة
    if any(x in name_u for x in ["BEIN", "SSC", "SPORT", "KORA", "AD SPORTS"]):
        return "SPORTS"
    
    return "ARABIC LIVE"

def clean_name(name):
    """تنظيف الاسم من كودات الـ HTML والرموز"""
    if not name: return "Unlabeled"
    name = re.sub(r'<[^>]+>', '', name) # حذف تاغات التليجرام
    name = re.sub(r'[^\w\s\-\(\)\[\]]', '', name)
    return name.strip()

def main():
    # الهيدر الأساسي لملف M3U
    final_list = "#EXTM3U\n"
    seen_links = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print("بدأ البحث الشامل في الويب والتليجرام...")

    for src in SOURCES:
        try:
            response = requests.get(src, timeout=20, headers=headers)
            
            # البحث عن الروابط (m3u8 لللايف، mp4/mkv للأفلام)
            # النمط الجديد يبحث عن أي رابط فيديو متبوع بنص (الاسم)
            pattern = r'(?:#EXTINF:.*,(.*)\n|([^>\n]+)\s*<a[^>]+href=")?(https?://[^\s<>"]+\.(?:m3u8|mp4|mkv|ts)[^\s<>"]*)'
            matches = re.findall(pattern, response.text)

            for m3u_name, tg_name, link in matches:
                link = link.strip()
                if link not in seen_links:
                    # اختيار الاسم المتاح (إما من M3U أو من تليجرام)
                    raw_name = m3u_name if m3u_name else tg_name
                    name = clean_name(raw_name)
                    
                    if len(name) < 2: name = "Premium Content"
                    
                    # تحديد الفئة (Category)
                    category = detect_category(link, name)
                    
                    # تحديد الجودة
                    quality = " [FHD]" if "1080" in link or "FHD" in link.upper() else ""
                    
                    # بناء السطر بتنسيق احترافي يفهمه أي تطبيق
                    final_list += f'#EXTINF:-1 group-title="{category}", {name}{quality}\n{link}\n'
                    seen_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"تم الانتهاء! المجموع: {len(seen_links)} مادة (لايف، أفلام، مسلسلات).")

if __name__ == "__main__":
    main()
