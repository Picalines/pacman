from typing import TypeVar, Tuple, Dict

TNumber = TypeVar('TNumber', int, float, complex)
Vector = Tuple[TNumber, TNumber]
Color = Tuple[TNumber, TNumber, TNumber]

size: Vector = (800, 600)
tile_size: Vector = (32, 32)

black: Color = (0, 0, 0)
white: Color = (255, 255, 255)
red: Color = (255, 0, 0)
pink: Color = (255, 84, 167)
extr_pink: Color = (255, 0, 255)
orange: Color = (255, 141, 56)
Azure: Color = (0, 128, 255)

ghost_names: Tuple[str, ...] = ('blinky', 'clyde', 'inky', 'pinky')

directions: Tuple[Vector, ...] = ((1, 0), (-1, 0), (0, -1), (0, 1))
direction_names: Dict[Vector, str] = {(1, 0): 'right', (-1, 0): 'left', (0, -1): 'up', (0, 1): 'down'}
direction_angles: Dict[int, Vector] = {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)}
angles_direction: Dict[Vector, int] = {(1, 0): 0, (0, -1): 90, (-1, 0): 180, (0, 1): 270}

score = 0

tick_speed: int = 10
dt = 0
fps = 60

# функции нужны для нормальной работы import * from config,
# т.к в питоне импортируются не сами переменные, а их изначальные значения,
# и изменить их по-нормальному нельзя (только если ещё раз писать import config)

def get_dt() -> float:
    return dt

def set_dt(v: float):
    global dt
    dt = v

def get_score() -> int:
    return score

def add_score(v: int):
    global score
    score += v





