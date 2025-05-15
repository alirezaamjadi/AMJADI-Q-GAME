import os
import requests

# تابع برای دانلود فونت وزیر
def download_font():
    font_url = "https://github.com/rastikerdar/vazir-font/raw/master/dist/font-face/Vazir-Regular.ttf"
    font_folder = "fonts"
    font_file = "Vazir-Regular.ttf"
    
    # چک کردن اینکه آیا پوشه fonts وجود دارد یا نه
    if not os.path.exists(font_folder):
        os.makedirs(font_folder)
    
    # مسیر ذخیره‌سازی فونت
    font_path = os.path.join(font_folder, font_file)
    
    # دانلود فایل فونت
    try:
        print("در حال دانلود فونت وزیر...")
        response = requests.get(font_url)
        response.raise_for_status()  # بررسی اینکه دانلود موفقیت‌آمیز بوده است
        with open(font_path, "wb") as f:
            f.write(response.content)
        print(f"فونت وزیر با موفقیت دانلود و ذخیره شد: {font_path}")
    except requests.exceptions.RequestException as e:
        print(f"خطا در دانلود فونت: {e}")

# فراخوانی تابع برای دانلود فونت اگر فونت وجود ندارد
font_path = "fonts/Vazir-Regular.ttf"
if not os.path.exists(font_path):
    download_font()

# سپس ادامه کد بازی شما
import pygame
pygame.init()

# استفاده از فونت
font = pygame.font.Font(font_path, 48)

# بقیه کد بازی...
