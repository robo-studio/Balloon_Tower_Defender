import pygame
from util import *
class Tower:
    def __init__(self, x, y, image, size, range, projectile_speed):
        self.projectile_speed = projectile_speed
        self.x = x
        self.y = y
        self.image_original = pygame.image.load(image)
        self.image_original = pygame.transform.scale(self.image_original, size)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image_original)
        self.range = range
        self.angle = 0
        self.shoot_cooldown = 50
        self.shoot_cooldown_time = 50

    def update(self, balloons):
        target = self.target(balloons)
        if target and self.shoot_cooldown_time <= 0:
            self.shoot_cooldown_time = self.shoot_cooldown  # Setzt die Abklingzeit (20 Frames)
            return True
        self.shoot_cooldown_time -= 1
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        # Kommentiere diesen Code ein, damit der Tower sich auch dreht
        # rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        # new_rect = rotated_image.get_rect(center=self.rect.center)
        # screen.blit(rotated_image, new_rect.topleft)

    def target(self, balloons):
        # Zielt auf den ersten Ballon, der in Reichweite ist
        for balloon in balloons:
            if distance_between_points(self.x, self.y, balloon.x, balloon.y) < self.range:
                self.angle = calculate_angle(self, balloon)
                return balloon
        return None

