import pygame
import os.path
from config import *


class HighScore:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 25, True)
        self.text_High_Score = "High Score:"
        self.ts1 = self.font.render(self.text_High_Score, False, white)

        hs_now = []
        if os.path.isfile('high_score.txt'):
            hs = open('high_score.txt', 'r')
            for line in hs:
                hs_now.append(line.replace("\n", ""))
            self.n = hs_now[0]
            hs.close()

        else:
            hs_now = ['0', '0', '0', '0', '0']
            hs = open('high_score.txt', 'w')
            hs.writelines("%s\n" % line for line in hs_now)
            self.n = '0'
            hs.close()

        self.ts2 = self.font.render(self.n, False, white)
        self.x1 = 650
        self.y1 = 60
        self.x2 = 650
        self.y2 = 90

    def render(self):
        if get_score() > int(self.n):
            self.n = str(get_score())

        self.ts2 = self.font.render(self.n, False, white)
        self.screen.blit(self.ts1, (self.x1, self.y1))
        self.screen.blit(self.ts2, (self.x2, self.y2))

    def updt(self):
        hs_now = []
        with open('high_score.txt', 'r') as hs:
            for line in hs:
                hs_now.append(line.replace("\n", ""))

        for s in hs_now:
            if get_score() == int(s):
                return

        hs_now.append(str(get_score()))
        hs_now_num = [int(g) for g in hs_now]
        hs_now_num = sorted(hs_now_num)
        hs_now = [int(g2) for g2 in hs_now_num]
        hs_now.reverse()
        hs_now = hs_now[:5]
        with open('high_score.txt', 'w') as hs:
            hs.writelines("%s\n" % line for line in hs_now)


