from skimage import data
from pylab import *
import time

from sinogram_generator import *

def setUpPixel(x, y, img, val):
    img[x,y] = val

def main():

    image = data.imread("img/Kropka.jpg", as_grey=True)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bresenham(0, 0, 200, 400, image, lambda x,y : setUpPixel(x,y,image,1.0))

    ax.imshow(image, cmap=cm.Greys_r, vmin=0, vmax=1)
    plt.show()
    return

if __name__ == '__main__':
    main()