import pygame
from config import *


class Score:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 25, True)
        self.text = "Score: "
        self.text1 = self.font.render(self.text, False, white)
        self.text2 = self.font.render(str(score), False, white)
        self.x_txt = 650
        self.y_txt = 150
        self.x_scr = 650
        self.y_scr = 180

    def render(self):

        self.screen.blit(self.text1, (self.x_txt, self.y_txt))
        self.text2 = self.font.render(str(get_score()), False, white)
        self.screen.blit(self.text2, (self.x_scr, self.y_scr))


