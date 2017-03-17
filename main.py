from skimage import data

from sinogram_generator import *


def main():
    image = data.imread("img/Shepp_logan.png", as_grey=True)

    plt.ion()

    fig = plt.figure(1)
    ax = fig.add_subplot(131)
    ax.imshow(image, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.pause(0.0001)

    ax = fig.add_subplot(132)
    ax2 = fig.add_subplot(133)
    axis = [ax, ax2]

    img, cpy = generate_sinogram(image, step=1, start=0, end=180, n=131, phi=150)

    ax.imshow(array(img).transpose(), cmap=cm.Greys_r, vmin=0, vmax=1)
    ax2.imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.pause(0.0001)

    plt.show(block=True)
    return


if __name__ == '__main__':
    main()
