from skimage import data

from sinogram_generator import *


def main():
    image = data.imread("img/Kwadraty2.jpg", as_grey=True)
    fig = plt.figure(1)
    ax = fig.add_subplot(121)
    ax.imshow(image, cmap=cm.Greys_r, vmin=0, vmax=1)

    img = generate_sinogram(image, da=1, n=70, phi=160)
    ax = fig.add_subplot(122)
    ax.imshow(img, cmap=cm.Greys_r, vmin=0, vmax=1)

    plt.show()
    return


if __name__ == '__main__':
    main()
