def main():
    # 1. تعريف الروابط التي جلبها "القناص" (أنت)
    links = [
        {
            "name": "Yalla Shoot - CH1",
            "url": "https://rwtiaaaaaaaa.yallaliveshoot.online/hls/ch1/live/index.m3u8",
            "ref": "https://rwtiaaaaaaaa.yallaliveshoot.online/"

        },
          links = [
        {
         "name": "Yalla Shoot - CH2",
            kora_url = "https://rwtiaaaaaaaa.kora-live-live.info/hls/ch3/live/index.m3u8"
     },
        {
            "name": "Premium Server - Source 2",
            "url": "https://axfgvvsvgwi.com/jmkubwvxbiucm?uQrlpAYR=3&xAoHOJaF=4&ufUzGNCP=5258894",
            "ref": "https://31.wwwkoora.com/"
        }
    ]

    m3u_content = "#EXTM3U\n"

    for link in links:
        # نستخدم صيغة التجاوز الاحترافية |
        # نضع User-Agent عام ونحدد الـ Referer لكل رابط حسب مصدره
        m3u_content += f'#EXTINF:-1 group-title="LIVE HD", {link["name"]}\n'
        m3u_content += f'{link["url"]}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) &Referer={link["ref"]}\n'

    # 2. حفظ الملف في المستودع
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("🚀 تم دمج الروابط الجديدة مع نظام كسر الحماية!")

if __name__ == "__main__":
    main()
