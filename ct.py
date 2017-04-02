from skimage import data

from assemble_picture import *
from sinogram_generator import *


class ct():
    def __init__(self):
        self.image = None
        self.sinogram = None
        self.lines = None
        self.reconstruction = None

        self.step = 1
        self.n = 200
        self.phi = 150
        self.type = "parallel"

        # plt.ion()
        #
        # fig = plt.figure(1)
        # ax = fig.add_subplot(231)
        #
        # ax.imshow(image, cmap=cm.Greys_r, vmin=0, vmax=1)
        # plt.pause(0.0001)
        #
        # ax = fig.add_subplot(232)
        # ax2 = fig.add_subplot(233)
        # axis = [ax, ax2]
        #
        # sinogram, cpy = generate_sinogram(image, type=type, step=1, start=0, end=180, n=200, phi=phi)
        #
        # ax.imshow(array(sinogram).transpose(), cmap=cm.Greys_r, vmin=0, vmax=1)
        # ax2.imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
        # plt.pause(0.0001)
        #
        # sinogram = filterSinogram(sinogram, 40)
        # ax = fig.add_subplot(235)
        # ax.imshow(array(sinogram).transpose(), cmap=cm.Greys_r, vmin=amin(sinogram), vmax=amax(sinogram))
        # plt.pause(0.0001)
        #
        # assembled_picture = assemble_sinogram(sinogram, imgdims=array([len(image), len(image)]), type=type, phi=phi)
        # assembled_picture = normalize(assembled_picture)
        # ax = fig.add_subplot(234)
        # ax.imshow(assembled_picture, cmap=cm.Greys_r, vmin=0, vmax=1)
        # plt.pause(0.0001)
        #
        # plt.show(block=True)

    def loadImage(self, imgPath):
        self.image = data.imread(imgPath, as_grey=True)

    def generateSinogram(self, animate=lambda sin, lines: None):
        self.sinogram, self.lines = generate_sinogram(self.image, animation=animate, type=self.type, step=self.step, start=0, end=180, n=self.n, phi=self.phi)

    def filterSinogram(self):
        self.sinogram = filterSinogram(self.sinogram, 40)

    def reconstruct(self):
        self.reconstruction = assemble_sinogram(self.sinogram, imgdims=array([len(self.image), len(self.image)]), type=self.type, phi=self.phi)
        self.reconstruction = normalize(self.reconstruction)
