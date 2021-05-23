import os
import shutil
import time
import warnings
import requests
import PyPDF2
import PIL
import uuid
from shutil import copyfile


class File:
    def __init__(self, path):
        self.path = os.path.normpath(path).replace("\\", "/")
        self.exists = os.path.isfile(self.path)
        self.fileName = self.path.split("/")[-1]
        if self.exists:
            self.byteSize = self.__convert_bytes(os.stat(self.path).st_size)
            self.creationTime = time.ctime(os.path.getctime(self.path))
            self.modificationTime = time.ctime(os.path.getmtime(self.path))
        else:
            self.byteSize = None
            self.creationTime = None
            self.modificationTime = None

    def rename(self, new_file_name):
        """Rename file receives  new file name."""

        if os.path.isfile(self.path):
            base_path = self.path.split("/")[:-1]
            new_path = "/".join(base_path) + "/" + new_file_name
        else:
            warnings.warn("File doesn't exists")
        if not os.path.exists(new_path):
            os.rename(self.path, new_path)
        else:
            warnings.warn("File already exists in destination folder")
        self.path = new_path

    def move(self, new_location):
        """Move file to new location"""

        new_path = "/".join(new_location, self.fileName)

        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                os.rename(self.path, new_path)
        elif os.path.exists(new_path):
            new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + self.fileName
            os.rename(self.path, new_path)
        self.path = new_path

    def remove(self):
        """Remove file"""

        if os.path.isfile(self.path):
            os.remove(self.path)
        else:
            warnings.warn("File doesn't exists")

    def copy(self, new_location=None):
        """copy file into new location, if location is None
            File will be copyed into current location"""

        if new_location is None:
            new_location = self.path.replace(self.path.split("/")[-1], "")
            new_path = new_location + "\\" + self.fileName

        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                copyfile(self.path, new_path)
            elif os.path.exists(new_path):
                new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + self.fileName
                copyfile(self.path, new_path)

    def waitFor(self):
        """Wait for file to appear in forlder"""

        from time import sleep
        while not os.path.isfile(self.path):
            sleep(1)
        self.__init__(self.path)

    @staticmethod
    def __convert_bytes(num):
        """Convert file to Bytes"""

        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0


class PDF(File):
    def __init__(self, path):
        """PDF Constructor Heritates from File Class"""
        super().__init__(path)
        self.pages = PyPDF2.PdfFileReader(open(path, "rb")).getNumPages() - 1
        self.info = PyPDF2.PdfFileReader(open(path, "rb")).getDocumentInfo()

    def read_page(self, pageNum, encoding=None):
        """Read page from PDF, receives number of page to receive and encofing
        :returns text from PDF"""

        if encoding is None:
            encoding = "utf-8"
        with open(self.path, "rb") as file:
            pdf = PyPDF2.PdfFileReader(file)
            page = pdf.getPage(pageNum)
            text = page.extractText().encode(encoding)
            if text is None:
                raise ValueError("Pdf not readable with this method, use OCR instead")
            return text

    def merge(self, pdf_document2, merged_path):
        """Append new pdf to current and store it as a new one."""

        from PyPDF2 import PdfFileMerger
        pdfs = [str(self.path), str(pdf_document2)]
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(merged_path)

    def spit(self):
        """Split pdf into multiple pages with format: pdfName_n.pdf"""

        pdf = PyPDF2.PdfFileReader(self.path)
        for page in range(self.pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = '{}_page_{}.pdf'.format(self.fileName, page + 1)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)


class Image(File):
    def __init__(self, path):
        """Image constructor, heritates from File"""

        super().__init__(path)
        self.size = self.__open().size
        self.format = self.__open().format

    def __open(self):
        """Open Image"""
        im = PIL.Image.__open(self.path)
        return im

    def rotate(self, angle):
        """Rotate Image, receives angle as integer to rotate"""

        im = self.__open()
        return im.rotate(angle, expand=True).save(self.path)

    def resize(self, size):
        """Resize image. receives size a tuple as size"""

        im = self.__open()
        return im.resize(size).save(self.path)

    def crop(self, box=None):
        """Resize image. receives a tuple as box"""

        im = self.__open()
        return im.crop(box).save(self.path)

    def mirrorH(self):
        """Mirror Image horizontally."""

        im = self.__open()
        return im.transpose(PIL.Image.FLIP_LEFT_RIGHT).save(self.path)

    def mirrorV(self):
        """Mirror Image Vertically."""
        im = self.__open()
        return im.transpose(PIL.Image.FLIP_TOP_BOTTOM).save(self.path)


class Folder:
    def __init__(self, path):
        """Instance folder Class. If folder doesn't exists it automatically creates a new one"""

        self.path = os.path.normpath(path).replace("\\", "/")
        if not os.path.exists(self.path):
            os.makedirs(path)
        self.name = path.split("/")[-1:]

    def rename(self, new_folder_name):
        """Rename folder :receives new_folder_name as parameter"""

        base_path = self.path.split("/")[:-1]
        new_path = "/".join(base_path) + "/" + new_folder_name
        if not os.path.exists(new_path):
            os.rename(self.path, new_path)
        self.path = new_path

    def move(self, new_location):
        """Move folder to new location"""

        new_path = new_location + "/" + self.name
        if os.path.isdir(self.path):
            if not os.path.isdir(new_path):
                os.rename(self.path, new_path)
            elif os.path.isdir(new_path):
                new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                os.rename(self.path, new_path)
        self.path = new_path

    def remove(self, allow_root=False, delete_read_only=True):
        """Remove folder, receives allow_root and delete_read_only as parameters """

        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path, ignore_errors=delete_read_only)

    def empty(self, allow_root=False):
        """Delete all files and folders in folder, receives allow_root as parameter"""

        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                for root, dirs, files in os.walk(self.path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))

    def copy(self, new_location=None):
        """Copy folder  into new location, if new_location is none,
         folder will be cloned into current directory"""

        if new_location is None:
            new_location = self.path.replace(self.path.split("/")[-1], "")
        new_path = "/".join(new_location, self.name)
        if os.path.isdir(self.path):
            if not os.path.isdir(new_path):
                shutil.copytree(self.path, new_path)
            elif os.path.isdir(new_path):
                if os.path.isdir(new_path):
                    new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                shutil.copytree(self.path, new_path)

    def listSubFolders(self):
        """Get list of subfolders :returns array of folder objects"""

        subfolders = [Folder(f.path) for f in os.scandir(self.path) if f.is_dir()]
        return subfolders

    def filelist(self):
        """Get List of files, Returns array of File Objects"""

        FileList = []
        for file in os.listdir(self.path):
            if File[0] != ".":
                FileList.append(File(self.path + "\\" + file))
        return FileList

    def downloadFile(self, url, name=None):
        """Download file from url, receives url and file_name :return file object"""

        if not name:
            filename = self.path + "/" + name
        else:
            filename = self.path + "/" + str(url).split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        return File(filename)
