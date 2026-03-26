import requests
import re

# مصادر القنوات
CHANNEL_SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u"
]

# مصادر أفلام (روابط مباشرة مجانية)
MOVIE_SOURCES = [
    "https://iptv-org.github.io/iptv/categories/movies.m3u"
]

SERIES_SOURCES = [
    "https://iptv-org.github.io/iptv/categories/series.m3u"
]

def fetch_m3u(url):
    try:
        r = requests.get(url, timeout=10)
        return re.findall(r'(#EXTINF:-1.*)\n(http.*)', r.text)
    except:
        return []

def categorize(info):
    text = info.lower()

    if "bein" in text:
        return "🔥 beIN SPORTS"
    elif "sport" in text:
        return "⚽ SPORTS"
    elif "movie" in text:
        return "🎬 MOVIES"
    elif "series" in text:
        return "📺 SERIES"
    else:
        return "🌍 OTHER"

def main():
    final = "#EXTM3U\n"
    added = set()

    print("🔍 Collecting channels...")
    for src in CHANNEL_SOURCES:
        for info, link in fetch_m3u(src):
            if link in added:
                continue

            group = categorize(info)
            info = re.sub(r'#EXTINF:-1', f'#EXTINF:-1 group-title="{group}"', info)

            final += f"{info}\n{link}\n"
            added.add(link)

    print("🎬 Adding Movies...")
    for src in MOVIE_SOURCES:
        for info, link in fetch_m3u(src):
            if link in added:
                continue

            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="🎬 MOVIES"', info)
            final += f"{info}\n{link}\n"
            added.add(link)

    print("📺 Adding Series...")
    for src in SERIES_SOURCES:
        for info, link in fetch_m3u(src):
            if link in added:
                continue

            info = re.sub(r'#EXTINF:-1', '#EXTINF:-1 group-title="📺 SERIES"', info)
            final += f"{info}\n{link}\n"
            added.add(link)

    with open("ultimate_entertainment.m3u", "w", encoding="utf-8") as f:
        f.write(final)

    print(f"✅ Done! Total items: {len(added)}")

if __name__ == "__main__":
    main()
