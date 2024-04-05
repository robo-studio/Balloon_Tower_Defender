import os
import random
import pygame
from util import *
from bloon import Balloon
from tower import Tower
from life_management import Life
from ice import Ice
from constants import *  # Importiere die Konstanten
from coin import Coin
from sounds import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_width = SCREEN_WIDTH #neu
        self.screen_height = SCREEN_HEIGHT #neu
        self.clock = pygame.time.Clock()
        self.balloons = []
        self.font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.stat_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.bg_image = load_image("images/background_image.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.heart_full = load_image("images/heart_full.png", HEART_SIZE)
        self.heart_empty = load_image("images/heart_empty.png", HEART_SIZE)
        self.atk_rt_icn = load_image("images/atk_rate.png", ATK_ICON_SIZE)
        self.atk_spd_icn = load_image("images/atk_speed.png", ATK_ICON_SIZE)
        self.tower = Tower(400, 300, get_asset_path("images/tower_image.png"), TOWER_SIZE, 250, 1)
        self.projectiles = []
        self.score = INITIAL_SCORE
        self.life = Life(LIFE_COUNT, self.heart_full, self.heart_empty, self)
        self.path = PATH
        self.ice_original = pygame.image.load(get_asset_path("images/ice1.png"))
        self.ice_icon = pygame.transform.scale(self.ice_original, ICE_ICON_SIZE)
        self.ice = Ice(self.ice_original, self)
        self.coin = Coin(self.screen)
        self.sound_manager = SoundManager()
        self.setup_icons()

    def setup_icons(self):
        self.atk_rate_icon_rect = self.atk_rt_icn.get_rect(topleft=ATK_RATE_ICON_POS)
        self.atk_speed_icon_rect = self.atk_spd_icn.get_rect(topleft=ATK_SPEED_ICON_POS)
        self.ice_icon_rect = self.ice_icon.get_rect(topleft=ICE_ICON_POS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        # Verarbeite Klicks auf Upgrade-Icons
        if self.atk_rate_icon_rect.collidepoint(pos):
            self.attempt_upgrade('rate')
        elif self.atk_speed_icon_rect.collidepoint(pos):
            self.attempt_upgrade('speed')
        elif self.ice_icon_rect.collidepoint(pos):
            self.attempt_activate_ice()

    def attempt_upgrade(self, upgrade_type):
        # Logik zum Verbessern der Turmfähigkeiten
        if upgrade_type == 'rate' and self.score >= UPGRADE_ATK_RATE_COST:
            self.score -= UPGRADE_ATK_RATE_COST
            if self.tower.shoot_cooldown >= 2:
                self.tower.shoot_cooldown -= 5
        elif upgrade_type == 'speed' and self.score >= UPGRADE_ATK_SPEED_COST:
            self.score -= UPGRADE_ATK_SPEED_COST
            if self.tower.projectile_speed <= 100:
                self.tower.projectile_speed += 5

    def attempt_activate_ice(self):
        # Aktiviere das Eis-Upgrade, falls genug Punkte vorhanden sind
        if self.score >= ICE_SKILL_COST:
            self.score -= ICE_SKILL_COST
            self.ice.visible = True
            self.ice.reset()

    def update_game_state(self):
        # Ballons erzeugen
        if random.randint(1, 500) == 1:
            new_balloon = Balloon(self.path, "images/balloon_image.png", self.score, BALLOON_SIZE)
            self.balloons.append(new_balloon)

        # Ballons bewegen und überprüfen, ob sie das Ende erreicht haben oder von Projektilen getroffen wurden
        for bloon in self.balloons[:]:
            upd_bloon = bloon.update(self.screen, self.projectiles)
            if upd_bloon:
                self.balloons.remove(bloon)
                if upd_bloon[1]:  # Ballon hat das Ende erreicht
                    self.life.value -= 1
                else:  # Ballon wurde getroffen
                    self.score += 1
                    self.sound_manager.play_sound('pop')
        # Turm und Projektile aktualisieren
        update_tower(self)
        update_projectile(self)

        if self.ice.visible:
            self.ice.cast()  # Aktualisiert den Zustand des Eis-Effekts, falls nötig

    def draw_game_state(self):
        self.screen.fill((0, 0, 0))  # Hintergrund mit Schwarz füllen
        self.screen.blit(self.bg_image, (0, 0))  # Hintergrundbild zeichnen

        # Ballons zeichnen
        for bloon in self.balloons:
            bloon.draw(self.screen)

        # Turm zeichnen
        self.tower.draw(self.screen)

        # Projektile zeichnen
        for projectile in self.projectiles:
            if projectile.visible:
                projectile.draw(self.screen)

        if self.ice.visible:
            self.screen.blit(self.ice.image, self.ice.rect.topleft)  # Eis-Effekt zeichnen

        # UI-Elemente zeichnen
        self.draw_ui()

    def draw_ui(self):
        # Punktzahl anzeigen
        score_text = self.font.render(f": {self.score}", True, WHITE)
        self.screen.blit(score_text, (45, 10))

        # Leben anzeigen
        life_text = self.font.render(f"Life:", True, LIFE_COLOR)
        self.screen.blit(life_text, (120, 10))
        self.life.draw()

        # Icons und weitere UI-Elemente
        self.screen.blit(self.atk_rt_icn, ATK_RATE_ICON_POS)
        atk_speed_text = self.stat_font.render(f"atk rate: {100 - self.tower.shoot_cooldown}", True,
                                            pygame.Color(252, 3, 98))
        self.screen.blit(atk_speed_text, (self.screen_width - 115, 180))

        self.screen.blit(self.atk_spd_icn, ATK_SPEED_ICON_POS)
        atk_speed_text = self.stat_font.render(f"atk speed: {self.tower.projectile_speed}%", True,
                                            pygame.Color(252, 3, 98))
        self.screen.blit(atk_speed_text, (self.screen_width - 115, 280))

        self.screen.blit(self.ice_icon, ICE_ICON_POS)
        ice_text = self.stat_font.render(f"Freeze (skill)", True,
                                            pygame.Color(252, 3, 98))
        self.screen.blit(ice_text, (self.screen_width - 100, 400))
        # Hier können weitere Texte oder Icons hinzugefügt werden

    def run(self):
        # Die Anzahl der Logik-Updates pro Sekunde
        LOGIC_UPDATES_PER_SECOND = 60
        # Wie viele Millisekunden ein einzelnes Logik-Update dauern soll
        UPDATE_INTERVAL = 200 // LOGIC_UPDATES_PER_SECOND
    
        # Speichert, wann das letzte Update durchgeführt wurde
        last_update_time = pygame.time.get_ticks()

        # Starte die Hintergrundmusik beim Beginn der Spiel-Schleife
        self.sound_manager.play_sound('bg_music')
        self.running = True
        while self.running:
            self.handle_events()

            # Aktuelle Zeit in Millisekunden
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > UPDATE_INTERVAL:
                self.update_game_state()
                last_update_time = current_time
            self.draw_game_state()
            self.coin.update()
            pygame.display.update()
            self.clock.tick(190)
        pygame.quit()

Game().run()
pygame.quit()
