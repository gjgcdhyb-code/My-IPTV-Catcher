import os

def main():
    # الروابط التي استخرجتها أنت (الكنوز)
    kora_url = "https://rwtiaaaaaaaa.kora-live-live.info/hls/ch3/live/index.m3u8"
    amazon_url = "https://s3.eu-north-1.amazonaws.com/196.a33/hls/1/stream.m3u8"

    # صنع محتوى الملف بتنسيق احترافي يتجاوز الحماية
    # نستخدم User-Agent الخاص بـ VLC أو المتصفح لإجبار السيرفر على القبول
    m3u_content = "#EXTM3U\n"
    
    # القناة الأولى: كورة لايف مع "Referer" و "User-Agent"
    m3u_content += '#EXTINF:-1 group-title="PREMIUM", Kora Live Stream\n'
    m3u_content += f'{kora_url}|User-Agent=Mozilla/5.0&Referer=https://rwtiaaaaaaaa.kora-live-live.info/\n'
    
    # القناة الثانية: أمازون مع "User-Agent" فقط
    m3u_content += '#EXTINF:-1 group-title="PREMIUM", Amazon High Speed\n'
    m3u_content += f'{amazon_url}|User-Agent=VLC/3.0.18 LibVLC/3.0.18\n'

    # حفظ الملف
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("🚀 تم تحديث القائمة بنجاح بأقوى إعدادات التجاوز!")

if __name__ == "__main__":
    main()
