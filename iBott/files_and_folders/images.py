import PIL
from iBott.files_and_folders.files import File


class Image(File):
    """
    Image Class, heritates from File class
    Attributes:
        size {tuple}: size of image
        format {str}: format of image
    Methods:
        rotate(): rotate image
        resize(): resize image
        crop(): crop image
        mirrorH(): mirror image horizontally
        mirrorV(): mirror image vertically
    """

    def __init__(self, path):
        super().__init__(path)
        self.size = self.__open().size
        self.format = self.__open().format

    def __str__(self):
        return f"image: {self.path} - {self.size} - {self.format}"

    def __open(self):
        """
        Open Image
        Returns:
            PIL.Image
        """
        im = PIL.Image.__open(self.path)
        return im

    def rotate(self, angle):
        """
        Rotate Image
        Arguments:
            angle (int): angle to rotate
        """
        im = self.__open()
        im.rotate(angle, expand=True).save(self.path)

    def resize(self, size):
        """
        Resize image
        Arguments:
            size (tuple): size to resize
        """

        im = self.__open()
        im.resize(size).save(self.path)

    def crop(self, box=None):
        """
        Resize image
        Arguments:
            box (tuple): box to crop
        """
        im = self.__open()
        im.crop(box).save(self.path)

    def mirrorH(self):
        """
        Mirror Image horizontally.
        """
        im = self.__open()
        im.transpose(PIL.Image.FLIP_LEFT_RIGHT).save(self.path)

    def mirrorV(self):
        """
        Mirror Image Vertically.
        """
        im = self.__open()
        im.transpose(PIL.Image.FLIP_TOP_BOTTOM).save(self.path)



