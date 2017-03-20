from pylab import *


def bresenham(x, y, x2, y2, img, fun_to_exec_on_points=lambda x, y: None):
    w = x2 - x
    h = y2 - y
    dx1, dy1, dx2, dy2 = sign(w), sign(h), sign(w), 0

    length = abs(w)
    height = abs(h)

    # switch x and y axis
    if length <= height:
        length = abs(h)
        height = abs(w)
        dy2 = sign(h)
        dx2 = 0

    numerator = length // 2
    for i in range(0, length, 1):
        fun_to_exec_on_points(x, y)
        numerator += height
        if numerator >= length:
            numerator -= length
            x += dx1
            y += dy1
        else:
            x += dx2
            y += dy2
