import pygame as pg
import constantes as cons
from objetos import Player, Enemy, Bullet, Boss, BossAttack, Particle, Item, FreezeBlast, Barrel
import os
import random
from random import randint
import math
import sys
import cv2  # NEW: Importación necesaria para el video

def resource_path(relative_path):
    """ Obtiene la ruta absoluta para que funcione en el .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configuración de ruta base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# --- INICIALIZACIÓN Y CONFIGURACIÓN ---
pg.mixer.init()
settings = {"vol_mus": 0.5, "vol_snd": 0.5, "lang": "ES"}
VOL_BASE = 0.7 

def load_highscore():
    try:
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
    except: pass
    return 0

def save_highscore(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except: pass

texts = {
    "ES": {
        "settings": "AJUSTES", "music": "Música", "sound": "Sonido", "lang_label": "Idioma",
        "save": "GUARDAR", "play": "JUGAR", "continue": "CONTINUAR", "exit": "SALIR",
        "credits": "CRÉDITOS", "credits_msg": "Proyecto Zomshot, hecho por ashlyrgg. Espero que te guste!",
        "how_to_play": "CÓMO JUGAR",
        "controls": [
            "WASD / Flechas: Moverse", "Click Izquierdo: Disparar", "Click Derecho (Mantener): Disparo Cargado",
            "Tecla Q: Escudo (40s)", "Tecla E: Ráfaga de Hielo (con item)", "Shift Izquierdo: Triple Disparo (50s)",
            "Tecla R: Reiniciar al morir/ganar"
        ],
        "level": "NIVEL", "lives": "VIDAS", "record": "PUNTOS", "high_record": "RÉCORD",
        "total_points": "PUNTOS TOTALES", "gameover_txt": ":( R para reiniciar", "victory_txt": ":) R para reiniciar",
        "incoming_boss": "¡ALGO SE APROXIMA!", "resist": "QUEDAN POCOS ZOMBIES, ¡RESISTE!"
    },
    "EN": {
        "settings": "SETTINGS", "music": "Music", "sound": "Sound", "lang_label": "Language",
        "save": "SAVE", "play": "PLAY", "continue": "CONTINUE", "exit": "EXIT",
        "credits": "CREDITS", "credits_msg": "Project Zomshot, made by ashlyrgg. Hope you like it!",
        "how_to_play": "HOW TO PLAY",
        "controls": [
            "WASD / Arrows: Move", "Left Click: Shoot", "Right Click (Hold): Charged Shot",
            "Q Key: Shield (40s)", "E Key: Ice Blast (with item)", "Left Shift: Triple Shot (50s)",
            "R Key: Restart on Win/Loss"
        ],
        "level": "LEVEL", "lives": "LIVES", "record": "SCORE", "high_record": "HIGH SCORE",
        "total_points": "TOTAL SCORE", "gameover_txt": ":( R to restart", "victory_txt": ":) R to restart",
        "incoming_boss": "SOMETHING IS APPROACHING!", "resist": "FEW ZOMBIES LEFT, RESIST!"
    }
}

def get_sound(path):
    return pg.mixer.Sound(path) if os.path.exists(path) else None

snd_shot = get_sound("sounds/disparo.mp3")
snd_death = [get_sound("sounds/shouting.mp3"), get_sound("sounds/shouting2.mp3")]
snd_victory = get_sound("sounds/victory_sound.mp3")
snd_gameover = get_sound("sounds/gameover_sound.mp3")
snd_menu = get_sound("sounds/menu.mp3")

menu_channel = pg.mixer.Channel(2)

def play_music(path):
    if path and os.path.exists(path):
        pg.mixer.music.load(path)
        pg.mixer.music.set_volume(settings["vol_mus"] * VOL_BASE)
        pg.mixer.music.play(-1)
    else: pg.mixer.music.stop()

def draw_text(win, text, size, x, y, color=(255,255,255), center=True):
    font = pg.font.SysFont("Arial", size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y)) if center else render.get_rect(topleft=(x, y))
    win.blit(render, rect)
    return rect

def show_how_to_play(Window):
    while True:
        W, H = Window.get_size(); lang = settings["lang"]
        try: bg = pg.transform.scale(pg.image.load("images/menu_background.png").convert(), (W, H))
        except: bg = pg.Surface((W, H)); bg.fill((20, 20, 20))
        Window.blit(bg, (0,0))
        draw_text(Window, texts[lang]["how_to_play"], 50, W//2, 80)
        y_offset = 180
        for line in texts[lang]["controls"]:
            draw_text(Window, line, 25, W//2, y_offset); y_offset += 40
        btn_back = draw_text(Window, texts[lang]["save"], 35, W//2, 520, (0,255,0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT: return "QUIT"
            if event.type == pg.MOUSEBUTTONDOWN and btn_back.collidepoint(event.pos): return

def show_credits(Window):
    while True:
        W, H = Window.get_size(); lang = settings["lang"]
        try: bg = pg.transform.scale(pg.image.load("images/menu_background.png").convert(), (W, H))
        except: bg = pg.Surface((W, H)); bg.fill((20, 20, 20))
        Window.blit(bg, (0,0))
        draw_text(Window, texts[lang]["credits"], 50, W//2, 100)
        draw_text(Window, texts[lang]["credits_msg"], 25, W//2, H//2)
        btn_back = draw_text(Window, texts[lang]["save"], 35, W//2, 500, (0,255,0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT: return "QUIT"
            if event.type == pg.MOUSEBUTTONDOWN and btn_back.collidepoint(event.pos): return

def show_settings(Window):
    while True:
        W, H = Window.get_size(); lang = settings["lang"]
        try: bg = pg.transform.scale(pg.image.load("images/menu_background.png").convert(), (W, H))
        except: bg = pg.Surface((W, H)); bg.fill((20, 20, 20))
        Window.blit(bg, (0,0))
        draw_text(Window, texts[lang]["settings"], 50, W//2, 100)
        
        btn_mus_up = draw_text(Window, "+", 40, W//2 + 120, 200)
        btn_mus_dn = draw_text(Window, "-", 40, W//2 - 120, 200)
        draw_text(Window, f"{texts[lang]['music']}: {int(settings['vol_mus']*100)}%", 30, W//2, 200)
        
        btn_snd_up = draw_text(Window, "+", 40, W//2 + 120, 300)
        btn_snd_dn = draw_text(Window, "-", 40, W//2 - 120, 300)
        draw_text(Window, f"{texts[lang]['sound']}: {int(settings['vol_snd']*100)}%", 30, W//2, 300)
        
        btn_lang = draw_text(Window, f"{texts[lang]['lang_label']}: {lang}", 30, W//2, 400)
        btn_back = draw_text(Window, texts[lang]["save"], 35, W//2, 500, (0,255,0))
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT: return "QUIT"
            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_mus_up.collidepoint(event.pos): 
                    settings["vol_mus"] = min(1.0, settings["vol_mus"] + 0.1)
                    pg.mixer.music.set_volume(settings["vol_mus"] * VOL_BASE)
                    menu_channel.set_volume(settings["vol_mus"] * VOL_BASE)
                if btn_mus_dn.collidepoint(event.pos): 
                    settings["vol_mus"] = max(0.0, settings["vol_mus"] - 0.1)
                    pg.mixer.music.set_volume(settings["vol_mus"] * VOL_BASE)
                    menu_channel.set_volume(settings["vol_mus"] * VOL_BASE)
                if btn_snd_up.collidepoint(event.pos): 
                    settings["vol_snd"] = min(1.0, settings["vol_snd"] + 0.1)
                if btn_snd_dn.collidepoint(event.pos): 
                    settings["vol_snd"] = max(0.0, settings["vol_snd"] - 0.1)
                if btn_lang.collidepoint(event.pos): settings["lang"] = "EN" if settings["lang"] == "ES" else "ES"
                if btn_back.collidepoint(event.pos): return

def show_menu(Window, is_pause=False):
    if is_pause: pg.mixer.music.pause()
    else: pg.mixer.music.stop() 

    try:
        menu_icon = pg.image.load("images/menu_icon.png").convert_alpha()
        menu_icon = pg.transform.scale(menu_icon, (700, 550))
    except:
        menu_icon = None

    if snd_menu and not menu_channel.get_busy():
        menu_channel.set_volume(settings["vol_mus"] * VOL_BASE)
        menu_channel.play(snd_menu, loops=-1)

    while True:
        W, H = Window.get_size(); lang = settings["lang"]
        if is_pause: 
            bg = pg.Surface((W, H), pg.SRCALPHA); bg.fill((0,0,0,180))
        else:
            try: bg = pg.transform.scale(pg.image.load("images/menu_background.png").convert(), (W, H))
            except: bg = pg.Surface((W, H)); bg.fill((20, 20, 20))
        
        Window.blit(bg, (0,0))

        if menu_icon and not is_pause:
            bobbing = math.sin(pg.time.get_ticks() * 0.005) * 8
            icon_rect = menu_icon.get_rect(center=(W // 2, 110 + int(bobbing)))
            Window.blit(menu_icon, icon_rect)

        btn_play = draw_text(Window, texts[lang]["continue"] if is_pause else texts[lang]["play"], 50, W//2, H//2 - 140)
        btn_sets = draw_text(Window, texts[lang]["settings"], 40, W//2, H//2 - 60)
        btn_how  = draw_text(Window, texts[lang]["how_to_play"], 40, W//2, H//2 + 10)
        btn_cred = draw_text(Window, texts[lang]["credits"], 40, W//2, H//2 + 80)
        btn_exit = draw_text(Window, texts[lang]["exit"], 40, W//2, H//2 + 160, (200, 0, 0))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                menu_channel.stop()
                return "QUIT"
            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos): 
                    menu_channel.stop()
                    if is_pause: pg.mixer.music.unpause()
                    return "START"
                if btn_sets.collidepoint(event.pos): 
                    if show_settings(Window) == "QUIT": 
                        menu_channel.stop()
                        return "QUIT"
                if btn_how.collidepoint(event.pos):
                    if show_how_to_play(Window) == "QUIT": 
                        menu_channel.stop()
                        return "QUIT"
                if btn_cred.collidepoint(event.pos):
                    if show_credits(Window) == "QUIT": 
                        menu_channel.stop()
                        return "QUIT"
                if btn_exit.collidepoint(event.pos): 
                    menu_channel.stop()
                    return "QUIT"

def game_loop():
    pg.init()
    pg.display.set_caption("Zomshot")
    try: pg.display.set_icon(pg.image.load("images/icon.png"))
    except: pass
    Window = pg.display.set_mode((cons.Width_Window, cons.Height_Window), pg.RESIZABLE)
    boss_channel = pg.mixer.Channel(1)
    highscore = load_highscore()
    
    # NEW: Carga del video de victoria
    video_path = "images/victory.mp4"
    cap = cv2.VideoCapture(video_path) if os.path.exists(video_path) else None

    while True:
        if show_menu(Window) == "QUIT": break
        
        play_music("sounds/background.mp3")
        clock = pg.time.Clock()
        
        shake_amount = 0 
        barrels = pg.sprite.Group()
        score, lost, current_level = 0, 0, 1
        game_state = "PLAYING"
        powerup_until, boss_defeated_at = 0, 0
        boss_active, played_final_sound = False, False
        combo_count, last_kill_time = 0, 0
        last_shield_use, last_multi_use = -40000, -50000 
        multi_shot_until = 0
        game_start = pg.time.get_ticks()
        last_level_time = game_start

        try:
            img_menu_btn = pg.transform.scale(pg.image.load("images/gameplay_menu.png").convert_alpha(), (60, 60))
            img_pwr_shift = pg.transform.scale(pg.image.load("images/triple_bullet.png").convert_alpha(), (60, 60))
            img_pwr_q = pg.transform.scale(pg.image.load("images/shield.png").convert_alpha(), (60, 60))
            img_pwr_e = pg.transform.scale(pg.image.load("images/iceball.png").convert_alpha(), (60, 60))
        except:
            img_menu_btn = pg.Surface((60,60)); img_menu_btn.fill((255,255,255))
            img_pwr_shift = pg.Surface((60,60)); img_pwr_q = pg.Surface((60,60)); img_pwr_e = pg.Surface((60,60))

        player = Player(cons.img_player, 90, 90, 400, 650, cons.speed_player)
        bullets, monsters, boss_attacks, particles, items, freeze_group = [pg.sprite.Group() for _ in range(6)]
        players_group, boss_group = pg.sprite.GroupSingle(player), pg.sprite.GroupSingle()
        
        running = True
        while running:
            now = pg.time.get_ticks()
            W, H = Window.get_size(); lang = settings["lang"]
            
            offset = pg.math.Vector2(0, 0)
            if shake_amount > 0:
                offset.x = random.uniform(-shake_amount, shake_amount)
                offset.y = random.uniform(-shake_amount, shake_amount)
                shake_amount *= 0.85 
                if shake_amount < 0.1: shake_amount = 0

            rect_menu = img_menu_btn.get_rect(topright=(W-10, 10))

            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    if cap: cap.release()
                    return "QUIT"
                if event.type == pg.MOUSEBUTTONDOWN and game_state == "PLAYING":
                    if rect_menu.collidepoint(event.pos):
                        if show_menu(Window, True) == "QUIT": running = False
                    if event.button == 1:
                        if snd_shot: 
                            snd_shot.set_volume(settings["vol_snd"] * VOL_BASE)
                            snd_shot.play()
                        if now < multi_shot_until:
                            for a in [-15, 0, 15]: bullets.add(Bullet(cons.img_disparo, 30, 30, player.pos.x, player.pos.y, 30, player.facing_dir.rotate(a), player.angle+a, 10))
                        else: bullets.add(Bullet(cons.img_disparo, 30, 30, player.pos.x, player.pos.y, 40, player.facing_dir, player.angle, 10))
                    if event.button == 3: player.is_charging, player.charge_start_time = True, now
                if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                    if player.is_charging and now - player.charge_start_time >= 1000:
                        bullets.add(Bullet(cons.img_disparo, 80, 80, player.pos.x, player.pos.y, 40, player.facing_dir, player.angle, 35, True))
                        shake_amount = 12
                    player.is_charging = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e and now < powerup_until: freeze_group.add(FreezeBlast(player.pos.x, player.pos.y, player.facing_dir))
                    if event.key == pg.K_q and now - last_shield_use >= 40000: 
                        player.has_shield = True; last_shield_use = now
                    if event.key == pg.K_LSHIFT and now - last_multi_use >= 50000: 
                        multi_shot_until = now + 10000; last_multi_use = now
                    # Al presionar R, salimos del bucle actual para volver al menú
                    if game_state != "PLAYING" and event.key == pg.K_r: running = False

            if game_state == "PLAYING":
                if not boss_active and random.random() < 0.006: 
                    barrels.add(Barrel("images/barrel.png", 80, 80, randint(50, W-50), -50, 4 + current_level * 0.3))

                if combo_count > 0 and now - last_kill_time > 7000: combo_count = 0
                if not boss_active and boss_defeated_at == 0 and now - last_level_time > 40000: current_level += 1; last_level_time = now
                
                limit = (3 + current_level) if boss_defeated_at == 0 else 2
                if not boss_active and len(monsters) < limit:
                    boost = 3.5 if boss_defeated_at > 0 else (current_level * 0.35)
                    if random.random() < 0.3: monsters.add(Enemy(cons.img_enemigo2, 100, 100, randint(50, W-50), -50, 2.7 + boost, "rapido"))
                    else: monsters.add(Enemy(cons.img_enemigo, 100, 100, randint(50, W-50), -50, 1.0 + boost, "comun"))

                if now - game_start > 90000 and not boss_active and boss_defeated_at == 0:
                    boss_active, boss = True, Boss(cons.img_boss, 190, 190, W//2, 150, 3.5, 780)
                    boss_group.add(boss); monsters.empty(); pg.mixer.music.pause()
                    shake_amount = 18
                    if get_sound("sounds/boss_music.mp3"): 
                        boss_channel.set_volume(settings["vol_mus"] * VOL_BASE)
                        boss_channel.play(get_sound("sounds/boss_music.mp3"), loops=-1)

                players_group.update(); bullets.update(); particles.update(); freeze_group.update(); items.update(); barrels.update(); monsters.update()

                for b in bullets:
                    hit_list = pg.sprite.spritecollide(b, barrels, True)
                    if hit_list:
                        shake_amount = 25
                        impact_pos = b.rect.center
                        b.kill()
                        for _ in range(25): particles.add(Particle(impact_pos[0], impact_pos[1], (255, 120, 0)))
                        for m in monsters:
                            dist = pg.math.Vector2(m.rect.center).distance_to(impact_pos)
                            if dist < 280:
                                m.salud -= 200
                                score += 25

                for blast in freeze_group:
                    hit_enemies = pg.sprite.spritecollide(blast, monsters, False)
                    for m in hit_enemies:
                        m.frozen_until = now + 4000
                        blast.kill()

                collected = pg.sprite.spritecollide(player, items, True)
                for item in collected:
                    if item.tipo == "heal": lost = max(0, lost - 1)
                    elif item.tipo == "ice": powerup_until = now + 30000

                for m in monsters:
                    if m.rect.top > H: 
                        lost += 1; combo_count = 0; m.kill()
                        if lost >= 5: game_state = "GAMEOVER"
                
                if boss_active: 
                    boss_group.update(boss_attacks, player.pos)
                    boss_attacks.update()
                    if boss.dash_just_started:
                        shake_amount = 25
                        boss.dash_just_started = False

                for b in bullets:
                    if boss_active and b.rect.colliderect(boss.rect):
                        if boss not in b.targets_hit:
                            boss.vida -= b.damage; shake_amount = 3
                            b.targets_hit.append(boss)
                            if boss.vida <= 0:
                                boss.kill(); boss_active, boss_defeated_at = False, now; score += 2000
                                items.add(Item(cons.iceball, 60, 60, boss.rect.centerx, boss.rect.centery, "ice"))
                                boss_channel.stop(); pg.mixer.music.unpause(); shake_amount = 30
                        if not b.pierce: b.kill()
                    
                    for m in pg.sprite.spritecollide(b, monsters, False):
                        if m not in b.targets_hit:
                            m.salud -= b.damage; m.rect.y -= 35; m.hit_flash_until = now + 150
                            b.targets_hit.append(m)
                            if m.salud <= 0:
                                combo_count += 1; last_kill_time = now; score += (20 * combo_count)
                                if score > highscore: highscore = score; save_highscore(highscore)
                                s = random.choice(snd_death)
                                if s: s.set_volume(settings["vol_snd"] * VOL_BASE); s.play()
                                for _ in range(6): particles.add(Particle(m.rect.centerx, m.rect.centery, (150,0,0)))
                                if random.random() < 0.15: items.add(Item(cons.img_botiquin, 50, 50, m.rect.centerx, m.rect.centery, "heal"))
                                m.kill()
                        if not b.pierce: b.kill()

                if pg.sprite.spritecollide(player, monsters, True) or pg.sprite.spritecollide(player, boss_attacks, True) or (boss_active and player.rect.colliderect(boss.rect)):
                    if player.has_shield: player.has_shield = False; player.last_hit_time = now; shake_amount = 10
                    elif now - player.last_hit_time > 1500:
                        lost += 1; combo_count = 0; player.last_hit_time = now; shake_amount = 15
                        if lost >= 5: game_state = "GAMEOVER"

                if boss_defeated_at > 0 and now - boss_defeated_at > 40000: game_state = "VICTORY"

            # --- RENDERIZADO FINAL ---
            if game_state == "VICTORY":
                # NEW: Manejo del Video de Fondo
                if cap is not None:
                    ret, frame = cap.read()
                    if not ret: # Si el video acaba, se reinicia (bucle)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, frame = cap.read()
                    
                    if ret:
                        # Convertir frame de OpenCV a superficie de Pygame
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = pg.surfarray.make_surface(frame.swapaxes(0, 1))
                        video_surf = pg.transform.scale(frame, (W, H))
                        Window.blit(video_surf, (0, 0))
                else:
                    Window.fill((0, 40, 0)) # Color verde oscuro si no hay video

                if not played_final_sound:
                    pg.mixer.music.stop() 
                    if snd_victory: snd_victory.set_volume(settings["vol_snd"] * VOL_BASE); snd_victory.play()
                    played_final_sound = True
                
                # Texto encima del video
                draw_text(Window, texts[lang]["victory_txt"], 50, W//2, H//2 - 50, (0,255,0))
                draw_text(Window, f"{texts[lang]['total_points']}: {score}", 35, W//2, H//2 + 30, (255, 255, 255))

            else:
                # Fondo normal para PLAYING y GAMEOVER
                try: 
                    bg_img = pg.image.load(cons.background).convert()
                    Window.blit(pg.transform.scale(bg_img, (W+60, H+60)), (-30 + offset.x, -30 + offset.y))
                except: Window.fill((30,30,30))

                for grp in [monsters, items, bullets, particles, players_group, boss_group, boss_attacks, freeze_group, barrels]:
                    for sprite in grp:
                        Window.blit(sprite.image, (sprite.rect.x + offset.x, sprite.rect.y + offset.y))
                
                if game_state == "PLAYING":
                    if boss_active: pg.draw.rect(Window, (255, 0, 0), (boss.rect.x + offset.x, boss.rect.y-20 + offset.y, boss.rect.width * (boss.vida/boss.max_vida), 10))
                    Window.blit(img_menu_btn, rect_menu)
                    draw_text(Window, f"{texts[lang]['level']} {current_level} | {texts[lang]['lives']}: {5-lost} | {texts[lang]['record']}: {score} | {texts[lang]['high_record']}: {highscore}", 25, 20, 20, (255,255,255), False)
                    if combo_count > 1: draw_text(Window, f"COMBO X{combo_count}", 35, W//2, 70, (255, 255, 0))
                    
                    if 80000 < (now - game_start) < 90000:
                        if (now // 500) % 2 == 0: draw_text(Window, texts[lang]["incoming_boss"], 45, W//2, H//2 - 100, (255, 50, 50))
                    if boss_defeated_at > 0:
                        t_win = 40000 - (now - boss_defeated_at)
                        if 0 < t_win <= 20000: draw_text(Window, f"{texts[lang]['resist']} ({t_win//1000}s)", 30, W//2, H//2 + 150, (255, 255, 0))
                    
                    # UIs de Cooldowns
                    cd_m = max(0, (last_multi_use + 50000 - now) // 1000)
                    Window.blit(img_pwr_shift, (W - 180, H - 60))
                    if cd_m > 0: 
                        draw_text(Window, str(cd_m), 20, W - 160, H - 85, (200, 200, 200))
                        s = pg.Surface((60, 60), pg.SRCALPHA); s.fill((0,0,0,160)); Window.blit(s, (W-180, H-60))
                    cd_s = max(0, (last_shield_use + 40000 - now) // 1000)
                    Window.blit(img_pwr_q, (W - 120, H - 60))
                    if cd_s > 0:
                        draw_text(Window, str(cd_s), 20, W - 100, H - 85, (200, 200, 200))
                        s = pg.Surface((60, 60), pg.SRCALPHA); s.fill((0,0,0,160)); Window.blit(s, (W-120, H-60))
                    Window.blit(img_pwr_e, (W - 60, H - 60))
                    if now < powerup_until: draw_text(Window, str((powerup_until - now) // 1000), 20, W - 40, H - 85, (0, 255, 255))
                    else: s = pg.Surface((60, 60), pg.SRCALPHA); s.fill((0,0,0,200)); Window.blit(s, (W-60, H-60))

                elif game_state == "GAMEOVER":
                    if not played_final_sound:
                        boss_channel.stop(); pg.mixer.music.stop() 
                        if snd_gameover: snd_gameover.set_volume(settings["vol_snd"] * VOL_BASE); snd_gameover.play()
                        played_final_sound = True
                    draw_text(Window, texts[lang]["gameover_txt"], 50, W//2, H//2 - 50, (255,0,0))
                    draw_text(Window, f"{texts[lang]['total_points']}: {score}", 35, W//2, H//2 + 30, (255, 255, 255))
                
            pg.display.flip(); clock.tick(60)
            
    # NEW: Liberar recursos de OpenCV al cerrar
    if cap: cap.release()
    pg.quit()

if __name__ == "__main__": game_loop()