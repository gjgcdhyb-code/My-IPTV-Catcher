def main():
    # 1. قائمة الروابط "الذهبية" التي استخرجتها أنت مع إعدادات التجاوز
    # تم إضافة رابط Kora Live ورابط Yalla Shoot والرابط المار عبر كورة
    streams = [
        {
            "name": "Kora Live - CH3",
            "url": "https://rwtiaaaaaaaa.kora-live-live.info/hls/ch3/live/index.m3u8",
            "ref": "https://rwtiaaaaaaaa.kora-live-live.info/"
        },
        {
            "name": "Yalla Shoot - CH1",
            "url": "https://rwtiaaaaaaaa.yallaliveshoot.online/hls/ch1/live/index.m3u8",
            "ref": "https://rwtiaaaaaaaa.yallaliveshoot.online/"
        },
        {
            "name": "Premium Source - Koora",
            "url": "https://axfgvvsvgwi.com/jmkubwvxbiucm?uQrlpAYR=3&xAoHOJaF=4&ufUzGNCP=5258894",
            "ref": "https://31.wwwkoora.com/"
        },
        {
            "name": "Amazon S3 - Stream",
            "url": "https://s3.eu-north-1.amazonaws.com/196.a33/hls/1/stream.m3u8",
            "ref": "" # أمازون عادة لا يطلب Referer محدد
        }
    ]

    # 2. بناء محتوى الملف بتنسيق M3U احترافي
    m3u_content = "#EXTM3U\n"

    for stream in streams:
        m3u_content += f'#EXTINF:-1 group-title="LIVE SPORTS", {stream["name"]}\n'
        
        # دمج الـ User-Agent والـ Referer لكسر الحماية في المشغلات (VLC, Drama Live)
        header_bypass = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        if stream["ref"]:
            header_bypass += f"&Referer={stream['ref']}"
        
        m3u_content += f'{stream["url"]}{header_bypass}\n'

    # 3. حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("✅ تم تحديث القائمة بجميع روابطك المستخرجة مع نظام التجاوز!")

if __name__ == "__main__":
    main()
