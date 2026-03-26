import requests
import re

# المصادر: روابط مباشرة + صفحات تليجرام (عرض الويب)
SOURCES = [
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()
    
    # رأس الطلب لتبدو وكأنك متصفح عادي وتتجنب الحظر
    headers = {'User-Agent': 'Mozilla/5.0'}

    for src in SOURCES:
        try:
            response = requests.get(src, timeout=15, headers=headers)
            # استخراج روابط m3u8 بكل أشكالها
            links = re.findall(r'https?://[^\s<>"]+\.m3u8[^\s<>"]*', response.text)
            
            for link in links:
                # تنظيف الرابط من أي علامات اقتباس
                clean_link = link.split('"')[0].split("'")[0]
                
                if clean_link not in seen_links:
                    final_list += f"#EXTINF:-1, Stream-{len(seen_links)+1}\n{clean_link}\n"
                    seen_links.add(clean_link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"Done! Found {len(seen_links)} links.")

if __name__ == "__main__":
    main()
