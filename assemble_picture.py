from scipy.linalg._cython_wrapper_generators import dims

from bresenham import *


def draw_func(x, y, img, val):
    img[x, y] += val


def assemble_sinogram(sinogram, imgdims = [None, None], start_deg=0, step=1, phi=100, type=None):
    res = zeros((imgdims[0], imgdims[1]))

    if type == "cone":
        assemble_cone(sinogram, res, start_deg=start_deg, step=step, phi=phi)
    elif type == "parallel":
        assemble_parallel(sinogram, res, start_deg=start_deg, step=step, phi=phi)
    else:
        return None

    res = divide(res, amax(res))
    return res


def assemble_cone(sinogram, drawimg, start_deg=0, step=1, phi=100):
    r = len(drawimg) // 2
    end = start_deg + len(sinogram)

    for alpha, line in zip(frange(start_deg, end, step), sinogram):
        xe = r * cos(radians(alpha)) + r - 1
        ye = r * sin(radians(alpha)) + r - 1
        n = len(line)
        for i in range(0, n, 1):
            if n - 1 == 0:
                deg = alpha + (phi / 2)
            else:
                deg = alpha + (phi / 2) - (i * (phi / (n - 1)))
            xd = r * cos(radians(deg) + pi) + r - 1
            yd = r * sin(radians(deg) + pi) + r - 1

            bresenham(int(xe), int(ye), int(xd), int(yd), drawimg,
                      lambda x, y: draw_func(x, y, drawimg, line[i]))


def assemble_parallel(sinogram, drawimg, start_deg=0, step=1, phi=100):
    r = len(drawimg) // 2
    end = start_deg + len(sinogram)

    for alpha, line in zip(frange(start_deg, end, step), sinogram):
        n = len(line)
        for i in range(0, n, 1):
            if n - 1 == 0:
                deg = phi / 2
            else:
                deg = (phi / 2) - (i * (phi / (n - 1)))

            xe = r * cos(radians(alpha - deg)) + r - 1
            ye = r * sin(radians(alpha - deg)) + r - 1

            xd = r * cos(radians(alpha + deg) + pi) + r - 1
            yd = r * sin(radians(alpha + deg) + pi) + r - 1

            bresenham(int(xe), int(ye), int(xd), int(yd), drawimg,
                      lambda x, y: draw_func(x, y, drawimg, line[i]))
