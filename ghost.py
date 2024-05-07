from animation import Animation
from typing import Callable
from pacman import Pacman
from math_utils import *
from config import *
import globals
import pygame


def check_ghost_name(name: str, include_sates=False):
    if not (name in ghost_names):
        if (not include_sates) or (not name.startswith("scared_") and name != 'killed'):
            raise ValueError("invalid ghost name: " + name)

def load_ghost_animation(name: str) -> Dict[Vector, Animation]:
    check_ghost_name(name, True)
    if Ghost.animation_sheets.get(name) is None:
        Ghost.animation_sheets[name] = pygame.image.load('res/ghosts/' + name + '_sprites.png')
    sheet = Ghost.animation_sheets[name]
    sheet = pygame.transform.scale(sheet, (tile_size[0] * 8, tile_size[1]))
    fsize, fcount, fdelay, floop = tile_size, 2, 0.2, True
    return {
        (1, 0): Animation(sheet, fsize, fcount, fdelay, floop),
        (-1, 0): Animation(sheet, fsize, fcount, fdelay, floop, start=2),
        (0, -1): Animation(sheet, fsize, fcount, fdelay, floop, start=4),
        (0, 1): Animation(sheet, fsize, fcount, fdelay, floop, start=6)
    }


class Ghost:
    animation_sheets: Dict[str, pygame.Surface] = {}

    score_multiplier: int = 1

    def __init__(self, surface: pygame.Surface, pos: Vector, name: str):
        check_ghost_name(name)
        self.name = name
        self.surface = surface

        self.image = pygame.Surface(tile_size, pygame.SRCALPHA, 32)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = pos

        self.animations: Dict[str, Dict[Vector, Animation]] = {
            'move': load_ghost_animation(self.name),
            'scared': load_ghost_animation('scared_0'),
            'scared_end': load_ghost_animation('scared_1'),
            'killed': load_ghost_animation('killed')
        }

        self.ai = ghost_ai_schemes[self.name](self)

        self.move = (0, -1)

        from globals import add_ghost
        add_ghost(self)

    def get_animation(self) -> Animation:
        move_dir = vector_norm(self.move)
        if not self.is_alive():
            return self.animations['killed'][move_dir]
        if self.is_scared():
            if self.ai.scared_timer / GhostAI.scared_duration_sec >= 0.7:
                return self.animations['scared_end'][move_dir]
            else:
                return self.animations['scared'][move_dir]
        return self.animations['move'][move_dir]

    def update(self):
        self.get_animation().update()
        self.ai.update()
        self.rect.x += self.move[0]
        self.rect.y += self.move[1]
        if self.rect.x < 0:
            self.rect.x = 18 * 32
            self.ai.path = 0
        if self.rect.x > 18 * 32:
            self.rect.x = 0
            self.ai.path = 0

    def render(self):
        self.image.fill(0)
        self.get_animation().render(self.image, (0, 0))
        self.surface.blit(self.image, self.rect)

    def check_collision_rect(self, other_rect: pygame.Rect) -> bool:
        return self.is_alive() and self.rect.colliderect(other_rect)

    def set_speed(self, v: float):
        self.move = mult_vector(self.move, v)

    # <editor-fold desc="ai state shortcuts">

    def is_alive(self) -> bool:
        return self.ai.state != "killed"

    def is_scared(self) -> bool:
        return self.ai.state == 'scared'

    def kill(self) -> bool:
        if self.ai.state == "scared":
            self.ai.state = "killed"
            add_score(200 * Ghost.score_multiplier)
            Ghost.score_multiplier += 1
            if Ghost.score_multiplier > 4:
                Ghost.score_multiplier = 1
        return not self.is_alive()

    def scare(self):
        self.ai.state = "scared"
        self.ai.scared_timer = 0

    # </editor-fold>


class GhostAI:
    StateCallable = Callable[[Pacman], Vector]

    scared_duration_sec = 6
    patrol_duration_sec = 10

    def __init__(self, ghost: Ghost):
        self.state = "patrol"
        self.ghost = ghost
        self.target = (0, 0)
        self.scared_timer = 0
        self.patrol_timer = GhostAI.patrol_duration_sec / 10
        self.path = tile_size[0]

    def check_state(self) -> StateCallable:
        attr = getattr(self, self.state, 0)
        if attr == 0 or not callable(attr):
            raise ValueError(f"invalid Ghost AI state '{self.state}'")
        return attr

    def update(self):
        if self.state == "scared":
            self.scared_timer += get_dt()
            self.patrol_timer = 0
        elif self.state != "killed":
            self.scared_timer = 0
            self.patrol_timer += get_dt()
            if self.state == "patrol" and self.patrol_timer >= GhostAI.patrol_duration_sec:
                self.patrol_timer = 0
                self.state = "chase"
            elif self.state == "chase" and self.patrol_timer >= GhostAI.patrol_duration_sec * 1.4:
                self.patrol_timer = 0
                self.state = "patrol"
        self.path -= vector_length(self.ghost.move)
        if self.path <= 0:
            self.path = tile_size[0]
            try:
                self.ghost.move = vector_norm(self.ghost.move)
                d: Vector = self.check_state()(globals.get_pacman())
                self.ghost.move = d
                if self.state == "killed":
                    self.ghost.set_speed(4)
            except TypeError:
                raise ValueError(f"invalid Ghost AI state '{self.state}'")

    def choose_direction(self) -> Vector:
        dirs = list(directions[:])
        ghost_dir_inv = vector_inverted(vector_norm(self.ghost.move))
        dirs.remove(ghost_dir_inv)

        tmap = globals.get_map()
        tsx, tsy = tmap.tile_size[0], tmap.tile_size[1]

        self.ghost.rect.x = int(self.ghost.rect.x // tsx) * tsx
        self.ghost.rect.y = int(self.ghost.rect.y // tsy) * tsy

        g_tpos = (self.ghost.rect.x // tsx, self.ghost.rect.y // tsy)

        for d in dirs[:]:
            s = clamp_vector(vector_sum(g_tpos, d), vector_sub(tmap.size, (1, 1)))
            if tmap.tiles[s[0]][s[1]] != 0:
                dirs.remove(d)

        def get_rpos(v: Vector): return (v[0] + 0.5) * tsx, (v[1] + 0.5) * tsy

        tar_rpos = get_rpos(self.target)
        r = sorted(dirs, key=lambda d: vector_dist( get_rpos(vector_sum(g_tpos, d)), tar_rpos ))
        if len(r) == 0:
            return 0, 1

        return r[0]

    # <editor-fold desc='blank states'>

    def chase(self, pacman: Pacman) -> Vector:
        raise NotImplemented

    def patrol(self, pacman: Pacman) -> Vector:
        raise NotImplemented

    def scared(self, pacman: Pacman) -> Vector:
        if self.scared_timer >= GhostAI.scared_duration_sec:
            self.scared_timer = 0
            self.state = "chase"
        self.target = vector_sum(get_tile_pos(self.ghost.rect.topleft, tile_size), rand_vector())
        return self.choose_direction()

    def killed(self, pacman: Pacman) -> Vector:
        tmap = globals.get_map()
        self.target = (tmap.size[0] // 2, tmap.size[1] // 2 - 2)
        if get_tile_pos(self.ghost.rect.topleft, tile_size) == self.target:
            self.state = "patrol"
            return self.patrol(pacman)
        return self.choose_direction()

    # </editor-fold>


# <editor-fold desc="ai schemes">


class BlinkyAI(GhostAI):
    def chase(self, pacman: Pacman) -> Vector:
        tmap = globals.get_map()
        self.target = (pacman.rect.x // tmap.tile_size[0], pacman.rect.y // tmap.tile_size[1])
        return self.choose_direction()

    def patrol(self, pacman: Pacman) -> Vector:
        self.target = (globals.get_map().size[0] - 1, 0)
        return self.choose_direction()


class PinkyAI(GhostAI):
    def chase(self, pacman: Pacman) -> Vector:
        tmap = globals.get_map()
        look_dir = mult_vector(direction_angles[pacman.angle], 2)
        self.target = vector_sum((pacman.rect.x // tmap.tile_size[0], pacman.rect.y // tmap.tile_size[1]), look_dir)
        return self.choose_direction()

    def patrol(self, pacman: Pacman) -> Vector:
        self.target = (0, 0)
        return self.choose_direction()


class InkyAI(GhostAI):
    Blinky: Ghost = None

    def chase(self, pacman: Pacman) -> Vector:
        if InkyAI.Blinky is None:
            InkyAI.Blinky = globals.get_ghost(0)
        tmap = globals.get_map()
        look_dir = direction_angles[pacman.angle]
        self.target = vector_sum((pacman.rect.x // tmap.tile_size[0], pacman.rect.y // tmap.tile_size[1]), look_dir)
        diff = vector_sub(self.target, (InkyAI.Blinky.rect.x // tmap.tile_size[0], InkyAI.Blinky.rect.y // tmap.tile_size[1]))
        self.target = vector_sum(self.target, diff)
        return self.choose_direction()

    def patrol(self, pacman: Pacman) -> Vector:
        self.target = vector_sum(globals.get_map().size, (-1, -1))
        return self.choose_direction()


class ClydeAI(GhostAI):
    def chase(self, pacman: Pacman) -> Vector:
        if vector_dist(self.ghost.rect.center, pacman.rect.center) >= 32 * 8:
            tmap = globals.get_map()
            self.target = (pacman.rect.x // tmap.tile_size[0], pacman.rect.y // tmap.tile_size[1])
            return self.choose_direction()
        else:
            return self.patrol(pacman)

    def patrol(self, pacman: Pacman) -> Vector:
        self.target = (0, globals.get_map().size[1] - 1)
        return self.choose_direction()


ghost_ai_schemes = {
    'blinky': BlinkyAI,
    'pinky': PinkyAI,
    'inky': InkyAI,
    'clyde': ClydeAI
}


# </editor-fold>


ghost_cage_image = None

def render_ghost_cage(surface: pygame.Surface, pos: Vector, count: int = 5):
    global ghost_cage_image
    if ghost_cage_image is None:
        ghost_cage_image = pygame.image.load("res/cage.png")
    for x in range(count):
        surface.blit(ghost_cage_image, (pos[0] + tile_size[0] * x, pos[1]))


'''if __name__ == '__main__':
    from config import size, black, tick_speed
    from tilemap import Tilemap, load_map_from_txt

    clock = pygame.time.Clock()

    over = False
    wscreen: pygame.Surface = pygame.display.set_mode(size)

    player = Pacman(wscreen, (32 * 9, 32 * 13))

    corns = []
    tile_map = Tilemap(wscreen, (19, 19), (32, 32), pygame.image.load('tiles_sheet.png'))
    load_map_from_txt('map_data.txt', tile_map, wscreen, corns)

    poses = [((7 + x) * 32, 8 * 32) for x in (0, 1, 3, 4)]
    ghosts = []
    i = 0
    for n in ghost_names:
        ghosts.append(Ghost(wscreen, poses[i], n))
        i += 1

    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True

        wscreen.fill(black)
        tile_map.render()

        for c in corns:
            if player.rect.collidepoint(c.rect.center[0], c.rect.center[1]):
                c.eat()
            c.render()

        for g in ghosts:
            if g.check_collision_rect(player.rect):
                g.kill()
            g.update()
            g.render()

        render_ghost_cage(wscreen, (32 * 7, 32 * (17 // 2)))

        player.input()
        player.render()

        pygame.display.flip()
        pygame.time.wait(tick_speed)
        set_dt(clock.tick(fps) / 1000.0)'''