import os
import math
import pygame

from projectile import Projectile

def get_asset_path(absolute_path):
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__)) + "/../assets/"

    # Construct the absolute path
    return os.path.join(script_dir, absolute_path)

def load_image(image_path, size=None):
    image = pygame.image.load(get_asset_path(image_path))
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_angle(origin, target):
    return math.atan2(target.y - origin.y, target.x - origin.x)


def move_bloons(game):
    for balloon in game.balloons[:]:
        reached_end = balloon.move_on_path()
        balloon.draw(game.screen)
        if reached_end:
            game.life -= 0.5
            game.balloons.remove(balloon)


def update_tower(game):
    # Turm zielen und schießen
    target = game.tower.target(game.balloons)
    game.tower.draw(game.screen)
    if game.tower.update(game.balloons):
        projectile_x = game.tower.x + game.tower.image.get_width() / 2
        projectile_y = game.tower.y + game.tower.image.get_height() / 2
        #game.tower.projectile_speed = 5
        game.projectiles.append(
            Projectile(projectile_x, projectile_y, load_image("images/projectile_image.png", (10, 10)), game.tower.projectile_speed, game.tower.angle, game.tower))


def update_projectile(game):
    for projectile in game.projectiles[:]:
        projectile.move()
        projectile.draw(game.screen)

def scale_image_to_height(image, target_height):
    """Skaliert ein Pygame-Surface-Objekt auf die gegebene Zielhöhe bei Beibehaltung des Seitenverhältnisses."""
    image_height = image.get_height()
    image_width = image.get_width()
    scaling_factor = target_height / image_height
    new_width = int(image_width * scaling_factor)
    new_height = target_height
    return pygame.transform.scale(image, (new_width, new_height))

def scale_image_to_width(image, target_width):
    """Skaliert ein Pygame-Surface-Objekt auf die gegebene Zielbreite bei Beibehaltung des Seitenverhältnisses."""
    image_height = image.get_height()
    image_width = image.get_width()
    scaling_factor = target_width / image_width
    new_width = target_width
    new_height = int(image_height * scaling_factor)
    return pygame.transform.scale(image, (new_width, new_height))

