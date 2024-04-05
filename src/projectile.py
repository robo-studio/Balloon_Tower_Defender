import pygame
import math


class Projectile:
    def __init__(self, x, y, image, speed, angle, tower):
        self.tower = tower
        self.x = x
        self.y = y
        self.visible = False
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.angle = angle

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        if not self.visible:
            # Erstellt eine Maske für das Projektil und den Turm
            projectile_mask = pygame.mask.from_surface(self.image)
            tower_mask = pygame.mask.from_surface(self.tower.image_original)
            offset = (int(self.tower.x - self.x), int(self.tower.y - self.y))

            # Überprüft, ob das Projektil den Turm verlassen hat
            if not projectile_mask.overlap(tower_mask, offset):
                self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))
