from collections import namedtuple

# Prepare vec(tor) / point type
vec = namedtuple("vec", "y x")


def vec_add(v1: vec, v2: vec) -> vec:
    return vec(v1.y + v2.y, v1.x + v2.x)


def vec_sub(v1: vec, v2: vec) -> vec:
    return vec(v1.y - v2.y, v1.x - v2.x)

def vec_mul(self: vec, mult) -> vec:
    return vec(self.y * mult, self.x * mult)

def vec_rotate_cw(self: vec) -> vec:
    return vec(self.x, -self.y)


def vec_rotate_ccw(self: vec) -> vec:
    return vec(-self.x, self.y)


vec.__add__ = vec_add
vec.__sub__ = vec_sub
vec.__mul__ = vec_mul
vec.rotate_cw = vec_rotate_cw
vec.rotate_ccw = vec_rotate_ccw


DIR_UP = vec(-1, 0)
DIR_RIGHT = vec(0, 1)
DIR_DOWN = vec(1, 0)
DIR_LEFT = vec(0, -1)

DIRS_ALL = [DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT]


__all__ = ["vec", "DIR_UP", "DIR_RIGHT", "DIR_DOWN", "DIR_LEFT", "DIRS_ALL"]
