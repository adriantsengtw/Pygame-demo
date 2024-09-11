import pygame as pg
from sys import exit
from tkinter import messagebox

import main_title

scr_w = 800
scr_h = 600
chi_font = "font\\NotoSansTC-Regular.ttf"

def main():
    pg.init()
    pg.mixer.init()

    clock = pg.time.Clock()
    pg.display.set_caption('Pygame Demo')
    screen = pg.display.set_mode((scr_w, scr_h))
    screen.fill((0, 0, 0))
    if pg.mixer.get_busy():
        pg.mixer.stop()
    pg.mixer.music.load("audio\\spencer_y.k._-_fear_of_the_dark.mp3")
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.8)

    blink = pg.USEREVENT + 1
    pg.time.set_timer(blink, 800)
    
    # 設定背景圖片
    try:
        help_img = pg.image.load("img\\help_chi.png").convert()
        help_img = pg.transform.scale(help_img, (scr_w, scr_h - 20))
        screen.blit(help_img, (0, 0))
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"圖片讀取失敗：{e}")

    font = pg.font.Font(chi_font, 20)
    text = font.render("點擊滑鼠右鍵回到主畫面", True, (255, 255, 0))
    show_text = True
    
    pg.display.update()

    running = True

    while running:
        clock.tick(60)
        right_click = pg.mouse.get_pressed()[2] # 點擊滑鼠右鍵
        
        for event in pg.event.get():
            if event.type == pg.QUIT: # 退出遊戲
                running = False
            if event.type == blink:
                show_text = not show_text
            if event.type == pg.MOUSEBUTTONUP and right_click:
                main_title.main()
        
        screen.fill((0, 0, 0))
        screen.blit(help_img, (0, 0))
        if show_text:
            screen.blit(text, text.get_rect(bottomright = screen.get_rect().bottomright))

        pg.display.update()

    pg.quit()
    exit()

if __name__ == '__main__':    
    main()