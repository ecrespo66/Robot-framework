import os

import pytesseract
from PIL import Image
import fitz
from iBott.files_activities import Folder, PDF


class OCR:
    def __init__(self, path, testData):
        """OCR Constructor.
        :receives path to tesseract binary file and test data to work with different lenaguages"""

        self.path = path
        self.testData = testData
        self.tessdata_dir_config = f"--tessdata-dir '{self.testData}'"

    def read_picture(self, filePath, lang='eng'):
        """Method to convert image to text, :receives path of image to process"""

        pytesseract.pytesseract.tesseract_cmd = self.path
        text = pytesseract.image_to_string(Image.open(filePath), lang=lang, config=self.tessdata_dir_config)
        return text

    def readPdf(self, file, scale=1, lang='eng', foldName=None):
        """Method to convert scanned PDF to text, :receives path of image to process"""

        pages = PDF(file).pages
        doc = fitz.open(file)
        e = scale

        if foldName is None:
            foldName = "Temp"
        else:
            foldName = foldName

        file = os.path.normpath(file).replace("\\", "/")
        folder = file.split("/")[-1] + foldName

        folder = Folder(folder)
        image_matrix = fitz.Matrix(fitz.Identity)
        image_matrix.preScale(e, e)

        for i in range(0, pages):
            page = doc.loadPage(i)
            pix = page.getPixmap(alpha=False, matrix=image_matrix)
            output = folder.path + '/' + str(i) + ".png"
            pix.writePNG(output)

        pics = folder.filelist()
        text = ""
        for i in range(0, len(pics)):
            pic = folder.path + "/" + str(i) + ".png"
            text += "\n" + self.readPicture(pic, lang)
        if foldName + "Temp":
            folder.remove()
        return text


