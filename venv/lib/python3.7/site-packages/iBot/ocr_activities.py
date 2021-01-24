import os
import pytesseract
from PIL import Image
import fitz
import re
from pathlib import Path
from iBot.files_activities import Folder, PDF


class OCR:
    def __init__(self, path):
        self.path = path
        self.testData = str(Path(path).parent.parent) + '/share/tessdata'
        self.tessdata_dir_config = f'--tessdata-dir "{self.testData}"'

    def readPicture(self, filePath, lang='eng'):
        pytesseract.pytesseract.tesseract_cmd = self.path
        text = pytesseract.image_to_string(Image.open(filePath), lang=lang, config=self.tessdata_dir_config)
        return text

    def readPdf(self, file, scale=1, lang='eng', foldName=None):
        pages = PDF(file).pages
        doc = fitz.open(file)
        e = scale

        if foldName is None:
            foldName = "Temp"
        else:
            foldName = foldName
        if "\\" in file:
            folder = file.replace(file.split("\\")[-1], "") + foldName
        elif "/" in file:
            folder = file.replace(file.split("/")[-1], "") + foldName

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


