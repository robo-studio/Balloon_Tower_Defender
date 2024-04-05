import pygame.transform
class Ice:
    def __init__(self, image, game):
        self.duration = 4000
        self.start = pygame.time.get_ticks()
        self.game = game
        self.image_original = image
        self.start_img = pygame.transform.scale(self.image_original, (300, 300))
        self.image = self.start_img
        self.x_pos = game.screen_width / 2
        self.y_pos = game.screen_height / 2
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.visible = False
        self.angle = 0  # Winkel für die Drehung

    def reset(self):
        self.start = pygame.time.get_ticks()
        self.start_img = pygame.transform.scale(self.image_original, (300, 300))
        self.image = self.start_img
        self.angle = 0

    def cast(self):
        if self.visible and ((pygame.time.get_ticks() - self.start) <= self.duration):
            # Skalieren des Bildes
            old_size = self.start_img.get_size()
            new_size = int(old_size[0] * 1.025), int(old_size[1] * 1.025)
            self.start_img = pygame.transform.scale(self.image_original, new_size)

            # Drehen des skalierten Bildes
            self.image = pygame.transform.rotate(self.start_img, self.angle)
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

            # Drehwinkel aktualisieren
            self.angle += 1

        elif not self.visible:
            self.reset()

# import pygame.transform
# import pygame.time
#
#
# class Ice:
#     def __init__(self, image, game):
#         self.duration = 3000
#         self.start = pygame.time.get_ticks()
#         self.angle = 0
#         self.game = game
#         self.image_original = image
#         self.start_img = pygame.transform.scale(self.image_original, (300, 300))
#         self.image = self.start_img
#         self.x_pos = game.screen_width / 2
#         self.y_pos = game.screen_height / 2
#         self.rect = self.image.get_rect()
#         self.rect.center = self.x_pos, self.y_pos
#         self.visible = False
#
#     def cast(self):
#         if self.visible:
#             if (pygame.time.get_ticks() - self.start) <= self.duration:
#                 old_size = self.image.get_width()
#                 if old_size <= 500:
#                     new_size = int(self.image.get_size()[0] * 1.025), int(self.image.get_size()[0] * 1.025)
#                     new_image = pygame.transform.scale(self.image, new_size)
#
#                     # Aktualisiere die Position, um das Bild im Zentrum zu halten
#                     self.rect = new_image.get_rect()
#                     self.rect.center = (self.x_pos, self.y_pos)
#
#                     self.image = pygame.transform.rotate(new_image, self.angle)
#                     self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
#                     self.angle += 1
#             else:
#                 self.visible = False
