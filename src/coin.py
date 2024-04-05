import pygame
from util import load_image, scale_image_to_height
from constants import COIN_ANIMATION_INTERVAL, COIN_SIZE

class Coin:
    def __init__(self, screen):
        self.screen = screen
        self.images = []
        self.images_original = [load_image(f"images/star_coin/star_coin_rotate/star_coin_{i}.png") for i in range(1, 7)]
        for image in self.images_original:
            self.images.append(scale_image_to_height(image, COIN_SIZE))
        self.idx = 0

    def update(self):
        x_offset = 0
        if self.idx > 0:
            x_offset = (COIN_SIZE - self.images[self.idx].get_width()) // 2
        
        self.screen.blit(self.images[self.idx], (10 + x_offset, 4))
        if 0 <= pygame.time.get_ticks() % COIN_ANIMATION_INTERVAL < 1:
            self.idx = (self.idx + 1) % (len(self.images))