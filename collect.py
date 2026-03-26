import requests
import re
import concurrent.futures

# تقنيات البحث (Dorks) لجلب قوائم جديدة من كل الإنترنت
SEARCH_QUERIES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/be.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u",
    # إضافة روابط API عامة تبحث عن ملفات m3u في GitHub تلقائياً
    "https://api.github.com/search/code?q=extension:m3u+beIN+sports",
    "https://api.github.com/search/code?q=extension:m3u+Netflix+arabic"
]

def fetch_content(url):
    try:
        # انتحال شخصية متصفح حقيقي لتجنب الحظر
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.text
    except:
        return ""

def extract_links(text):
    # ريجيكس (Regex) متطور لصيد أي رابط IPTV أو VOD في أي نص
    return re.findall(r'(#EXTINF:-1.*)\n(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', text)

def main():
    final_list = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    seen_links = set()
    
    print("🕵️ جاري تفعيل وضع الصياد العالمي...")

    # استخدام ThreadPoolExecutor لتسريع البحث (Multi-threading)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_content, SEARCH_QUERIES))

    for content in results:
        matches = extract_links(content)
        for info, link in matches:
            link = link.strip()
            # التأكد من عدم التكرار وصحة الرابط
            if link not in seen_links and (link.endswith('.m3u8') or link.endswith('.mp4') or link.endswith('.mkv')):
                info_l = info.lower()
                
                # تصنيف ذكي جداً بناءً على محتوى الرابط
                if any(x in info_l for x in ["bein", "ssc", "sport", "match"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"⚽ BEIN & SPORTS\"")
                elif any(x in info_l for x in ["movie", "فيلم", "egybest", "نتفلكس", "cinema"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🎬 GLOBAL MOVIES\"")
                elif any(x in info_l for x in ["series", "مسلسل", "episode", "season"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"📺 GLOBAL SERIES\"")
                else:
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🌐 GLOBAL CHANNELS\"")
                
                final_list += f"{info}\n{link}\n"
                seen_links.add(link)

    # حفظ الحصيلة الضخمة
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    
    print(f"✅ تم صيد {len(seen_links)} رابط من حول العالم!")

if __name__ == "__main__":
    main()
