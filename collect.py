import requests
import re

# مصادر ضخمة ومحدثة باستمرار لقنوات عربية ورياضية
SOURCES = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u",
    "https://raw.githubusercontent.com/freetv-app/freetv-app/master/playlists/playlist_ar.m3u"
]

def check_link(url):
    try:
        # فحص سريع
        r = requests.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def main():
    final_list = "#EXTM3U\n"
    seen_links = set() # لمنع تكرار الروابط

    for src in SOURCES:
        try:
            response = requests.get(src, timeout=15)
            # استخراج اسم القناة والرابط بدقة أكبر
            matches = re.findall(r'(#EXTINF.*)\n(http.*)', response.text)
            
            for info, link in matches:
                link = link.strip()
                if link not in seen_links:
                    # سنضيف القنوات العربية كلها حالياً للتجربة
                    final_list += f"{info}\n{link}\n"
                    seen_links.add(link)
        except:
            continue
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)

if __name__ == "__main__":
    main()
