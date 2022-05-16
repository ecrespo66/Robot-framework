import os

import numpy as np
import pytesseract
from PIL import Image
import fitz
from iBott.files_and_folders.folders import Folder
from iBott.files_and_folders.pdfs import PDF
import cv2




class OCR:
    """
    This class is used to perform OCR on a pdf or an image file.
    It uses tesseract technology to convert images to text.
    Arguments:
        path (engine): The path to the file OCR engine .

    Methods:
        set_config(config): Sets the config for the OCR engine.
        read_picture(file_path, lang): Reads a picture and returns the text.
        read_pdf(file_path, scale, lang): Reads a pdf and returns the text.
        to_grayscale(file_path): Converts an image to grayscale.
        remove_noise(file_path): Removes noise from an image.
        thresholding(file_path): Thresholds an image.
        canny(file_path): Performs canny edge detection on an image.
        deskew(file_path): Deskews an image.
        opening(file_path): Performs an opening on an image.
        erode(file_path): Erodes an image.
        dilate(file_path): Dilates an image.
        opening(file_path): Performs an opening on an image.
    """

    def __init__(self, path=None):
        """
        Constructor
        Arguments:
            path (str): The path to the OCR engine.
        """
        if path:
            pytesseract.pytesseract.tesseract_cmd = path
        self.custom_config = '--psm 6'

    def set_config(self, config):
        self.custom_config = config

    def read_picture(self, file_path, lang='eng'):
        """
        Method to convert image to text
        Arguments:
            file_path (str): image object OCR'd.
            lang (str): The language to be used for OCR.
        Returns:
            text: The text extracted from the image.
        """
        image = cv2.imread(file_path)
        text = pytesseract.image_to_string(image, lang=lang, config=self.custom_config)
        return text

    def read_pdf(self, file_path, scale=1, lang='eng'):
        """Method to convert scanned PDF to text
        Arguments:
            file_path (str): The path to the file to be read.
            scale (int): The scale of the PDF.
            lang (str): The language of the PDF.
        Returns:
            text: The text extracted from the PDF.

        """

        pages = PDF(file_path).pages
        doc = fitz.open(file_path)
        e = scale

        foldName = "Temp"
        file = os.path.normpath(file_path).replace("\\", "/")
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

    @staticmethod
    def to_grayscale(file_path):
        """
        Method to convert an image to grayscale.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(file_path, gray)

    @staticmethod
    def remove_noise(file_path):
        """
        Method to remove noise from an image.
        Arguments:
            file_path (str): The path to the image.
        Returns:
            image: The image with noise removed.
        """
        image = cv2.imread(file_path)
        img = cv2.medianBlur(image, 5)
        cv2.imwrite(file_path, img)

    @staticmethod
    def thresholding(file_path):
        """
        Method to threshold an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        thresholding = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.imwrite(file_path, thresholding)

    @staticmethod
    def canny(file_path):
        """
        Method to perform canny edge detection on an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        canny = cv2.Canny(image, 100, 200)
        cv2.imwrite(file_path, canny)

    @staticmethod
    def deskew(file_path):
        """
        Method to deskew an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(file_path, rotated)

    @staticmethod
    def opening(file_path):
        """
        Method to remove noise from an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        cv2.imwrite(file_path, opening)

    @staticmethod
    def erode(file_path):
        """
        Method to erode an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        kernel = np.ones((5, 5), np.uint8)
        erode = cv2.erode(image, kernel, iterations=1)
        cv2.imwrite(file_path, erode)

    @staticmethod
    def dilate(file_path):
        """
        Method to dilate an image.
        Arguments:
            file_path (str): The path to the image.
        """
        image = cv2.imread(file_path)
        kernel = np.ones((5, 5), np.uint8)
        dilate = cv2.dilate(image, kernel, iterations=1)
        cv2.imwrite(file_path, dilate)


if __name__ == "__main__":
    ocr = OCR()
    print(ocr.read_picture("/Users/enriquecrespodebenito/Desktop/pyseract_test.jpeg", "eng"))
