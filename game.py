import pygame
import json
import sys
import random
import os
import arabic_reshaper
from bidi.algorithm import get_display


# تنظیمات اولیه Pygame
pygame.init()
info = pygame.display.Info()
FULL_WIDTH, FULL_HEIGHT = info.current_w, info.current_h
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800  # اندازه پنجره در حالت غیر تمام صفحه

# حالت نمایش
is_fullscreen = False  # حالت پیش‌فرض: پنجره‌ای
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Amjadi Game")
clock = pygame.time.Clock()

# رنگ‌ها
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
CORRECT_COLOR = (0, 255, 0)
INCORRECT_COLOR = (255, 0, 0)
EXIT_COLOR = (200, 50, 50)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
FULLSCREEN_BTN_COLOR = (100, 100, 100)

# فونت‌ها
try:
    font_regular = pygame.font.Font("fonts/Yekan.ttf", 32)
    font_bold = pygame.font.Font("fonts/Yekan-Bold.ttf", 48)
    font_large = pygame.font.Font("fonts/Yekan-Bold.ttf", 64)
except:
    font_regular = pygame.font.SysFont('arial', 32)
    font_bold = pygame.font.SysFont('arial', 48, bold=True)
    font_large = pygame.font.SysFont('arial', 64, bold=True)

def toggle_fullscreen():
    """تغییر حالت بین تمام صفحه و پنجره‌ای"""
    global is_fullscreen, screen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        screen = pygame.display.set_mode((FULL_WIDTH, FULL_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.flip()

def get_current_screen_size():
    """دریافت اندازه صفحه فعلی"""
    if is_fullscreen:
        return FULL_WIDTH, FULL_HEIGHT
    return WINDOW_WIDTH, WINDOW_HEIGHT

def calculate_scaled_positions():
    """محاسبه موقعیت‌های عناصر با توجه به اندازه صفحه"""
    width, height = get_current_screen_size()
    
    return {
        'question': (width // 2, height // 3),
        'player_turn': (width // 2, height // 6),
        'timer': (width // 2, height - 100),
        'scores': (50, height - 150),
        'creator': (20, height - 70),
        'exit_btn': (width - 120, height - 70),
        'fullscreen_btn': (width - 250, height - 70),
        'answer_input': (width // 2, height // 2),
        'result_title': (width // 2, 100),
        'winner': (width // 2, 250),
        'second_place': (width // 2, 400),
        'third_place': (width // 2, 550),
        'final_exit': (width // 2, height - 100)
    }

def render_text(text, font, color):
    """نمایش متن فارسی با راست‌چین"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return font.render(bidi_text, True, color)

def draw_text(text, font, color, x, y, centered=False):
    """رسم متن روی صفحه"""
    text_surface = render_text(text, font, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color):
    """رسم دکمه روی صفحه"""
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=10)
    draw_text(text, font_regular, TEXT_COLOR, x + width//2, y + height//2, centered=True)
    return rect

def draw_fullscreen_button():
    """رسم دکمه تغییر حالت تمام صفحه"""
    pos = calculate_scaled_positions()
    text = "" if is_fullscreen else ""
    btn = draw_button(text, pos['fullscreen_btn'][0], pos['fullscreen_btn'][1], 280, 50, FULLSCREEN_BTN_COLOR)
    return btn

def get_user_input(prompt):
    """دریافت ورودی از کاربر"""
    input_text = ""
    input_active = True
    pos = calculate_scaled_positions()
    
    while input_active:
        screen.fill(BACKGROUND_COLOR)
        draw_text(prompt, font_regular, TEXT_COLOR, pos['answer_input'][0], pos['answer_input'][1] - 100, centered=True)
        
        # نمایش متن ورودی
        input_surface = render_text(input_text, font_bold, TEXT_COLOR)
        input_rect = input_surface.get_rect(center=pos['answer_input'])
        pygame.draw.rect(screen, BUTTON_COLOR, input_rect.inflate(20, 10), 2, border_radius=5)
        screen.blit(input_surface, input_rect)
        
        # دکمه تمام صفحه
        fullscreen_btn = draw_fullscreen_button()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                    toggle_fullscreen()
                else:
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if fullscreen_btn.collidepoint(mouse_pos):
                    toggle_fullscreen()
    
    return input_text.strip()

def load_questions():
    """بارگذاری سوالات از فایل JSON"""
    try:
        with open('AMJADIQUE.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data.get('questions'):
                raise ValueError("فایل سوالات ساختار صحیح ندارد")
            return data['questions']
    except FileNotFoundError:
        print("خطا: فایل سوالات یافت نشد")
        return []
    except json.JSONDecodeError:
        print("خطا: فایل سوالات معتبر نیست")
        return []
    except Exception as e:
        print(f"خطای ناشناخته: {str(e)}")
        return []

def show_scores(players):
    """نمایش امتیازات بازیکنان"""
    pos = calculate_scaled_positions()
    y_position = pos['scores'][1]
    for i, player in enumerate(sorted(players, key=lambda x: x['score'], reverse=True)):
        text = f"{i+1}. {player['name']}: {player['score']}"
        

def show_final_results(players):
    """نمایش نتایج نهایی با برنده بزرگ و نفرات دوم و سوم"""
    # مرتب کردن بازیکنان بر اساس امتیاز
    sorted_players = sorted(players, key=lambda x: x['score'], reverse=True)
    pos = calculate_scaled_positions()
    
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # نمایش عنوان
        draw_text("نتایج نهایی", font_large, GOLD, pos['result_title'][0], pos['result_title'][1], centered=True)
        
        # نمایش برنده اول (بزرگ)
        if len(sorted_players) > 0:
            draw_text("برنده بزرگ:", font_bold, GOLD, pos['winner'][0], pos['winner'][1] - 50, centered=True)
            draw_text(sorted_players[0]['name'], font_large, GOLD, pos['winner'][0], pos['winner'][1], centered=True)
            draw_text(f"امتیاز: {sorted_players[0]['score']}", font_bold, GOLD, pos['winner'][0], pos['winner'][1] + 60, centered=True)
        
        
        
        # نمایش نفر دوم
        if len(sorted_players) > 1:
            draw_text("نفر دوم:", font_bold, SILVER, pos['second_place'][0], pos['second_place'][1] - 50, centered=True)
            draw_text(sorted_players[1]['name'], font_bold, SILVER, pos['second_place'][0], pos['second_place'][1], centered=True)
            draw_text(f"امتیاز: {sorted_players[1]['score']}", font_regular, SILVER, pos['second_place'][0], pos['second_place'][1] + 60, centered=True)
        
        # نمایش نفر سوم
        if len(sorted_players) > 2:
            draw_text("نفر سوم:", font_bold, BRONZE, pos['third_place'][0], pos['third_place'][1] - 50, centered=True)
            draw_text(sorted_players[2]['name'], font_bold, BRONZE, pos['third_place'][0], pos['third_place'][1], centered=True)
            draw_text(f"امتیاز: {sorted_players[2]['score']}", font_regular, BRONZE, pos['third_place'][0], pos['third_place'][1] + 70, centered=True)
        
        # دکمه‌های کنترل
        fullscreen_btn = draw_fullscreen_button()
        exit_btn = draw_button("خروج", pos['final_exit'][0] - 50, pos['final_exit'][1], 100, 50, EXIT_COLOR)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_btn.collidepoint(mouse_pos):
                    running = False
                elif fullscreen_btn.collidepoint(mouse_pos):
                    toggle_fullscreen()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    toggle_fullscreen()

    pygame.quit()
    sys.exit()

def game_loop():
    """حلقه اصلی بازی"""
    global is_fullscreen
    
    # حالت اولیه پنجره‌ای
    is_fullscreen = False
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # دریافت تعداد بازیکنان
    while True:
        num_players = get_user_input("تعداد بازیکنان (2-8):")
        try:
            num_players = int(num_players)
            if 2 <= num_players <= 8:
                break
        except:
            pass
    
    # دریافت نام بازیکنان
    players = []
    for i in range(num_players):
        while True:
            name = get_user_input(f"نام بازیکن {i+1}: ").strip()
            if name:
                players.append({"name": name, "score": 0})
                break
    
    # بارگذاری سوالات
    questions = load_questions()
    if not questions:
        pos = calculate_scaled_positions()
        draw_text("خطا در بارگذاری سوالات!", font_bold, INCORRECT_COLOR, pos['question'][0], pos['question'][1], centered=True)
        pygame.display.flip()
        pygame.time.wait(2000)
        return
    
    random.shuffle(questions)
    total_questions = min(25, len(questions))  # حداکثر 25 سوال
    
    player_turn = 0
    for question_num in range(total_questions):
        current_player = players[player_turn]
        question = questions[question_num]
        pos = calculate_scaled_positions()
        
        # نمایش سوال
        start_time = pygame.time.get_ticks()
        answered = False
        answer = ""
        
        while not answered:
            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            remaining = max(0, 15 - elapsed)
            
            if remaining <= 0:
                draw_text("زمان شما به پایان رسید!", font_bold, INCORRECT_COLOR, pos['question'][0], pos['question'][1] + 150, centered=True)
                pygame.display.flip()
                pygame.time.wait(2000)
                players[player_turn]['score'] -= 1
                break
            
            # نمایش صفحه سوال
            screen.fill(BACKGROUND_COLOR)
            draw_text(f"نوبت: {current_player['name']}", font_bold, TEXT_COLOR, pos['player_turn'][0], pos['player_turn'][1], centered=True)
            draw_text(question, font_bold, BUTTON_COLOR, pos['question'][0], pos['question'][1], centered=True)
            
            # نمایش زمان باقیمانده
            draw_text(f"زمان باقیمانده: {int(remaining)} ثانیه", font_regular, TEXT_COLOR, pos['timer'][0], pos['timer'][1], centered=True)
            
            # نمایش امتیازات
            show_scores(players)
            
            # دکمه‌های کنترل
            fullscreen_btn = draw_fullscreen_button()
            draw_button("سازنده: علیرضا امجدی", pos['creator'][0], pos['creator'][1], 300, 50, BUTTON_COLOR)
            exit_btn = draw_button("خروج", pos['exit_btn'][0], pos['exit_btn'][1], 100, 50, EXIT_COLOR)
            
            pygame.display.flip()
            
            # دریافت رویدادها
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        answered = True
                        answer = get_user_input(f"{current_player['name']}، پاسخ شما:")
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        toggle_fullscreen()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_btn.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif fullscreen_btn.collidepoint(mouse_pos):
                        toggle_fullscreen()
        
        # بررسی پاسخ
        if answer:
            pos = calculate_scaled_positions()
            screen.fill(BACKGROUND_COLOR)
            draw_text(f"پاسخ شما: {answer}", font_bold, TEXT_COLOR, pos['answer_input'][0], pos['answer_input'][1] - 100, centered=True)
            
            correct_btn = draw_button("درست", pos['answer_input'][0] - 150, pos['answer_input'][1], 120, 60, CORRECT_COLOR)
            incorrect_btn = draw_button("غلط", pos['answer_input'][0] + 30, pos['answer_input'][1], 120, 60, INCORRECT_COLOR)
            fullscreen_btn = draw_fullscreen_button()
            
            pygame.display.flip()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if correct_btn.collidepoint(mouse_pos):
                            current_player['score'] += 3
                            waiting = False
                        elif incorrect_btn.collidepoint(mouse_pos):
                            current_player['score'] -= 1
                            waiting = False
                        elif fullscreen_btn.collidepoint(mouse_pos):
                            toggle_fullscreen()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            toggle_fullscreen()
        
        # تغییر نوبت
        player_turn = (player_turn + 1) % num_players
    
    # نمایش نتایج نهایی
    show_final_results(players)

if __name__ == "__main__":
    game_loop()