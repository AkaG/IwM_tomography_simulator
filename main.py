from numpy.core.multiarray import zeros
from skimage import data

from assemble_picture import *
from sinogram_generator import *


def main():
    image = data.imread("img/Kwadraty2.jpg", as_grey=True)

    plt.ion()

    fig = plt.figure(1)
    ax = fig.add_subplot(231)
    ax.imshow(image, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.pause(0.0001)

    ax = fig.add_subplot(232)
    ax2 = fig.add_subplot(233)
    axis = [ax, ax2]

    phi = 120
    type = "parallel"
    sinogram, cpy = generate_sinogram(image, type=type, step=1, start=0, end=180, n=80, phi=phi)

    ax.imshow(array(sinogram).transpose(), cmap=cm.Greys_r, vmin=0, vmax=1)
    ax2.imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.pause(0.0001)

    # assembled_picture = zeros((len(image),len(image)))
    # assemble_parallel(sinogram, assembled_picture, start_deg=0, rotate_degs=180, phi=180)
    # ax = fig.add_subplot(234)
    # ax.imshow(assembled_picture, cmap=cm.Greys_r, vmin=0, vmax=amax(assembled_picture))

    assembled_picture = assemble_sinogram(sinogram, imgdims=array([len(image),len(image)]), type=type, phi=phi)
    ax = fig.add_subplot(234)
    ax.imshow(assembled_picture, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.pause(0.0001)

    plt.show(block=True)
    return


if __name__ == '__main__':
    main()
