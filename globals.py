from typing import List, Tuple
from tilemap import Tilemap
from pacman import Pacman
from ghost import Ghost

__pacman: Pacman
__ghosts: List[Ghost] = []
__tilemap: Tilemap


def get_pacman() -> Pacman:
    return __pacman

def set_pacman(p: Pacman):
    global __pacman
    __pacman = p


def get_ghost(i: int) -> Ghost:
    global __ghosts
    return __ghosts[i]

def get_ghosts() -> Tuple[Ghost]:
    global __ghosts
    return tuple(__ghosts)

def add_ghost(g: Ghost):
    global __ghosts
    __ghosts.append(g)


def get_map() -> Tilemap:
    global __tilemap
    return __tilemap

def set_map(t: Tilemap):
    global __tilemap
    __tilemap = t
