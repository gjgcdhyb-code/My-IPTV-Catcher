import requests
import re

# قائمة المصادر (يمكنك إضافة أي قناة تليجرام تريدها بنفس الصيغة)
SOURCES = [
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://t.me/s/M_IPTV",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def clean_name(name):
    """تنظيف اسم القناة من الرموز والكلمات الزائدة"""
    if not name: return "Live Stream"
    # إزالة الرموز التعبيرية والكلمات غير الضرورية
    name = re.sub(r'[^\w\s\-\(\)\[\]]', '', name)
    name = name.replace('رابط التحميل', '').replace('مباشر', '').strip()
    return name if name else "Unknown Channel"

def main():
    final_list = "#EXTM3U\n"
    seen_links = set()
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("جاري استخراج القنوات مع الأسماء...")

    for src in SOURCES:
        try:
            response = requests.get(src, timeout=15, headers=headers)
            # تقنية متطورة: البحث عن النصوص القريبة من الروابط
            # هذا النمط يبحث عن اسم القناة في ملفات M3U أو في نصوص التليجرام
            if 't.me/s/' in src:
                # في تليجرام، الاسم غالباً يكون في الفقرة التي تسبق الرابط
                blocks = re.findall(r'([^>\n]+)\s*<a[^>]+href="(https?://[^\s<>"]+\.m3u8[^"]*)"', response.text)
            else:
                # في ملفات M3U العادية
                blocks = re.findall(r'#EXTINF:.*,(.*)\n(http[s]?://[^\s\n]+)', response.text)

            for name, link in blocks:
                link = link.strip()
                if link not in seen_links:
                    c_name = clean_name(name)
                    # تصنيف تلقائي بسيط
                    group = "SPORTS" if any(x in c_name.upper() for x in ["BEIN", "SSC", "SPORT"]) else "ARABIC"
                    
                    final_list += f"#EXTINF:-1 group-title='{group}', {c_name}\n{link}\n"
                    seen_links.add(link)
                    print(f"Found: {c_name}")
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)
    print(f"Done! Captured {len(seen_links)} named channels.")

if __name__ == "__main__":
    main()
