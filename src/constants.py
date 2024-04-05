"""
This module contains constant values used in the Bloon Tower Defense game.

Constants:
- SCREEN_WIDTH: The width of the game screen.
- SCREEN_HEIGHT: The height of the game screen.
- WHITE: The RGB value for the color white.
- LIFE_COLOR: The RGB value for the life color.
- FONT_SIZE_LARGE: The font size for large text.
- FONT_SIZE_SMALL: The font size for small text.
- TOWER_SIZE: The size of the tower image.
- BALLOON_SIZE: The size of the balloon image.
- HEART_FULL_SIZE: The size of the full heart image.
- HEART_EMPTY_SIZE: The size of the empty heart image.
- ATK_RATE_ICON_SIZE: The size of the attack rate icon image.
- ATK_SPEED_ICON_SIZE: The size of the attack speed icon image.
- ICE_ICON_SIZE: The size of the ice icon image.
- PROJECTILE_SIZE: The size of the projectile image.
- PATH: The coordinates of the path that the balloons follow.
- INITIAL_SCORE: The initial score of the player.
- LIFE_COUNT: The initial number of lives the player has.
- UPGRADE_ATK_RATE_COST: The cost to upgrade the attack rate.
- UPGRADE_ATK_SPEED_COST: The cost to upgrade the attack speed.
- ICE_SKILL_COST: The cost to use the ice skill.

Author: Fiji141
"""

import pygame

# Bildschirmeinstellungen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Farben
WHITE = (255, 255, 255)
LIFE_COLOR = (252, 3, 98)  # RGB-Wert

# Schriftgrößen
FONT_SIZE_LARGE = 36
FONT_SIZE_SMALL = 22

# Bildgrößen
TOWER_SIZE = (50, 50)
BALLOON_SIZE = (50, 50)
HEART_SIZE = (30, 30)
ATK_ICON_SIZE = (80, 80)
ICE_ICON_SIZE = (120, 120)
PROJECTILE_SIZE = (10, 10)
COIN_SIZE = 35

# Icons
ATK_RATE_ICON_POS = (SCREEN_WIDTH - 90, 100)
ATK_SPEED_ICON_POS = (SCREEN_WIDTH - 90, 200)
ICE_ICON_POS = (SCREEN_WIDTH - 110, 300) # self.screen_width - 110, 300

# Pfadkonfigurationen
PATH = [(0, 300), (200, 300), (200, 100), (600, 100), (600, 500), (800, 500)]

# Spielwerte
INITIAL_SCORE = 2000
LIFE_COUNT = 6

# Kosten
UPGRADE_ATK_RATE_COST = 20
UPGRADE_ATK_SPEED_COST = 15
ICE_SKILL_COST = 100

# Sonstiges
ICON_X_OFFSET = -90
COIN_ANIMATION_INTERVAL = 32
