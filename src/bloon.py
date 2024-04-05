import pygame

from util import *


class Balloon:
    def __init__(self, path, image, score, size=None):
        """
        Initializes a Balloon object.

        Args:
            path (list): A list of (x, y) coordinates representing the path the balloon will follow.
            image (str): The filepath of the image file for the balloon.
            size (tuple): The size of the balloon image as a tuple of (width, height).
            score (float): The initial score of the balloon.

        Returns:
            None
        """
        self.score = score
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[self.path_index]
        self.image = load_image(image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0.5

    def move_on_path(self):
        """
        Moves the balloon along the defined path.

        Returns:
            bool: True if the balloon has reached the end of the path, False otherwise.
        """
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            angle = math.atan2(target_y - self.y, target_x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

            if distance_between_points(self.x, self.y, target_x, target_y) < self.speed:
                self.path_index += 1
        else:
            return True  # Signalizes that the balloon has reached the end of the path
        return False

    def draw(self, screen):
        """
        Draws the balloon on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the balloon on.

        Returns:
            None
        """
        screen.blit(self.image, (self.x, self.y))

    def update(self, screen, projectiles):
        """
        Updates the balloon's position, checks for collisions with projectiles, and updates the score.

        Args:
            screen (pygame.Surface): The surface to draw the balloon on.
            projectiles (list): A list of Projectile objects.

        Returns:
            tuple: A tuple containing the updated balloon object and a boolean value indicating if the balloon was hit or reached the end.
        """
        reached_end = self.move_on_path()
        self.draw(screen)
        for projectile in projectiles:
            if pygame.Rect.colliderect(self.rect, projectile.rect):
                offset = (int(self.x - projectile.x), int(self.y - projectile.y))
                if self.mask.overlap(projectile.mask, offset):
                    projectiles.remove(projectile)
                    self.score += 0.25
                    return self, False  # False => balloon hit

        if reached_end:
            self.score -= 1
            return self, True  # True => balloon reached end
