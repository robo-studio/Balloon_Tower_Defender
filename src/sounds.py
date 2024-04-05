import pygame
from util import get_asset_path

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'pop': pygame.mixer.Sound(get_asset_path("sounds/pop.ogg")),
            'bg_music': get_asset_path("sounds/bg-music.mp3"),
        }

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            if sound_name == 'bg_music':
                pygame.mixer.music.load(self.sounds[sound_name])
                pygame.mixer.music.play(-1)
            else:
                self.sounds[sound_name].play()

    def stop_music(self):
        pygame.mixer.music.stop()
