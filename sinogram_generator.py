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


def calc_weakening(x, y, img, tmp):
    tmp[0] += img[x, y]
    if img[x, y] > 0:
        tmp[1] += 1
    tmp[2] += 1
    # img[x,y] = 0.5


# da - step, n - sensors per step, l - spread
def generate_sinogram(img, da=1, n=50, phi=100):
    res = []
    r = (len(img) // 2)

    for alpha in frange(0, 180, da):
        xe = r * cos(radians(alpha)) + r - 1
        ye = r * sin(radians(alpha)) + r - 1
        tmp = []
        for i in range(0, n, 1):
            deg = alpha - (phi / 2) + (i * (phi / n))
            xd = r * cos(radians(deg) + pi) + r - 1
            yd = r * sin(radians(deg) + pi) + r - 1
            bresenhamret = [0, 0, 0]
            bresenham(int(xe), int(ye), int(xd), int(yd), img, lambda x, y: calc_weakening(x, y, img, bresenhamret))
            tmp.append(pow(bresenhamret[0], 2))
        res.append(tmp)

    res = divide(res, amax(res))
    return res