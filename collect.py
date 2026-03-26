import requests
import re
import concurrent.futures

# دالات البحث الذكي - تبحث في "مستودعات" ضخمة تتحدث كل دقيقة
CRAWL_TARGETS = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u",
    "https://raw.githubusercontent.com/yousef777/IPTV-Free/main/arabic.m3u",
    "https://raw.githubusercontent.com/Tiptop-IPTV/free/main/channels/ar.m3u",
    "https://raw.githubusercontent.com/Stay-Sane/Free-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/moez-b/iptv/master/playlist.m3u",
    "https://api.github.com/search/code?q=extension:m3u+bein+sport", # يبحث في كودات غيت هاب عن بين سبورت
]

def spider_hunt(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # إذا كان الرابط من API غيت هاب يحتاج معالجة خاصة، لكننا سنركز على الروابط المباشرة لسرعة السكربت
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # استخراج أي رابط فيديو يبدأ بـ http وينتهي بصيغة بث
            found = re.findall(r'(#EXTINF.*)\n(http[s]?://[^\s]+)', response.text)
            return found
    except:
        return []

def main():
    final_playlist = "#EXTM3U x-tvg-url=\"http://epg.itv.re/epg.xml.gz\"\n"
    captured_links = set()
    total_count = 0

    print("🕵️ جاري تفعيل 'الرادار' للبحث عن روابط المباريات والأفلام...")

    # استخدام ThreadPool لزيادة سرعة "الصيد" بمقدار 10 أضعاف
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(spider_hunt, CRAWL_TARGETS))

    for result in results:
        for info, link in result:
            link = link.strip()
            if link not in captured_links:
                info_low = info.lower()
                
                # تصنيف ذكي جداً لفرز الـ 20 ألف قناة
                if any(x in info_low for x in ["bein", "ssc", "sport", "kora", "match", "يلا"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"⚽ LIVE MATCHES & BEIN\"")
                elif any(x in info_low for x in ["movie", "فيلم", "netflix", "egybest", "shahid"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🍿 MOVIES LIBRARY\"")
                elif any(x in info_low for x in ["series", "مسلسل", "episode", "season"]):
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"📺 SERIES LIBRARY\"")
                else:
                    info = info.replace("#EXTINF:-1", "#EXTINF:-1 group-title=\"🌍 WORLD CHANNELS\"")
                
                final_playlist += f"{info}\n{link}\n"
                captured_links.add(link)
                total_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)
    
    print(f"✅ مبروك! السكربت صاد {total_count} رابط من كل مكان.")

if __name__ == "__main__":
    main()
