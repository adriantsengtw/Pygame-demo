import pygame as pg
from sys import exit
from tkinter import messagebox

import fight
import fight_eng
import help_page
import help_page_eng

scr_w = 800
scr_h = 600
chi_font = "font\\GenWanMin2-R.ttc"

def main():
    pg.init()
    pg.mixer.init()

    clock = pg.time.Clock()
    pg.display.set_caption('Pygame Demo')
    screen = pg.display.set_mode((scr_w, scr_h))
    screen.fill((255, 255, 255))
    pg.time.delay(1000)
    if pg.mixer.get_busy():
        pg.mixer.stop()
    pg.mixer.music.load("audio\\Treasures of Ancient Dungeon.mp3")
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.3)
    
    # 設定背景圖片
    try:
        bg = pg.image.load("img\\main_bg.png").convert()
        bg_rect = bg.get_rect(center = (scr_w / 2, scr_h / 2))
        screen.blit(bg, bg_rect)
        layer = pg.Surface((scr_w, scr_h))
        layer.fill((100, 100, 100))
        layer.set_alpha(160)
        screen.blit(layer, (0, 0))
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"背景圖片讀取失敗：{e}")
    
    # 設定標題文字
    c_font = pg.font.Font(chi_font, 80)
    c_font_outline = pg.font.Font(chi_font, 80)
    c_font_outline.set_bold(1)
    e_font = pg.font.SysFont(None, 80)
    e_font_outline = pg.font.SysFont(None, 79)
    e_font_outline.set_bold(1)

    c_title_outline = c_font_outline.render("地   下   城   闖   關", True, (80, 0, 0))
    e_title_outline = e_font_outline.render("Dungeon Adventure", True, (80, 0, 0))
    c_title = c_font.render("地   下   城   闖   關", True, (180, 0, 60))
    e_title = e_font.render("Dungeon Adventure", True, (180, 0, 60))
    screen.blit(c_title_outline, c_title_outline.get_rect(center = (scr_w / 2, 100)))
    screen.blit(e_title_outline, e_title_outline.get_rect(center = (scr_w / 2, 180)))
    screen.blit(c_title, c_title.get_rect(center = (scr_w / 2, 100)))
    screen.blit(e_title, e_title.get_rect(center = (scr_w / 2, 180)))

    # 設定開始按鍵
    start_font = pg.font.Font(chi_font, 32)
    start_text = start_font.render("開始遊戲", True, (255, 255, 255))
    start = pg.draw.rect(screen, (140, 80, 0), (280, 240, 220, 60))
    screen.blit(start_text, start_text.get_rect(center = start.center))
    start_eng_text = start_font.render("Start Game", True, (255, 255, 255))
    start_eng = pg.draw.rect(screen, (140, 80, 0), (280, 320, 220, 60))
    screen.blit(start_eng_text, start_eng_text.get_rect(center = start_eng.center))
    
    # 設定遊戲說明按鍵
    help_font = pg.font.Font(chi_font, 16)
    help_text = help_font.render("遊戲說明", True, (255, 255, 255))
    help = pg.draw.rect(screen, (140, 80, 0), (280, 420, 100, 50))
    screen.blit(help_text, help_text.get_rect(center = help.center))
    help_eng_text = help_font.render("How To Play", True, (255, 255, 255))
    help_eng = pg.draw.rect(screen, (140, 80, 0), (400, 420, 100, 50))
    screen.blit(help_eng_text, help_eng_text.get_rect(center = help_eng.center))
    
    # 設定按鈕hover回復原本的效果
    def button_refresh(button):
        if button == start:
            button = pg.draw.rect(screen, (140, 80, 0), (280, 240, 220, 60))
            screen.blit(start_text, start_text.get_rect(center = button.center))
        if button == start_eng:
            button = pg.draw.rect(screen, (140, 80, 0), (280, 320, 220, 60))
            screen.blit(start_eng_text, start_eng_text.get_rect(center = button.center))
        if button == help:
            button = pg.draw.rect(screen, (140, 80, 0), (280, 420, 100, 50))
            screen.blit(help_text, help_text.get_rect(center = button.center))
        if button == help_eng:
            button = pg.draw.rect(screen, (140, 80, 0), (400, 420, 100, 50))
            screen.blit(help_eng_text, help_eng_text.get_rect(center = button.center))
    
    pg.display.update()

    running = True
    while running:
        clock.tick(60)
        pos = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT: # 退出遊戲
                running = False

        # 設定按鈕hover效果
        if start.collidepoint(pos):
            start = pg.draw.rect(screen, (200, 110, 0), (280, 240, 220, 60))
            screen.blit(start_text, start_text.get_rect(center = start.center))
        else:
            button_refresh(start)
        if start_eng.collidepoint(pos):
            start_eng = pg.draw.rect(screen, (200, 110, 0), (280, 320, 220, 60))
            screen.blit(start_eng_text, start_eng_text.get_rect(center = start_eng.center))
        else:
            button_refresh(start_eng)
        if help.collidepoint(pos):
            help = pg.draw.rect(screen, (200, 110, 0), (280, 420, 100, 50))
            screen.blit(help_text, help_text.get_rect(center = help.center))
        else:
            button_refresh(help)
        if help_eng.collidepoint(pos):
            help_eng = pg.draw.rect(screen, (200, 110, 0), (400, 420, 100, 50))
            screen.blit(help_eng_text, help_eng_text.get_rect(center = help_eng.center))
        else:
            button_refresh(help_eng)
        
        if pg.mouse.get_pressed()[0]:
            if start.collidepoint(pos):
                fight.main()
            if start_eng.collidepoint(pos):
                fight_eng.main()
            if help.collidepoint(pos):
                help_page.main()
            if help_eng.collidepoint(pos):
                help_page_eng.main()             

        pg.display.update()

    pg.quit()
    exit()

if __name__ == '__main__':    
    main()