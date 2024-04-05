import os
import random

import pygame.image

from util import *
from bloon import Balloon
from tower import Tower
from life_management import Life
from ice import Ice
from constants import *

# Game Klasse
class Game:
    def __init__(self):
        # Pygame initialisieren
        pygame.init()

        # Fenstergröße und Titel festlegen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.balloons = []
        # Farben und Schrift
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)

        self.stat_font = pygame.font.Font(None, 22)
        # Background
        self.bg_image = load_image("images/background_image.png", (self.screen_width, self.screen_height))

        # Load heart images
        self.heart_full = load_image("images/heart_full.png", (30, 30))
        self.heart_empty = load_image("images/heart_empty.png", (30, 30))

        # Stats
        self.atk_rt_icn = load_image("images/atk_rate.png", (80, 80))
        self.atk_spd_icn = load_image("images/atk_speed.png", (80, 80))

        # Initialisierungen
        self.balloon_size = (50, 50)
        self.tower = Tower(400, 300, get_asset_path("images/tower_image.png"), (50, 50), 250, 1)  # Beispiel-Turm
        self.projectiles = []
        self.score = 2000
        self.life = Life(6, self.heart_full, self.heart_empty, self)
        self.path = [(0, 300), (200, 300), (200, 100), (600, 100), (600, 500), (800, 500)]
        self.ice_original = pygame.image.load(get_asset_path("images/ice1.png"))
        self.ice_icon = pygame.transform.scale(self.ice_original, (120, 120))
        self.ice = Ice(self.ice_original, self)
    def run(self):

        pygame.mixer.music.load(get_asset_path('sounds/bg-music.mp3'))
        pygame.mixer.music.play(-1, 0.0)
        pop_sound = pygame.mixer.Sound(get_asset_path("sounds/pop.ogg"))
        coin = Coin(self.screen)
        # Stats
        icon_x = self.screen_width - 90
        atk_r_pos = (icon_x, 100)
        atk_s_pos = (icon_x, 200)
        atk_r_rect = self.atk_spd_icn.get_rect()
        atk_r_rect.topleft = atk_r_pos
        atk_s_rect = self.atk_spd_icn.get_rect()
        atk_s_rect.topleft = atk_s_pos
        ice_pos = (icon_x - 20, 300)
        ice_rect = self.ice_icon.get_rect()
        ice_rect.topleft = ice_pos

        # Spiel-Schleife
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if atk_r_rect.collidepoint(pos) and self.score >= 20:
                        if self.score >= 20:
                            self.score -= 20
                            if self.tower.shoot_cooldown >= 2:
                                self.tower.shoot_cooldown -= 5
                    if atk_s_rect.collidepoint(pos):
                        self.score -= 15
                        if self.tower.projectile_speed <= 100:
                            self.tower.projectile_speed += 5
                    if ice_rect.collidepoint(pos) and self.score >= 100:
                        self.score -= 100
                        self.ice.visible = True
                        self.ice.reset()  # Setzt die Eis-Grafik zurück

            # Ballons erzeugen
            if random.randint(1, 500) == 1:
                new_balloon = Balloon(self.path, "images/balloon_image.png", self.score, self.balloon_size)
                self.balloons.append(new_balloon)

            # Ballons bewegen
            for bloon in self.balloons:
                upd_bloon = bloon.update(self.screen, self.projectiles)
                if upd_bloon:
                    self.balloons.remove(bloon)
                    if upd_bloon[1]:
                        self.life.value -= 1
                    else:
                        self.score += 1
                        pop_sound.play()

            update_tower(self)
            # Projektile bewegen und zeichnen
            update_projectile(self)

            if self.ice.visible:
                print("show ice")
                self.ice.cast()
                self.screen.blit(self.ice.image, self.ice.rect.topleft)

            # Punktzahl anzeigen
            score_text = self.font.render(f": {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (45, 10))
            # Leben anzeigen
            life_text = self.font.render(f"Life:", True, pygame.Color(252, 3, 98))
            self.screen.blit(life_text, (120, 10))
            self.life.update()
            self.life.draw()
            coin.update()

            # Stats
            # self.screen.fill(self.WHITE, atk_rect)
            self.screen.blit(self.atk_rt_icn, atk_r_pos)
            life_text = self.stat_font.render(f"atk rate: {100 - self.tower.shoot_cooldown}", True,
                                              pygame.Color(252, 3, 98))
            self.screen.blit(life_text, (self.screen_width - 115, 180))

            self.screen.blit(self.atk_spd_icn, atk_s_pos)
            life_text = self.stat_font.render(f"atk speed: {self.tower.projectile_speed}%", True,
                                              pygame.Color(252, 3, 98))
            self.screen.blit(life_text, (self.screen_width - 115, 280))

            self.screen.blit(self.ice_icon, ice_pos)
            life_text = self.stat_font.render(f"Freeze (skill)", True,
                                              pygame.Color(252, 3, 98))
            self.screen.blit(life_text, (self.screen_width - 100, 400))

            pygame.display.update()


class Coin:
    def __init__(self, screen):
        self.screen = screen
        self.images = [load_image(f"images/star_coin/star_coin_rotate/star_coin_{i}.png", (35, 35)) for i in range(1, 7)]
        self.idx = 0

    def update(self):
        self.screen.blit(self.images[self.idx], (10, 4))
        if 0 <= pygame.time.get_ticks() % 32 < 1:
            self.idx = (self.idx + 1) % (len(self.images))


Game().run()
pygame.quit()
