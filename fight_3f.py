import pygame as pg
from sys import exit

import random as rd
import json
from tkinter import messagebox

import main_title
import fight_2f

scr_w = 800
scr_h = 600
screen = pg.display.set_mode((scr_w, scr_h))
chi_font = "font\\NotoSerifTC-Regular.ttf"

fight_w = 150
fight_h = 200        

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    
    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pg.draw.rect(screen, (170, 0, 0), (self.x, self.y, self.w, self.h))
        pg.draw.rect(screen, (0, 164, 0), (self.x, self.y, self.w * ratio, self.h))
        

# 戰鬥主程式
def main():
    pg.init()
    pg.mixer.init()

    clock = pg.time.Clock()    
    pg.display.set_caption('Pygame Demo')
    screen.fill((255,255,255))
    
    if pg.mixer.get_busy():
        pg.mixer.stop()
    pg.mixer.music.load("audio\\Dungeon of Agony.mp3")
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.6)
    
    # 角色攻擊判定
    def attack(char):
        crit_status = False
        crit = rd.randint(1, 10)
        atk = 0
        if char in ["Phil", "菲爾"]:
        # 每次攻擊固定給予敵人 ATK 80 的攻擊
            atk = 80
        if char in ["York", "約克"]:
        # 每次給予敵人 ATK 40 - 90 之間的攻擊, 30% 機率給予 ATK 120 的爆擊
            if crit >= 8:
                crit_status = True
                atk = 120
            else:
                atk = rd.randint(40, 90)
        if char in ["Thomas", "瑪斯"]:
        # 每次給予敵人 ATK 60 - 120 之間的攻擊, 20% 機率給予 ATK 150 的爆擊
            if crit >= 9:
                crit_status = True
                atk = 150
            else:
                atk = rd.randint(60, 120)
        if char in ["Harper", "赫波"]:
        # 每次給予敵人 ATK 80 - 140 之間的攻擊, 10% 機率給予 ATK 180 的爆擊
            if crit == 10:
                crit_status = True
                atk = 180
            else:
                atk = rd.randint(80, 140)
        return crit_status, atk
    
    # 戰鬥狀態文字多行顯示與更新    
    def status_update(status_text):
        text_refresh = False
        status_lst.append(status_text)
        if len(status_lst) > status_line_lim:
            status_lst.pop(0)
            text_refresh = True
        status_text = ""
        if text_refresh == True:
            rect_text = pg.draw.rect(screen, (80, 80, 80), (600, scr_h - fight_h, 200, fight_h))
            text_refresh = False
        for i, line in enumerate(status_lst):
            status_text_r = status_font.render(line, True, (255, 255, 255))
            textRect = status_text_r.get_rect(topleft = (600, scr_h - fight_h + 20 * i))
            screen.blit(status_text_r, textRect)

    # 戰鬥成功
    def win():
        pg.mixer.music.fadeout(500)
        sound = pg.mixer.Sound("audio\\Heavy_ConceptB.wav")
        sound.play()
        sound.set_volume(0.1)
        layer = pg.Surface((scr_w, scr_h))
        layer.fill((255, 255, 255))
        layer.set_alpha(10)
        font = pg.font.Font(chi_font, 120)
        win_text = font.render("戰 鬥 成 功", True, (0, 0, 120))
        
        screen.blit(layer, (0, 0))
        screen.blit(win_text, win_text.get_rect(center = (scr_w / 2, scr_h / 2)))
        button_font = pg.font.Font(chi_font, 30)
        main_menu = pg.draw.rect(screen, (140, 80, 0), (100, scr_h / 2 + 80, 200, 50))
        main_menu_text = button_font.render("回到主選單", True, (255, 255, 255))
        next_level = pg.draw.rect(screen, (140, 80, 0), (500, scr_h / 2 + 80, 200, 50))
        next_level_text = button_font.render("進入下一層", True, (255, 255, 255))
        screen.blit(main_menu_text, main_menu_text.get_rect(center = main_menu.center))
        screen.blit(next_level_text, next_level_text.get_rect(center = next_level.center))
        
        pos = pg.mouse.get_pos()
        if main_menu.collidepoint(pos):
            main_menu = pg.draw.rect(screen, (200, 110, 0), (100, scr_h / 2 + 80, 200, 50))
            screen.blit(main_menu_text, main_menu_text.get_rect(center = main_menu.center))
        if next_level.collidepoint(pos):
            next_level = pg.draw.rect(screen, (200, 110, 0), (500, scr_h / 2 + 80, 200, 50))
            screen.blit(next_level_text, next_level_text.get_rect(center = next_level.center))

        if event.type == pg.MOUSEBUTTONUP and left_click:
            pos = pg.mouse.get_pos()
            if main_menu.collidepoint(pos):
                main_title.main()
            if next_level.collidepoint(pos):
                font = pg.font.Font(chi_font, 24)
                not_text = font.render("尚未開放", True, (0, 0, 0))
                screen.blit(not_text, not_text.get_rect(center = (next_level.centerx, next_level.centery + 60)))
                

    # 戰鬥失敗
    def lose():
        pg.mixer.music.fadeout(500)
        sound = pg.mixer.Sound("audio\\death.wav")
        sound.play()
        sound.set_volume(0.2)
        layer = pg.Surface((scr_w, scr_h))
        layer.fill((100, 100, 100))
        layer.set_alpha(10)
        font = pg.font.Font(chi_font, 120)
        lose_text = font.render("戰  鬥  失  敗", True, (255, 0, 0))
       
        screen.blit(layer, (0, 0))
        screen.blit(lose_text, lose_text.get_rect(center = (scr_w / 2, scr_h / 2)))
        button_font = pg.font.Font(chi_font, 30)
        main_menu = pg.draw.rect(screen, (140, 80, 0), (scr_w / 2 - 100, scr_h / 2 + 80, 200, 50))
        main_menu_text = button_font.render("回到主選單", True, (255, 255, 255))
        screen.blit(main_menu_text, main_menu_text.get_rect(center = main_menu.center))
        
        pos = pg.mouse.get_pos()
        if main_menu.collidepoint(pos):
            main_menu = pg.draw.rect(screen, (200, 110, 0), (scr_w / 2 - 100, scr_h / 2 + 80, 200, 50))
            screen.blit(main_menu_text, main_menu_text.get_rect(center = main_menu.center))
        
        if event.type == pg.MOUSEBUTTONUP and left_click:
            pos = pg.mouse.get_pos()
            if main_menu.collidepoint(pos):
                main_title.main()

    # 設定背景圖片
    try:
        bg = pg.image.load("img\\fight_bg2.png").convert()
        bg_rect = bg.get_rect(center = (scr_w / 2, scr_h / 2))
        screen.blit(bg, bg_rect)
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"背景圖片讀取失敗：{e}")
    
    # 設定敵人圖片
    try:
        enemy = pg.image.load("img\\enemy3_tpbg.png").convert_alpha()
        enemy = pg.transform.scale(enemy, (scr_h - 250, scr_h - 250))
        enemy_rect = enemy.get_rect(center = (scr_w / 2, 250))
        screen.blit(enemy, enemy_rect)
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"敵人圖片讀取失敗：{e}")
    
    # 設定角色顯示區塊
    rect_char1 = pg.draw.rect(screen, (80, 80, 80), (0, scr_h - fight_h, fight_w, fight_h))
    rect_char2 = pg.draw.rect(screen, (0, 0, 0), (150, scr_h - fight_h, fight_w, fight_h))
    rect_char3 = pg.draw.rect(screen, (80, 80, 80), (300, scr_h - fight_h, fight_w, fight_h))
    rect_char4 = pg.draw.rect(screen, (0, 0, 0), (450, scr_h - fight_h, fight_w, fight_h))
        
    # 載入角色資料
    try:
        char_data = "data\\fight_char.json"
        with open(char_data, encoding = "utf-8") as rf:
            data = json.load(rf)
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"角色資料讀取失敗：{e}")

    # 玩家決定角色順序
    char_name = []
    char_hp = []
    char_attack_note = []
    char_pic = []

    char_select = "1234" # 預留未來選擇角色的空間

    # 系統產生對戰角色
    for i in char_select:
        for j in data:
            if int(i) == j["Num"]:
                char_name.append(j["Chi"])
                char_hp.append(j["HP"])
                char_attack_note.append(j["Attack_note"])
                char_pic.append(j["Pic"])
                continue

    char_hp = list(map(int, char_hp))

    bt_name = char_name.copy()
    bt_hp = char_hp.copy()

    # 設定角色圖片
    char_img = []
    try:
        for pic in char_pic:
            pic_url = "img\\" + pic
            char = pg.image.load(pic_url).convert()
            char_img.append(char)
        for i, char in enumerate(char_img):
            char = pg.transform.scale(char, (fight_w, fight_h - 50))
            screen.blit(char, (150 * i, scr_h - fight_h))
    except Exception as e:
        messagebox.showerror("遊戲錯誤訊息", f"角色圖片讀取失敗：{e}")
                                
    # 設定角色名字
    char_font = pg.font.Font(chi_font, 28)
    char_margin = 65
    char1_r = char_font.render(bt_name[0], True, (255, 255, 255))
    char1_Rect = char1_r.get_rect(center = (rect_char1.centerx, rect_char1.centery + char_margin))
    char2_r = char_font.render(bt_name[1], True, (255, 255, 255))
    char2_Rect = char2_r.get_rect(center = (rect_char2.centerx, rect_char2.centery + char_margin))
    char3_r = char_font.render(bt_name[2], True, (255, 255, 255))
    char3_Rect = char3_r.get_rect(center = (rect_char3.centerx, rect_char3.centery + char_margin))
    char4_r = char_font.render(bt_name[3], True, (255, 255, 255))
    char4_Rect = char4_r.get_rect(center = (rect_char4.centerx, rect_char4.centery + char_margin))
    screen.blit(char1_r, char1_Rect)
    screen.blit(char2_r, char2_Rect)
    screen.blit(char3_r, char3_Rect)
    screen.blit(char4_r, char4_Rect)

    # 設定戰鬥狀態區塊
    rect_text = pg.draw.rect(screen, (80, 80, 80), (600, scr_h - fight_h, 200, fight_h))
    status_font = pg.font.Font(chi_font, 14)
    status_line_lim = 9
    status_lst = []
    
    # 設定說明區塊
    note = "敵人有 30% 機率攻擊第二次"
    note_font = pg.font.Font(chi_font, 13)
    def note_text(note):
        rect_note = pg.draw.rect(screen, (30, 30, 30), (0, 380, scr_w, 20))
        note_r = note_font.render(note, True, (255, 255, 255))
        note_Rect = note_r.get_rect(topleft = rect_note.topleft)
        screen.blit(note_r, note_Rect)
    note_text(note)
    
    # 設定角色血量
    hp_h = 10
    hp_char1 = HealthBar(5, scr_h - hp_h, 135, hp_h, char_hp[0])
    hp_char2 = HealthBar(155, scr_h - hp_h, 135, hp_h, char_hp[1])
    hp_char3 = HealthBar(305, scr_h - hp_h, 135, hp_h, char_hp[2])
    hp_char4 = HealthBar(455, scr_h - hp_h, 135, hp_h, char_hp[3])
    hp_char1.draw(screen)
    hp_char2.draw(screen)
    hp_char3.draw(screen)
    hp_char4.draw(screen)
    def hp():
        hp_char1.hp = bt_hp[0]
        hp_char2.hp = bt_hp[1]
        hp_char3.hp = bt_hp[2]
        hp_char4.hp = bt_hp[3]
        hp_char1.draw(screen)
        hp_char2.draw(screen)
        hp_char3.draw(screen)
        hp_char4.draw(screen)
        
    # 設定敵人血量
    enemy_full_hp = 950
    enemy_hp = 950
    hp_enemy = HealthBar(100, 50, 600, 20, enemy_full_hp)
    hp_enemy.draw(screen)
    
    # 設定回合數
    round_count = 8
    round_font = pg.font.Font(chi_font, 18)
    def round():
        if round_count <= 2:
            round_text = round_font.render("剩餘回合數：" + str(round_count), True, (255, 0, 0))
        else:
            round_text = round_font.render("剩餘回合數：" + str(round_count), True, (255, 255, 255))
        pg.draw.rect(screen, (0, 0, 0), (scr_w - 160, 0, 160, 25))
        screen.blit(round_text, round_text.get_rect(topright = (scr_w, 0)))       
    round()

    # 設定角色區塊重新整理
    def refresh_char():
        pg.draw.rect(screen, (80, 80, 80), (0, scr_h - fight_h, fight_w, fight_h))
        pg.draw.rect(screen, (0, 0, 0), (150, scr_h - fight_h, fight_w, fight_h))
        pg.draw.rect(screen, (80, 80, 80), (300, scr_h - fight_h, fight_w, fight_h))
        pg.draw.rect(screen, (0, 0, 0), (450, scr_h - fight_h, fight_w, fight_h))
        for i, char in enumerate(char_img):
            char = pg.transform.scale(char, (fight_w, fight_h - 50))
            screen.blit(char, (150 * i, scr_h - fight_h))
        screen.blit(char1_r, char1_Rect)
        screen.blit(char2_r, char2_Rect)
        screen.blit(char3_r, char3_Rect)
        screen.blit(char4_r, char4_Rect)
        hp()
    
    pg.display.update()

    running = True
    while running:
        clock.tick(30)
        left_click = pg.mouse.get_pressed()[0] # 點擊滑鼠左鍵
        right_click = pg.mouse.get_pressed()[2] # 點擊滑鼠右鍵
        pos = pg.mouse.get_pos()
        player = True
        battle = False
        second_target = False
        
        if enemy_hp > 0 and bt_hp.count(0) != 4 and round_count > 0:
            battle = True       
                         
        for event in pg.event.get():
            # 退出遊戲
            if event.type == pg.QUIT:
                running = False

            # 點擊右鍵角色區塊
            if battle and event.type == pg.MOUSEBUTTONUP and right_click:
                if player and rect_char1.collidepoint(pos):
                    note = char_attack_note[0]
                elif player and rect_char2.collidepoint(pos):
                    note = char_attack_note[1]
                elif player and rect_char3.collidepoint(pos):
                    note = char_attack_note[2]
                elif player and rect_char4.collidepoint(pos):
                    note = char_attack_note[3]
                else:
                    break
                note_text(note)
                pg.display.update()

            # 點擊角色區塊
            if battle and event.type == pg.MOUSEBUTTONUP and left_click:
                if player and rect_char1.collidepoint(pos):
                    crit_status, atk = attack(bt_name[0])
                    if bt_hp[0] == 0:
                        atk = 0
                        status_text = bt_name[0] + " 已經無法戰鬥"
                    else:
                        if crit_status == True:
                            status_text = bt_name[0] + " 爆擊 造成 " + str(atk) + " 的傷害"
                        else:
                            status_text = bt_name[0] + " 攻擊 造成 " + str(atk) + " 的傷害"
                        player = False
                    status_update(status_text)
                elif player and rect_char2.collidepoint(pos):
                    crit_status, atk = attack(bt_name[1])
                    if bt_hp[1] == 0:
                        atk = 0
                        status_text = bt_name[1] + " 已經無法戰鬥"
                    else:
                        if crit_status == True:
                            status_text = bt_name[1] + " 爆擊 造成 " + str(atk) + " 的傷害"
                        else:
                            status_text = bt_name[1] + " 攻擊 造成 " + str(atk) + " 的傷害"
                        player = False
                    status_update(status_text)
                elif player and rect_char3.collidepoint(pos):
                    crit_status, atk = attack(bt_name[2])
                    if bt_hp[2] == 0:
                        atk = 0
                        status_text = bt_name[2] + " 已經無法戰鬥"
                    else:
                        if crit_status == True:
                            status_text = bt_name[2] + " 爆擊 造成 " + str(atk) + " 的傷害"
                        else:
                            status_text = bt_name[2] + " 攻擊 造成 " + str(atk) + " 的傷害"
                        player = False
                    status_update(status_text)
                elif player and rect_char4.collidepoint(pos):
                    crit_status, atk = attack(bt_name[3])
                    if bt_hp[3] == 0:
                        atk = 0
                        status_text = bt_name[3] + " 已經無法戰鬥"
                    else:
                        if crit_status == True:
                            status_text = bt_name[3] + " 爆擊 造成 " + str(atk) + " 的傷害"
                        else:
                            status_text = bt_name[3] + " 攻擊 造成 " + str(atk) + " 的傷害"   
                        player = False
                    status_update(status_text)
                else:
                    break
                
                # 成功攻擊敵人時產生音效
                if player == False:
                    sound = pg.mixer.Sound("audio\\sword_sfx.wav")
                    sound.play()               

                # 敵人血量更新
                if enemy_hp <= atk:
                    enemy_hp = 0
                else:
                    enemy_hp -= atk
                hp_enemy.hp = enemy_hp
                hp_enemy.draw(screen)
                pg.display.update()
                pg.time.delay(600)

                # 設定敵人攻擊    
                if player == False and enemy_hp > 0:
                    enemy_atk = rd.randint(30, 150)
                    while enemy_atk:
                        target = rd.choice(bt_hp)
                        i = bt_hp.index(target)
                        if bt_hp[i] == 0:
                            continue
                        else:
                            status_text = bt_name[i] + " 受到敵人 " + str(enemy_atk) + " 的傷害"
                            status_update(status_text)
                            sound = pg.mixer.Sound("audio\\hit06.flac")
                            sound.play()
                            sound.set_volume(0.2)
                            # 更新角色區塊 呈現角色受到傷害的效果
                            pg.time.delay(50)
                            damage_layer = pg.draw.rect(screen, (120, 0, 0), (i * 150, scr_h - fight_h, fight_w, fight_h))
                            pg.display.update()
                            pg.time.delay(50)
                            refresh_char()
                            break
                            
                    # 玩家角色死亡判定
                    if target - enemy_atk <= 0 and target != 0:
                        bt_hp[i] = 0
                        status_text = bt_name[i] + " 無法戰鬥"
                        status_update(status_text)
                        sound = pg.mixer.Sound("audio\\01._damage_grunt_male.wav")
                        sound.play()
                        sound.set_volume(0.2)
                        round_count -= 1
                    else:
                        bt_hp[i] -= enemy_atk
                        round_count -= 1

                    # 敵人有30%機率攻擊第二次
                    second_attack = rd.randint(1, 10)
                    if second_attack >= 8 and bt_hp.count(0) != 4:
                        pg.time.delay(100)
                        enemy_atk = rd.randint(40, 100)
                        second_target = True
                        while enemy_atk:
                            target = rd.choice(bt_hp)
                            i = bt_hp.index(target)
                            if bt_hp[i] == 0:
                                continue
                            else:
                                status_text = "敵人發動二次攻擊"
                                status_update(status_text)
                                status_text = bt_name[i] + " 受到敵人 " + str(enemy_atk) + " 的傷害"
                                status_update(status_text)
                                sound = pg.mixer.Sound("audio\\hit10.flac")
                                sound.play()
                                sound.set_volume(0.2)
                                # 更新角色區塊 呈現角色受到傷害的效果
                                pg.time.delay(50)
                                damage_layer = pg.draw.rect(screen, (120, 0, 0), (i * 150, scr_h - fight_h, fight_w, fight_h))
                                pg.display.update()
                                pg.time.delay(50)
                                refresh_char()
                                break
                            
                    # 玩家角色死亡判定2
                    if second_target:
                        if target - enemy_atk <= 0 and target != 0:
                            bt_hp[i] = 0
                            status_text = bt_name[i] + " 無法戰鬥"
                            status_update(status_text)
                            sound = pg.mixer.Sound("audio\\01._damage_grunt_male.wav")
                            sound.play()
                            sound.set_volume(0.2)
                        else:
                            bt_hp[i] -= enemy_atk

                    second_target = False
                    player = True
                    
                # 回合數、角色血量更新
                round()
                hp()
    
        # 呈現陣亡角色
        if battle == True:
            h = 10
            if bt_hp[0] == 0:
                char1_r = char_font.render(bt_name[0], True, (255, 0, 0))
                screen.blit(char1_r, char1_Rect)
                pg.draw.rect(screen, (80, 80, 80), (0, scr_h - h, fight_w, h))
            if bt_hp[1] == 0:
                char2_r = char_font.render(bt_name[1], True, (255, 0, 0))
                screen.blit(char2_r, char2_Rect)
                pg.draw.rect(screen, (0, 0, 0), (150, scr_h - h, fight_w, h))
            if bt_hp[2] == 0:
                char3_r = char_font.render(bt_name[2], True, (255, 0, 0))
                screen.blit(char3_r, char3_Rect)
                pg.draw.rect(screen, (80, 80, 80), (300, scr_h - h, fight_w, h))
            if bt_hp[3] == 0:
                char4_r = char_font.render(bt_name[3], True, (255, 0, 0))
                screen.blit(char4_r, char4_Rect)
                pg.draw.rect(screen, (0, 0, 0), (450, scr_h - h, fight_w, h))

        # 畫面重整更新
        pg.display.update()

        # 戰鬥結果判定
        if enemy_hp == 0 and bt_hp.count(0) != 4:
            battle = False
            win()
        elif bt_hp.count(0) == 4 or round_count == 0:
            battle = False
            lose()
        else:
            pass
    
    pg.quit()
    exit()

if __name__ == '__main__':    
    main()
    
