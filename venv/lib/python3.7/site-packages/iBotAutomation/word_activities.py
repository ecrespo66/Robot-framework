from docx import *
from docx.shared import Inches
from docx.shared import Cm
from docx2pdf import convert
import os
from .files_activities import File


class Word(File):
    def __init__(self, path):
        self.path = path
        self.document = self.file()
        File.__init__(self, path)

    def save(self):
        self.document.save(self.path)

    def file(self):
        if os.path.isfile(self.path):
            doc = Document(self.path)
        else:
            doc = Document()
            doc.save(self.path)
        return doc

    def addHeading(self, text, level=0):
        self.document.add_heading(text, level)

    def addParagraph(self, text, style=None):
        self.document.add_paragraph(text, style=style)

    def addPicture(self, path, width=None, height=None):
        self.document.add_picture(path, width=width)

    def addTable(self, list):

        table = self.document.add_table(rows=len(list), cols=len(list[0]))

        for i in range(len(list)):

            for j in range(len(list[0])):
                table.rows[i].cells[j].text = str(list[i][j])

    def read(self):

        data = ""
        fullText = []
        for para in self.document.paragraphs:
            fullText.append(para.text)
            data = '\n'.join(fullText)

        return data

    def convertToPdf(self):

        self.path.replace('.docx', '.pdf')
        return convert(self.path)
