import pygame as pg
import constantes as cons
import math
import random
import os

class GameObject(pg.sprite.Sprite):
    def __init__(self, image_path, width, height, posx, posy, speed):
        super().__init__()
        try:
            self.original_image = pg.image.load(image_path).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (width, height))
        except:
            self.original_image = pg.Surface((width, height))
            self.original_image.fill((255, 0, 255))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(posx, posy))
        self.pos = pg.math.Vector2(posx, posy)
        self.speed = speed

class Player(GameObject):
    def __init__(self, image, width, height, posx, posy, speed):
        super().__init__(image, width, height, posx, posy, speed)
        self.facing_dir = pg.math.Vector2(0, -1)
        self.angle, self.last_hit_time = 0, 0
        self.is_charging, self.charge_start_time = False, 0
        self.has_shield = False

    def update(self):
        keys = pg.key.get_pressed()
        move = pg.math.Vector2(0, 0)
        if keys[pg.K_LEFT] or keys[pg.K_a]: move.x = -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]: move.x = 1
        if keys[pg.K_UP] or keys[pg.K_w]: move.y = -1
        if keys[pg.K_DOWN] or keys[pg.K_s]: move.y = 1
        
        if move.magnitude() > 0:
            self.pos += move.normalize() * self.speed

        mouse_pos = pg.mouse.get_pos()
        target_dir = pg.math.Vector2(mouse_pos) - self.pos
        if target_dir.magnitude() > 0:
            self.facing_dir = self.facing_dir.lerp(target_dir.normalize(), 0.2)
            self.angle = math.degrees(math.atan2(-self.facing_dir.y, self.facing_dir.x)) - 90

        now = pg.time.get_ticks()
        self.image = pg.transform.rotate(self.original_image, self.angle)
        
        if self.is_charging and now - self.charge_start_time >= 1000:
            self.image.fill((255, 255, 0, 100), special_flags=pg.BLEND_ADD)
        
        if self.has_shield:
            pg.draw.circle(self.image, (0, 255, 255), (self.image.get_width()//2, self.image.get_height()//2), 40, 4)

        self.image.set_alpha(128 if (now - self.last_hit_time < 1500 and (now // 100) % 2 == 0) else 255)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        
        sw, sh = pg.display.get_surface().get_size()
        self.pos.x = max(40, min(self.pos.x, sw - 40))
        self.pos.y = max(40, min(self.pos.y, sh - 40))

class Enemy(GameObject):
    def __init__(self, image, width, height, posx, posy, speed, tipo):
        super().__init__(image, width, height, posx, posy, speed)
        self.tipo = tipo
        self.frozen_until = 0
        self.hit_flash_until = 0
        self.offset_x = random.uniform(0, 100)
        self.amplitude = random.uniform(0.3, 0.6)
        self.salud = 30 if tipo == "comun" else 20

    def update(self):
        now = pg.time.get_ticks()
        if now < self.frozen_until:
            temp_img = self.original_image.copy()
            temp_img.fill((0, 100, 255, 150), special_flags=pg.BLEND_ADD)
            self.image = temp_img
            return 
        self.rect.y += self.speed
        self.rect.x += math.sin(now * 0.005 + self.offset_x) * self.amplitude
        self.pos.y, self.pos.x = self.rect.centery, self.rect.centerx
        if now < self.hit_flash_until:
            temp_img = self.original_image.copy()
            temp_img.fill((255, 0, 0, 180), special_flags=pg.BLEND_ADD)
            self.image = temp_img
        else:
            self.image = self.original_image

class Boss(GameObject):
    def __init__(self, image, width, height, posx, posy, speed, vida):
        self.base_speed = speed - 2.0 
        super().__init__(image, width, height, posx, 130, self.base_speed)
        self.vida, self.max_vida, self.state = vida, vida, "NORMAL"
        self.timer_mov, self.last_dash_time = 0, pg.time.get_ticks()
        self.last_shot = 0
        self.dash_target = pg.math.Vector2(0,0)
        self.snd_dash = pg.mixer.Sound("sounds/boss_enojado.mp3") if os.path.exists("sounds/boss_enojado.mp3") else None
        self.dash_just_started = False

    def update(self, attacks_group, player_pos):
        now = pg.time.get_ticks()
        sw = pg.display.get_surface().get_width()
        if self.state == "DASH":
            dir_v = (self.dash_target - self.pos)
            if dir_v.magnitude() > 10: 
                self.pos += dir_v.normalize() * (self.base_speed * 6.5)
            else:
                self.state, self.last_dash_time = "NORMAL", now
        else: 
            self.timer_mov += 0.028
            self.pos.x = (sw // 2) + math.sin(self.timer_mov) * (sw // 3)
            self.pos.y = 130 + math.sin(self.timer_mov * 0.8) * 50
            if now - self.last_dash_time > 8000:
                self.state = "DASH"
                self.dash_target = pg.math.Vector2(player_pos)
                self.dash_just_started = True
                if self.snd_dash: self.snd_dash.play()
        self.rect.center = self.pos
        if self.state != "DASH" and now - self.last_shot > 1300:
            attacks_group.add(BossAttack(cons.img_bone, 40, 50, self.rect.centerx, self.rect.centery, 7, player_pos))
            self.last_shot = now

class Bullet(GameObject):
    def __init__(self, image, width, height, posx, posy, speed, direction, angle, damage, pierce=False):
        super().__init__(image, width, height, posx, posy, speed)
        self.dir = direction.copy()
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(posx, posy))
        self.damage = damage
        self.pierce = pierce
        self.targets_hit = [] # Almacena quién ya fue golpeado por esta bala

    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = self.pos
        if not pg.display.get_surface().get_rect().colliderect(self.rect): self.kill()

class BossAttack(GameObject):
    def __init__(self, image, width, height, posx, posy, speed, target_pos):
        super().__init__(image, width, height, posx, posy, speed)
        direction = pg.math.Vector2(target_pos) - pg.math.Vector2(posx, posy)
        self.dir = direction.normalize() if direction.magnitude() > 0 else pg.math.Vector2(0, 1)

    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = self.pos
        if not pg.display.get_surface().get_rect().colliderect(self.rect): self.kill()

class Item(GameObject):
    def __init__(self, image_path, width, height, posx, posy, tipo="heal"):
        super().__init__(image_path, width, height, posx, posy, 0)
        self.tipo, self.spawn_time = tipo, pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > 8000: self.kill()

class FreezeBlast(GameObject):
    def __init__(self, posx, posy, direction):
        super().__init__(cons.iceball, 40, 40, posx, posy, 14)
        self.dir = direction.copy()

    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = self.pos
        if not pg.display.get_surface().get_rect().colliderect(self.rect): self.kill()

class Particle(pg.sprite.Sprite):
    def __init__(self, posx, posy, color):
        super().__init__()
        size = random.randint(2, 5)
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(posx, posy))
        self.pos = pg.math.Vector2(posx, posy)
        self.vel = pg.math.Vector2(random.uniform(-4, 4), random.uniform(-4, 4))
        self.life = 255

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        self.life -= 8
        if self.life <= 0: self.kill()
        else: self.image.set_alpha(self.life)

class Barrel(GameObject):
    def __init__(self, image_path, width, height, posx, posy, speed):
        super().__init__(image_path, width, height, posx, posy, speed)
        self.health = 1

    def update(self):
        self.rect.y += self.speed
        self.pos.y = self.rect.centery
        if self.rect.top > 800: self.kill()
