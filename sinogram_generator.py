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
    for i in range(0, length , 1):
        fun_to_exec_on_points(x, y)
        numerator += height
        if numerator >= length:
            numerator -= length
            x += dx1
            y += dy1
        else:
            x += dx2
            y += dy2

# da - step, n - sensors per step, l - spread
def generate_sinogram(img, da=1, n=20, phi=30):
    res = []
    r = (len(img) // 2) - 1

    for alpha in range(0, 180, da):
        xe = r * cos(radians(alpha)) + r
        ye = r * sin(radians(alpha)) + r
        # img[int(xe), int(ye)] = 1
        for i in range(0, n, 1):
            deg = alpha - (phi / 2) + (i * (phi / n))
            xd = r * cos(radians(deg) + pi) + r
            yd = r * sin(radians(deg) + pi) + r
            # img[int(xd), int(yd)] = 0.3
            # print(alpha, deg, xe, ye, xd, yd)
    return