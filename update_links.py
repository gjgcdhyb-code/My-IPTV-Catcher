import requests
import re

# الرابط الحالي والمعلومات الأساسية
SERVER = "http://vipwettbornwet.top:8080"
CHANNEL_ID = "37642"
TOKEN_PART = "1260f37e4c58"

def find_new_accounts():
    # هنا كمبرمج وهكر، يمكنك إضافة منطق لجلب يوزرات من مواقع تسريب (Scraping)
    # أو تجربة نمط معين (Pattern) لليوزرات
    return ["VIP016471744476160385", "VIP016471744476160386"]

def update_m3u():
    accounts = find_new_accounts()
    for acc in accounts:
        test_url = f"{SERVER}/{acc}/{TOKEN_PART}/{CHANNEL_ID}"
        try:
            if requests.head(test_url, timeout=5).status_code == 200:
                # إذا اشتغل الرابط، نقوم بتحديث ملف playlist.m3u
                with open("playlist.m3u", "w") as f:
                    f.write("#EXTM3U\n")
                    f.write(f'#EXTINF:-1 tvg-name="AFG: 1 AFGHAN" ...,AFG: 1 AFGHAN\n')
                    f.write(test_url)
                return True
        except:
            continue
    return False

if __name__ == "__main__":
    update_m3u()
