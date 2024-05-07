from config import tick_speed, Vector, get_dt
from pygame import Surface, Rect, image
from typing import Tuple

class Animation:
    def __init__(self, sprite_sheet: Surface, f_size: Vector, f_count: int, delay: float, pong: bool=False, start: int=0):
        # init sprite size
        self.sprite_size = f_size

        # crop sheet to sprites in tuple
        sprites = []
        if f_count <= 1:
            raise ValueError("animation sprite count can't be <= 1")
        if start < 0:
            raise ValueError("animation invalid start argument")

        for x in range(0, f_count):
            sprites.append(sprite_sheet.subsurface(((start + x) * self.sprite_size[0], 0, f_size[0], f_size[1])))
        self.sprites: Tuple[Surface, ...] = tuple(sprites)
        if len(self.sprites) != f_count:
            raise ValueError("invalid animation frames count")
        self.sprites_count: int = f_count

        # set delay > 0
        if delay <= 0:
            raise ValueError("animation delay can't be <= 0")
        self.delay: float = delay

        self.pong = pong
        self.timer = 0
        self.current_sprite = 0
        self.sprite_shift = 1

    def update(self):
        self.timer += get_dt() # timer in ms, delay in sec
        if self.timer >= self.delay:
            self.timer = 0
            self.current_sprite += self.sprite_shift
            if self.current_sprite >= self.sprites_count:
                if self.pong:
                    self.sprite_shift *= -1
                    self.current_sprite = self.sprites_count - 2
                else:
                    self.current_sprite = 0
            elif self.current_sprite < 0:
                self.sprite_shift = 1
                self.current_sprite = 1

    def get_sprite(self) -> Surface:
        return self.sprites[self.current_sprite]

    def get_rect(self) -> Rect:
        return self.get_sprite().get_rect()

    def render(self, screen: Surface, pos: Vector = (0, 0)):
        screen.blit(self.get_sprite(), pos)


if __name__ == '__main__':
    from pygame import display, event, QUIT, time
    from config import size as screen_size, black, set_dt, fps

    wscreen = display.set_mode(screen_size)
    game_over = False
    clock = time.Clock()

    test_anim = Animation(image.load("res/pacman_anim.png"), (32, 32), 3, 0.2, True)

    while not game_over:
        for ev in event.get():
            if ev.type == QUIT:
                game_over = True

        wscreen.fill(black)

        test_anim.update()
        test_anim.render(wscreen)

        display.flip()
        time.wait(tick_speed)
        set_dt(clock.tick(fps) / 1000.0)
