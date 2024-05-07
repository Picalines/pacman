from config import Vector, directions
from random import randint
from math import floor

def clamp(n: float, smallest: float, largest: float) -> float:
    return max(smallest, min(n, largest))

def clamp_vector(v: Vector, l: Vector) -> Vector:
    return clamp(v[0], 0, l[0]), clamp(v[1], 0, l[1])

def vector_inverted(v: Vector) -> Vector:
    return v[0] * -1, v[1] * -1

def vector_length(v: Vector) -> float:
    return (v[0] ** 2 + v[1] ** 2) ** 0.5

def vector_norm(v: Vector) -> Vector:
    if v == (0, 0):
        return v
    return div_vector(v, vector_length(v))

def vector_dist(a: Vector, b: Vector) -> float:
    return vector_length((a[0] - b[0], a[1] - b[1]))

def get_tile_pos(pos: Vector, tile_size: Vector) -> Vector:
    return pos[0] // tile_size[0], pos[1] // tile_size[1]

def mult_vector(a: Vector, b: float) -> Vector:
    return a[0] * b, a[1] * b

def div_vector(a: Vector, b: float) -> Vector:
    return a[0] / b, a[1] / b

def vector_sum(a: Vector, b: Vector) -> Vector:
    return a[0] + b[0], a[1] + b[1]

def vector_sub(a: Vector, b: Vector) -> Vector:
    return a[0] - b[0], a[1] - b[1]

def rand_vector() -> Vector:
    return directions[randint(0, len(directions) - 1)]

def floor_vector(v: Vector) -> Vector:
    return floor(v[0]), floor(v[1])