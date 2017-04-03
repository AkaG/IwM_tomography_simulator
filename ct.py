from dicom.dataset import Dataset, FileDataset
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

        self.pname = ""
        self.plastname = ""
        self.page = ""
        self.pcomment = ""

    def loadImage(self, imgPath):
        self.image = data.imread(imgPath, as_grey=True)

    def saveAsDICOM(self, filename):
        print(filename)

        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here for real work
        file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here

        ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

        ds.PatientID = "123456"
        ds.PatientName = self.pname + "^" + self.plastname
        ds.PatientAge = self.page
        ds.PatientComments = self.pcomment

        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16
        ds.SmallestImagePixelValue = b'\\x00\\x00'
        ds.LargestImagePixelValue = b'\\xff\\xff'

        ds.Rows = self.reconstruction.shape[0]
        ds.Columns = self.reconstruction.shape[1]

        if self.image.dtype != np.uint16:
            ds.PixelData = multiply(self.reconstruction, np.iinfo(np.uint16).max).astype(np.uint16)
        else:
            ds.PixelData = self.reconstruction

        ds.is_little_endian = True
        ds.is_implicit_VR = True

        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        ds.ContentTime = timeStr

        ds.save_as(filename)

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
