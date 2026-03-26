import requests
import re

# المصادر الذهبية (التليجرام + السيرفرات العالمية)
SOURCES = [
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://t.me/s/M_IPTV",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def detect_quality(url, name):
    """تحليل الرابط والاسم لمعرفة الجودة"""
    url_upper = url.upper()
    name_upper = name.upper()
    
    if "4K" in url_upper or "4K" in name_upper or "UHD" in url_upper:
        return " [4K]"
    elif "1080" in url_upper or "FHD" in url_upper or "1080" in name_upper:
        return " [FHD]"
    elif "720" in url_upper or "HD" in url_upper:
        return " [HD]"
    return ""

def clean_name(name):
    """تنظيف الاسم من الشوائب"""
    if not name: return "Live Stream"
    name = re.sub(r'<[^>]+>', '', name) # حذف أي تاغات HTML من التليجرام
    name = re.sub(r'[^\w\s\-\(\)\[\]]', '', name)
    return name.strip()

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("بدأ صيد الجودات العالية...")

    for src in SOURCES:
        try:
            response = requests.get(src, timeout=15, headers=headers)
            
            # استخراج الاسم والرابط من التليجرام أو M3U
            if 't.me/s/' in src:
                blocks = re.findall(r'([^>\n]+)\s*<a[^>]+href="(https?://[^\s<>"]+\.m3u8[^"]*)"', response.text)
            else:
                blocks = re.findall(r'#EXTINF:.*,(.*)\n(http[s]?://[^\s\n]+)', response.text)

            for name, link in blocks:
                link = link.strip()
                if link not in seen_links:
                    c_name = clean_name(name)
                    quality_tag = detect_quality(link, c_name)
                    
                    # نركز فقط على القنوات اللي بيها اسم واضح أو جودة عالية
                    if len(c_name) > 2:
                        final_list += f"#EXTINF:-1, {c_name}{quality_tag}\n{link}\n"
                        seen_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"تم بنجاح! القائمة الآن تحتوي على {len(seen_links)} قناة مع جوداتها.")

if __name__ == "__main__":
    main()
