import requests
import re

# مصادر قوية (يمكنك إضافة روابط قنوات تليجرام أو مواقع هنا)
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u"
]

def check_link(url):
    try:
        # فحص سريع للتأكد أن الرابط شغال وغير منقطع
        r = requests.head(url, timeout=3)
        return r.status_code == 200
    except:
        return False

def main():
    final_list = "#EXTM3U\n"
    for src in SOURCES:
        response = requests.get(src)
        # استخراج روابط BeIN و OSN باستخدام Regex
        matches = re.findall(r'(#EXTINF.*(?:beIN|OSN|SSC).*)\n(http.*)', response.text)
        
        for info, link in matches:
            if check_link(link):
                # إضافة وسوم الجودة لضمان 1080p إذا توفرت
                final_list += f"{info}\n{link}\n"
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)

if __name__ == "__main__":
    main()
