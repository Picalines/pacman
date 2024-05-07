from math_utils import Vector, get_tile_pos, vector_inverted, vector_sum
from config import tile_size, angles_direction
import pygame

class Pacman:
    eat_anim_image = pygame.image.load("res/pacman_anim.png")
    death_anim_image = pygame.image.load("res/pacman_death.png")

    def __init__(self, surface: pygame.Surface, pos: Vector):
        from animation import Animation

        self.surface = surface
        self.anim = Animation(Pacman.eat_anim_image, tile_size, 3, 0.1, True)
        self.death_anim = Animation(Pacman.death_anim_image, tile_size, 6, 0.3, False)
        self.image: pygame.Surface = pygame.Surface(tile_size, pygame.SRCALPHA, 32)

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = pos
        self.shift: Vector = (0, 0)
        self.input_dir: Vector = (0, -1)
        self.speed = 1
        self.angle = 0

        self.start_pos = self.rect.topleft
        self.old_tile_pos = get_tile_pos(self.rect.topleft, tile_size)

        self.dead = False

        from globals import set_pacman
        set_pacman(self)

    def update(self):
        self.input()
        new_tile_pos = get_tile_pos(self.rect.topleft, tile_size)
        if self.old_tile_pos != new_tile_pos:
            self.check_map_collision()
        elif self.shift == (0, 0):
            self.check_map_collision()
        elif self.input_dir == vector_inverted(self.shift):
            self.check_map_collision()

        self.rect.x += self.shift[0] * self.speed
        self.rect.y += self.shift[1] * self.speed
        
        if self.rect.x < 0:
            self.rect.x = 18 * 32
        if self.rect.x > 18 * 32:
            self.rect.x = 0

        self.old_tile_pos = new_tile_pos

        if self.shift != (0, 0):
            self.anim.delay = 0.1 / self.speed
            self.anim.update()
            self.angle = angles_direction[self.shift]
        else:
            self.anim.current_sprite = 1

    def render(self):
        self.image.fill(0)

        if not self.dead:
            self.update()
            self.anim.render(self.image)
        else:
            if self.death_anim.current_sprite < self.death_anim.sprites_count - 1:
                self.death_anim.update()
            self.death_anim.render(self.image)

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.surface.blit(self.image, self.rect)

    def set_speed(self, v: float):
        self.speed = v

    def kill(self):
        self.dead = True
        self.angle = 0
        self.shift = (0, 0)
        self.input_dir = (0, -1)

    def rebirth(self):
        if self.dead:
            self.dead = False
            self.rect.topleft = self.start_pos
            self.speed = 1
            self.shift = (0, 0)
            self.input_dir = (0, -1)
            self.death_anim.current_sprite = 0
            self.death_anim.timer = 0

    def check_map_collision(self):
        from globals import get_map

        try:
            tmap = get_map()
            t_pos = get_tile_pos(self.rect.center, tmap.tile_size)

            if self.shift != self.input_dir:
                t_inpt_pos = vector_sum(t_pos, self.input_dir)
                if tmap.tiles[t_inpt_pos[0]][t_inpt_pos[1]] == 0:
                    self.shift = tuple(self.input_dir)

            t_next_pos = vector_sum(t_pos, self.shift)
            if tmap.tiles[t_next_pos[0]][t_next_pos[1]] != 0:
                self.shift = (0, 0)
        except IndexError:
            return

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.input_dir = (-1, 0)
        elif keys[pygame.K_d]:
            self.input_dir = (1, 0)
        elif keys[pygame.K_w]:
            self.input_dir = (0, -1)
        elif keys[pygame.K_s]:
            self.input_dir = (0, 1)
