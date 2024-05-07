import pygame
from config import *
import os.path
from run import screen, font


class Button:
    def __init__(self, x, y, act_color, not_act_color, action=None):
        self.screen = pygame.display.set_mode(size)
        self.act_color = act_color
        self.not_act_color = not_act_color
        self.rect = act_color.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action

    def draw_button(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (self.rect.x <= mouse[0] <= (self.rect.x + 300)) and (self.rect.y <= mouse[1] <= (self.rect.y + 65)):
            self.screen.blit(self.act_color, self.rect)
            if click[0] == 1:
                if self.action is not None:
                    self.action()
        else:
            self.screen.blit(self.not_act_color, self.rect)


def h_scr():
    font2 = pygame.font.SysFont('arial', 45, True)
    show_hsc = False

    hs_now = []
    if os.path.isfile('high_score.txt'):
        hs = open('high_score.txt', 'r')
        for line in hs:
            hs_now.append(line.replace("\n", ""))
        hs.close()

    else:
        hs_now = ['0', '0', '0', '0', '0']
        hs = open('high_score.txt', 'w')
        hs.writelines("%s\n" % line for line in hs_now)
        hs.close()
    while not show_hsc:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    show_hsc = True

        screen.fill(black)

        text_h_scr1 = font2.render("High Score:", False, white)
        screen.blit(text_h_scr1, (800 / 2 - text_h_scr1.get_rect().w // 2, 7))

        y_scr_in_t = 57
        i = 0
        for i in range(5):
            text_h_scr2 = font2.render(hs_now[i], False, white)
            y_scr_in_t += 60
            screen.blit(text_h_scr2, (800 / 2 - text_h_scr2.get_rect().w // 2, y_scr_in_t))

        text_h_scr3 = font2.render("Press Esc To Exit The Menu", False, white)

        screen.blit(text_h_scr3, (800 / 2 - text_h_scr3.get_rect().w // 2, 500))
        pygame.display.flip()

    from run import show_menu
    show_menu()


def authors(name_T_L, name_Del_1, name_Del_2, name_Del_3, name_Del_4):
    name_T_L = font.render(name_T_L, False, pink)
    name_Del_1 = font.render(name_Del_1, False, orange)
    name_Del_2 = font.render(name_Del_2, False, extr_pink)
    name_Del_3 = font.render(name_Del_3, False, red)
    name_Del_4 = font.render(name_Del_4, False, Azure)
    screen.blit(name_T_L, (620, 350))
    screen.blit(name_Del_1, (620, 400))
    screen.blit(name_Del_2, (620, 450))
    screen.blit(name_Del_3, (620, 500))
    screen.blit(name_Del_4, (620, 550))












