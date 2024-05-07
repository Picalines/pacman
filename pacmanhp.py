import pygame


class HP:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.hp = pygame.image.load("res/pacman_hp.png")
        self.rect = self.hp.get_rect()
        self.rect.x = 690
        self.rect.y = 2
        self.count = 3

    def render(self):
        for x in range(0, self.count):
            self.surface.blit(self.hp, self.rect)
            self.rect.x += 35
        self.rect.x = 690
        
