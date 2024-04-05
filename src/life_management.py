class Life:
    def __init__(self, init_life, img_f, img_e, game):
        self.game = game
        self.image_f = img_f
        self.image_e = img_e
        self.init_life = init_life
        self.value = init_life
        self.hearts = [[self.image_f, (180 + i * 30, 5), 'f'] for i in range(0, self.value)]

    def draw(self):
        for heart in self.hearts:
            self.game.screen.blit(heart[0], (heart[1][0], heart[1][1]))

    def update(self):
        if self.value < self.init_life:
            for i in range(self.value, self.init_life):
                if self.hearts[i][2] == 'f':
                    self.hearts[i][0] = self.image_e
                    return
                else:
                    return
