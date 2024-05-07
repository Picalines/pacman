from config import Vector, tile_size as ts
from typing import List, Tuple
import pygame

class Tilemap:
    def __init__(self, surface: pygame.Surface, size: Vector, tile_size: Vector, tile_sheet: pygame.Surface):
        self.size = size
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("tilemap size <= 0")

        self.tiles: List[List[int]] = [[0 for _ in range(0, size[1])] for __ in range(0, size[0])]

        self.tile_size = tile_size
        timgs: List[pygame.Surface] = []
        tcount = tile_sheet.get_rect().w // tile_size[0]
        for x in range(0, tcount):
            timgs.append(tile_sheet.subsurface((x * tile_size[0], 0, tile_size[0], tile_size[1])))
        self.tile_images: Tuple[pygame.Surface] = tuple(timgs)

        self.surface = surface
        self.rendered = False
        self.image = pygame.Surface((tile_size[0] * size[0], tile_size[1] * size[1]))

        from globals import set_map
        set_map(self)

    def check_tile_pos(self, x: int, y: int):
        return 0 <= x <= self.size[0] and self.size[1] >= y >= 0

    def check_tile_id(self, tile_id: int):
        return 0 <= tile_id < len(self.tile_images)

    def set_tile(self, x: int, y: int, tile_id: int):
        if not self.check_tile_pos(x, y):
            raise ValueError(f"invalid tile pos [{x}, {y}]")
        if not self.check_tile_id(tile_id):
            raise ValueError(f"invalid tile id {tile_id}")
        self.rendered = False
        self.tiles[x][y] = tile_id

    def render(self, pos: Vector = (0, 0)):
        if not self.rendered:
            self.image.fill(0)
            for x in range(0, self.size[0]):
                for y in range(0, self.size[1]):
                    t_id = self.tiles[x][y]
                    d = (x * self.tile_size[0], y * self.tile_size[1])
                    self.image.blit(self.tile_images[t_id], d)
            self.rendered = True
        self.surface.blit(self.image, pos)


def load_map_from_txt(path: str, tilemap: Tilemap, surface: pygame.Surface, corns: list):
    from corn import Corn, SuperCorn
    with open(path) as f:
        y = 0
        for line in f.readlines():
            lin_tiles = [tid for tid in line.split(",")]
            x = 0
            for t_id in lin_tiles:
                t_id_r = t_id.replace(" ", "")
                if t_id_r == "d":
                    corns.append(Corn(surface, ((x + 0.5) * ts[0], (y + 0.5) * ts[1])))
                elif t_id_r == "ds":
                    corns.append(SuperCorn(surface, ((x + 0.5) * ts[0], (y + 0.5) * ts[1])))
                else:
                    tilemap.set_tile(x, y, int(t_id))
                x += 1
            y += 1
        f.close()


if __name__ == '__main__':
    from config import size as ssize, tick_speed

    wscreen = pygame.display.set_mode(ssize)

    corns = []

    test_map = Tilemap(wscreen, (25, 19), (32, 32), pygame.image.load('tiles_sheet.png'))
    load_map_from_txt('map_data.txt', test_map, wscreen, corns)

    over = False
    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True

        test_map.render()

        for c in corns:
            c.render()

        pygame.display.flip()
        pygame.time.wait(tick_speed)