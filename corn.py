from config import Vector, Color, add_score, get_dt
import globals
import pygame

class Corn:
    color: Color = (255, 255, 255)

    image: pygame.Surface = pygame.image.load('res/corn.png')

    def __init__(self, surface: pygame.Surface, center_pos: Vector):
        self.surface = surface
        self.image = Corn.image.convert_alpha(Corn.image)
        self.rect = self.image.get_rect()
        self.rect.center = center_pos
        self.eaten = False

    def check_collision_rect(self, rect: pygame.Rect) -> bool:
        return (not self.eaten) and self.rect.colliderect(rect)

    def eat(self, score: int = 10):
        if not self.eaten:
            self.eaten = True
            add_score(score)

    def render(self):
        if not self.eaten:
            self.surface.blit(self.image, self.rect)


class SuperCorn(Corn):
    image: pygame.Surface = pygame.image.load('res/super_corn.png')

    buff_duration = 6
    buff_active_count = 0

    def __init__(self, surface: pygame.Surface, center_pos: Vector):
        super().__init__(surface, center_pos)
        self.image = SuperCorn.image.convert_alpha(SuperCorn.image)
        self.rect = self.image.get_rect()
        self.rect.size = (30, 30)
        self.rect.center = center_pos
        self.buff_timer = 0
        self.buff_active = False

    def eat(self, score: int = 50):
        if not self.eaten:
            self.buff_active = True
            SuperCorn.buff_active_count += 1
            globals.get_pacman().speed = 2
            for ghost in globals.get_ghosts():
                ghost.scare()
        super().eat(score)

    def render(self):
        super().render()
        if self.buff_active:
            self.buff_timer += get_dt()
            if self.buff_timer >= SuperCorn.buff_duration:
                self.buff_active = False
                if SuperCorn.buff_active_count == 1:
                    globals.get_pacman().speed = 1
                    globals.Ghost.score_multiplier = 1
                SuperCorn.buff_active_count -= 1
