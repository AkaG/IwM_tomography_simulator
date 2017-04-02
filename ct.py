from skimage import data

from assemble_picture import *
from sinogram_generator import *


class ct():
    def __init__(self):
        self.image = None
        self.sinogram = None
        self.filteredsinogram = None
        self.lines = None
        self.reconstruction = None
        self.reconstructionDiff = None

        self.step = 1
        self.n = 200
        self.phi = 150
        self.type = "parallel"

    def loadImage(self, imgPath):
        self.image = data.imread(imgPath, as_grey=True)

    def generateSinogram(self, animate=lambda sin, lines: None):
        self.sinogram, self.lines = generate_sinogram(self.image, animation=animate, type=self.type, step=self.step, start=0, end=180,
                                                      n=self.n, phi=self.phi)

    def filterSinogram(self, masklen=40):
        self.filteredsinogram = filterSinogram(self.sinogram, masklen)

    def reconstruct(self):
        self.reconstruction = assemble_sinogram(self.filteredsinogram, imgdims=array([len(self.image), len(self.image)]), type=self.type,
                                                phi=self.phi)
        self.reconstruction = normalize(self.reconstruction)

    def generateDiff(self):
        self.reconstructionDiff = normalize(subtract(self.image, self.reconstruction))
