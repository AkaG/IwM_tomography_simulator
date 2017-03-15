from pylab import *


def bresenham(x1, y1, x2, y2, img, fun_to_exec_on_points=lambda x, y : None):
    res = 0
    x, y = x1, y1

    # kierunek rysowania
    getDir = lambda x1, x2: ((1 if x1 < x2 else -1), abs(x1 - x2))
    xi, dx = getDir(x1, x2)
    yi, dy = getDir(y1, y2)

    doBreak = lambda x, y, img: False if (x < len(img) and y < len(img)) else True

    fun_to_exec_on_points(x, y)
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx

        while x != x2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi

            if doBreak(x, y, img):
                break

            fun_to_exec_on_points(x, y)

    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy

        while y != y2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi

            if doBreak(x, y, img):
                break

            fun_to_exec_on_points(x, y)
