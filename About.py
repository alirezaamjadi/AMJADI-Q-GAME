import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display
import math

pygame.init()

# تنظیمات پنجره
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("بازی پرسش و پاسخ امجدی | Amjadi Quiz Game")

# رنگ‌ها
BLACK = (10, 10, 10)
WHITE = (230, 230, 230)
DARK_BLUE = (15, 40, 80)
LIGHT_BLUE = (70, 160, 255)
GOLD = (255, 215, 0)
GRAY = (70, 70, 70)

TEXT_COLOR = (200, 200, 200)  # خاکستری روشن برای متن

# فونت‌ها
try:
    font_fa = pygame.font.Font("seguiemj.ttf", 26)  # فونت مناسب فارسی (اگر دارید)
except:
    font_fa = pygame.font.SysFont("Tahoma", 26)
font_en = pygame.font.SysFont("Arial", 24, bold=True)
font_main = pygame.font.SysFont("Tahoma", 18)

# متن سازنده
text_fa = "سازنده : علیرضا امجدی"
text_en = ""

def reshape_and_bidi(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

text_fa_reshaped = reshape_and_bidi(text_fa)

rendered_fa = font_fa.render(text_fa_reshaped, True, GOLD)
rendered_en = font_en.render(text_en, True, LIGHT_BLUE)

# متن README نهایی شما
game_text = """
🎮 بازی پرسش و پاسخ امجدی | Amjadi Quiz Game

📖 نحوه بازی و قوانین | How to Play & Rules

✅ شروع بازی | Starting the Game

1. تعداد بازیکنان | Number of Players:

   وقتی بازی شروع می‌شود، باید تعداد بازیکنان بین ۲ تا ۸ نفر انتخاب شود.
   سپس نام هر بازیکن به صورت منحصربه‌فرد وارد شود.

2. داور یا گرداننده | Referee / Moderator:

   یک نفر به عنوان داور پشت سیستم می‌نشیند و روند بازی را کنترل می‌کند.
   داور مسئول بررسی پاسخ‌ها و اعلام نتیجه (درست ✅ یا غلط ❌) است.

3. مثال | Example:

   بازیکنان: علی، مریم، جواد
   داور: رضا
   رضا نام بازیکنان را وارد می‌کند و بازی شروع می‌شود.

🎯 اجرای بازی و قوانین | Gameplay & Rules

سوالات به صورت تصادفی از فایل AMJADIQUE.json بارگذاری می‌شوند.
هر بازیکن به نوبت یک سوال دریافت می‌کند که وسط صفحه نمایش داده می‌شود (متن فارسی).
بازیکن باید در ⏰ ۱۵ ثانیه پاسخ خود را وارد کند.

4. قوانین بازی | Game Rules:

   پاسخ باید سریع داده شود.
   داور بررسی می‌کند که جواب صحیح ✅ یا غلط ❌ است.
   پاسخ صحیح: +۳ امتیاز
   پاسخ غلط: -۱ امتیاز
   اگر بازیکن پاسخ ندهد تا پایان ۱۵ ثانیه، پایان زمان ⏰ محسوب شده و -۱ امتیاز کسر می‌شود.

5. مثال | Example:

   سوال: «پایتخت ایران کجاست؟»
   علی پاسخ می‌دهد: «تهران» → داور: درست ✅ → علی +۳ امتیاز
   مریم پاسخ می‌دهد: «مشهد» → داور: غلط ❌ → مریم -۱ امتیاز
   جواد پاسخ نمی‌دهد تا پایان زمان → پایان زمان ⏰ → جواد -۱ امتیاز

🔄 چرخش نوبت | Turn Rotation

پس از اعلام نتیجه توسط داور، نوبت به بازیکن بعدی می‌رود.
این روند تا پایان سوالات (حداکثر ۲۵ سوال) ادامه دارد.

6. مثال | Example:

   ترتیب نوبت: علی → مریم → جواد → علی → ...

🏆 پایان بازی و اعلام نتایج | Game End & Results

پس از پاسخ به تمام سوالات، صفحه نتایج نهایی نمایش داده می‌شود.
بازیکنان بر اساس امتیازشان رتبه‌بندی می‌شوند:
🥇 اول، 🥈 دوم، 🥉 سوم

7. مثال | Example:

   علی ۱۵ امتیاز
   مریم ۸ امتیاز
   جواد ۵ امتیاز
   نتایج:

   🥇 علی (۱۵)
   🥈 مریم (۸)
   🥉 جواد (۵)

❌ خروج از بازی و تغییر حالت نمایش | Exiting & Display Mode

داور می‌تواند هر زمان دکمه خروج را بزند و بازی را ترک کند.
تغییر بین حالت پنجره‌ای و تمام‌صفحه فقط با دکمه خاکستری رنگ وسط صفحه انجام می‌شود (استفاده از دکمه F مجاز نیست).

🕹️ نکات مهم | Important Notes

داور همیشه باید پشت سیستم باشد تا پاسخ‌ها را بررسی کند.
بازیکنان فقط باید در زمان مشخص شده پاسخ دهند.
استفاده از ایموجی‌ها در پاسخ‌ها و اعلان‌ها برای جذاب‌تر شدن بازی.

👨‍💻 سازنده | Creator

علیرضا امجدی | Alireza Amjadi
"""

def prepare_multiline_text(text, font):
    lines = text.strip().split("\n")
    rendered_lines = []
    for line in lines:
        stripped = line.strip()
        # اگر خط شامل فقط انگلیسی یا ایموجی باشه به همون صورت رندر می‌کنیم
        # اما خطوط فارسی را reshape و bidi می‌کنیم
        has_persian = any('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' for c in stripped)
        if has_persian:
            reshaped = reshape_and_bidi(stripped)
            rendered_lines.append(font.render(reshaped, True, TEXT_COLOR))
        else:
            rendered_lines.append(font.render(stripped, True, TEXT_COLOR))
    return rendered_lines

rendered_game_text = prepare_multiline_text(game_text, font_main)

clock = pygame.time.Clock()

# حالت‌ها: scrolling_name (اسم پایین چپ + انیمیشن), showing_text, done
state = "scrolling_name"
anim_time = 0
anim_duration = 3000  # 3 ثانیه انیمیشن اسکرول اسم سازنده

# جایگاه اسم پایین سمت چپ
name_x = 20
name_y = HEIGHT
name_base_y = HEIGHT - rendered_fa.get_height() - 10

# موقعیت اولیه متن بازی برای اسکرول
text_y_start = HEIGHT
text_scroll_speed = 0.5
text_line_height = font_main.get_height() + 6

def draw_fancy_box(x, y, w, h, t):
    glow_intensity = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
    glow_color = (int(180 + 75 * glow_intensity), int(180 + 75 * glow_intensity), 0)
    pygame.draw.rect(screen, glow_color, (x - t, y - t, w + 2*t, h + 2*t), border_radius=12)
    pygame.draw.rect(screen, GRAY, (x, y, w, h), border_radius=12)

running = True
while running:
    dt = clock.tick(60)
    screen.fill(DARK_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if state == "scrolling_name":
        # انیمیشن پایین آمدن اسم سازنده
        if name_y > name_base_y:
            name_y -= 1.5
        else:
            anim_time += dt

        wave = math.sin(pygame.time.get_ticks() * 0.005) * 5
        scale = 1 + 0.05 * math.sin(pygame.time.get_ticks() * 0.01)

        fa_surf = pygame.transform.rotozoom(rendered_fa, 0, scale)
        en_surf = pygame.transform.rotozoom(rendered_en, 0, scale)

        box_w = fa_surf.get_width() + en_surf.get_width() + 30
        box_h = max(fa_surf.get_height(), en_surf.get_height()) + 20
        draw_fancy_box(name_x - 10, name_y - 5, box_w, box_h, 3)

        screen.blit(fa_surf, (name_x, name_y + wave))
        screen.blit(en_surf, (name_x + fa_surf.get_width() + 10, name_y + wave + (fa_surf.get_height() - en_surf.get_height()) // 2))

        if anim_time > anim_duration:
            state = "showing_text"
            text_y_start = HEIGHT

    elif state == "showing_text":
        text_y_start -= text_scroll_speed
        base_y = int(text_y_start)

        for idx, line_surf in enumerate(rendered_game_text):
            line_x = 20
            line_y = base_y + idx * text_line_height
            if -text_line_height < line_y < HEIGHT:
                screen.blit(line_surf, (line_x, line_y))

        # ثابت نگه داشتن اسم پایین سمت چپ
        box_w = rendered_fa.get_width() + rendered_en.get_width() + 30
        box_h = max(rendered_fa.get_height(), rendered_en.get_height()) + 20
        draw_fancy_box(name_x - 10, name_base_y - 5, box_w, box_h, 3)
        screen.blit(rendered_fa, (name_x, name_base_y))
        screen.blit(rendered_en, (name_x + rendered_fa.get_width() + 10, name_base_y + (rendered_fa.get_height() - rendered_en.get_height()) // 2))

        if base_y + len(rendered_game_text) * text_line_height < 0:
            state = "done"

    elif state == "done":
        # اگر خواستید بعد از اتمام متن کاری انجام بدید اینجا قرار بدید
        pass

    pygame.display.flip()

pygame.quit()
sys.exit()
