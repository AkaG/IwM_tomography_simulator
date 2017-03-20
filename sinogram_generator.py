from bresenham import *


def calc_weakening(x, y, img, imgcpy, tmp):
    tmp[0] += img[x, y]

    if img[x, y] > 0:
        tmp[1] += 1
    tmp[2] += 1

    imgcpy[x, y] = 1


def generate_sinogram(img, axis=[None, None], step=1, start=0, end=180, n=50, phi=100, type=None):
    res = []
    cpy = copy(img)

    if type == "cone":
        generator = yield_generate_sinogram_cone(img, cpy, step=step, start=start, end=end, n=n, phi=phi)
    elif type == "parallel":
        generator = yield_generate_sinogram_parallel(img, cpy, step=step, start=start, end=end, n=n, phi=phi)
    else:
        return None, None

    for i in range(start, end, step):
        res.append(next(generator))

        if (axis[0] != None and axis[1] != None):
            axis[0].clear()
            axis[1].clear()
            axis[0].imshow(res, cmap=cm.Greys_r, vmin=0, vmax=amax(res))
            axis[1].imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
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
