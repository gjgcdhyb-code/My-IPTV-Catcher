import requests
import re
from googlesearch import search

SOURCES = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://t.me/s/iptv442web",
    "https://t.me/s/Z_Y_X_K",
    "https://raw.githubusercontent.com/Moebis/TV/master/playlist.m3u"
]

def check_link(url):
    try:
        r = requests.head(url, timeout=3)
        return r.status_code == 200
    except:
        return False

def main():
    final_list = "#EXTM3U\n"
    seen = set()
    
    # البحث التلقائي عن روابط جديدة في جوجل
    print("Searching for new links...")
    try:
        for url in search('filetype:m3u arabic 2026', num_results=5):
            SOURCES.append(url)
    except: pass

    for src in SOURCES:
        try:
            res = requests.get(src, timeout=10)
            matches = re.findall(r'(?:#EXTINF:.*,(.*)\n|([^>\n]+)\s*<a[^>]+href=")?(https?://[^\s<>"]+\.(?:m3u8|mp4|mkv|ts)[^\s<>"]*)', res.text)
            for m_name, t_name, link in matches:
                link = link.strip()
                if link not in seen and check_link(link):
                    name = (m_name or t_name or "Premium").strip()
                    group = "MOVIES" if any(x in link.lower() for x in [".mp4", ".mkv"]) else "LIVE"
                    final_list += f'#EXTINF:-1 group-title="{group}", {name}\n{link}\n'
                    seen.add(link)
        except: continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_list)

if __name__ == "__main__":
    main()
