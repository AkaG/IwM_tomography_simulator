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


def calc_weakening(x, y, img, imgcpy, tmp):
    tmp[0] += img[x, y]

    if img[x, y] > 0:
        tmp[1] += 1
    tmp[2] += 1

    imgcpy[x, y] = 1


def generate_sinogram(img, ax=[None, None], step=1, start=0, end=180, n=50, phi=100):
    res = []
    cpy = copy(img)

    # generator = yield_generate_sinogram_cone(img, cpy, step=step, start=start, end=end, n=n, phi=phi)
    generator = yield_generate_sinogram_parallel(img, cpy, step=step, start=start, end=end, n=n, phi=phi)

    for i in range(start, end, step):
        res.append(next(generator))

        if (ax[0] != None and ax[1] != None):
            ax[0].clear()
            ax[1].clear()
            ax[0].imshow(res, cmap=cm.Greys_r, vmin=0, vmax=amax(res))
            ax[1].imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
            plt.pause(0.000001)

    res = divide(res, amax(res))
    return res, cpy


# da - step, n - sensors per step, l - spread
def yield_generate_sinogram_cone(img, imgcpy, step=1, start=0, end=180, n=50, phi=100):
    r = (len(img) // 2)

    for alpha in frange(start, end - 1, step):
        xe = r * cos(radians(alpha)) + r - 1
        ye = r * sin(radians(alpha)) + r - 1
        tmp = []
        for i in range(0, n, 1):
            if n - 1 == 0:
                deg = alpha + (phi / 2)
            else:
                deg = alpha + (phi / 2) - (i * (phi / (n - 1)))
            xd = r * cos(radians(deg) + pi) + r - 1
            yd = r * sin(radians(deg) + pi) + r - 1

            bresenhamret = [0, 0, 0]
            bresenham(int(xe), int(ye), int(xd), int(yd), img,
                      lambda x, y: calc_weakening(x, y, img, imgcpy, bresenhamret))
            tmp.append(bresenhamret[0])
        yield tmp


# da - step, n - sensors per step, l - spread
def yield_generate_sinogram_parallel(img, imgcpy, step=1, start=0, end=180, n=31, phi=150):
    r = (len(img) // 2)

    for alpha in frange(start, end - 1, step):
        tmp = []
        for i in range(0, n, 1):
            if n - 1 == 0:
                deg = phi / 2
            else:
                deg = (phi / 2) - (i * (phi / (n - 1)))

            xe = r * cos(radians(alpha - deg)) + r - 1
            ye = r * sin(radians(alpha - deg)) + r - 1

            xd = r * cos(radians(alpha + deg) + pi) + r - 1
            yd = r * sin(radians(alpha + deg) + pi) + r - 1

            bresenhamret = [0, 0, 0]
            bresenham(int(xe), int(ye), int(xd), int(yd), img,
                      lambda x, y: calc_weakening(x, y, img, imgcpy, bresenhamret))
            tmp.append(bresenhamret[0])
        yield tmp
