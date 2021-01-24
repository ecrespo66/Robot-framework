import os
import shutil
import time
import requests
import PyPDF2
import PIL
from shutil import copyfile


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


class File:

    def __init__(self, path):
        self.path = path
        self.exists = os.path.isfile(self.path)
        if self.exists:
            self.byteSize = convert_bytes(os.stat(path).st_size)
            self.creationTime = time.ctime(os.path.getctime(path))
            self.modificationTime = time.ctime(os.path.getmtime(path))
        else:
            self.byteSize = None
            self.creationTime = None
            self.modificationTime = None

    def rename(self, new_file_name):
        old_path = self.path
        if os.path.isfile(old_path):
            if "\\" in old_path:
                base_path = old_path.split("\\")[:-1]
                new_path = "\\".join(base_path) + "\\" + new_file_name
            elif "/" in old_path:
                base_path = old_path.split("/")[:-1]
                new_path = "/".join(base_path) + "/" + new_file_name

        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
        self.path = new_path

    def move(self, new_location):
        import uuid
        if "\\" in self.path:
            name = self.path.split("\\")[-1]
            new_path = new_location + "\\" + name
        elif "/" in self.path:
            name = self.path.split("/")[-1]
            new_path = new_location + "/" + name

        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                os.rename(self.path, new_path)
        elif os.path.exists(new_path):
            if "\\" in self.path:
                new_path = new_location + "\\" + "(" + str(uuid.uuid4())[:8] + ") " + name
            elif "/" in self.path:
                new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + name
            os.rename(self.path, new_path)

        self.path = new_path

    def remove(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def copy(self, new_location=None):
        import uuid
        if new_location is None:
            if "\\" in self.path:
                new_location = self.path.replace(self.path.split("\\")[-1], "")
            elif "/" in self.path:
                new_location = self.path.replace(self.path.split("/")[-1], "")

        if "\\" in self.path:
            name = self.path.split("\\")[-1]
            new_path = new_location + "\\" + name
        elif "/" in self.path:
            name = self.path.split("/")[-1]
            new_path = new_location + "/" + name

        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                copyfile(self.path, new_path)
            elif os.path.exists(new_path):
                if "\\" in self.path:
                    new_path = new_location + "\\" + "(" + str(uuid.uuid4())[:8] + ") " + name
                elif "/" in self.path:
                    new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + name
                copyfile(self.path, new_path)

    def waitFor(self):
        from time import sleep
        while not os.path.isfile(self.path):
            sleep(1)
        self.__init__(self.path)


class PDF(File):
    def __init__(self, path):
        File.__init__(self, path)
        self.path = path
        self.pages = PyPDF2.PdfFileReader(open(path, "rb")).getNumPages() - 1
        self.info = PyPDF2.PdfFileReader(open(path, "rb")).getDocumentInfo()
        return

    def readPage(self, pageNum, encoding=None):
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
        from PyPDF2 import PdfFileMerger
        pdfs = [str(self.path), str(pdf_document2)]
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(merged_path)
        return


class Image(File):
    def __init__(self, path):
        File.__init__(self, path)
        self.size = self.open().size
        self.format = self.open().format

    def open(self):
        im = PIL.Image.open(self.path)
        return im

    def rotate(self, angle):
        im = self.open()
        return im.rotate(angle, expand=True).save(self.path)

    def resize(self, size):
        im = self.open()
        return im.resize(size).save(self.path)

    def crop(self, box=None):
        im = self.open()
        return im.crop(box).save(self.path)

    # Mirrors an image with a given path from left to right.

    def mirrorH(self):
        im = self.open()
        return im.transpose(PIL.Image.FLIP_LEFT_RIGHT).save(self.path)

    #    Mirrors an image with a given path from top to bottom.
    def mirrorV(self):
        im = self.open()
        return im.transpose(PIL.Image.FLIP_TOP_BOTTOM).save(self.path)


class Folder:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(path)
        if "\\" in path:
            self.name = path.split("\\")[-1:]
        elif "/" in path:
            self.name = path.split("/")[-1:]

    def rename(self, new_folder_name):
        old_path = self.path
        if os.path.exists(old_path):
            if "\\" in old_path:
                base_path = old_path.split("\\")[:-1]
                new_path = "\\".join(base_path) + "\\" + new_folder_name
            elif "/" in old_path:
                base_path = old_path.split("/")[:-1]
                new_path = "/".join(base_path) + "/" + new_folder_name

            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
        self.path = new_path

    def move(self, new_location):
        old_path = self.path
        import uuid
        if "\\" in old_path:
            name = old_path.split("\\")[-1]
            new_path = new_location + "\\" + name
        elif "/" in old_path:
            name = old_path.split("/")[-1]
            new_path = new_location + "/" + name

        if os.path.isdir(old_path):
            if not os.path.isdir(new_path):
                os.rename(old_path, new_path)
            elif os.path.isdir(new_path):
                new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                os.rename(old_path, new_path)
        self.path = new_path

    def remove(self, allow_root=False, delete_read_only=True):
        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path, ignore_errors=delete_read_only)
        return

    def empty(self, allow_root=False):
        path = self.path
        if len(path) > 10 or allow_root:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))

    def copy(self, new_location = None):
        import uuid
        if new_location is None:
            if "\\" in self.path:
                new_location = self.path.replace(self.path.split("\\")[-1], "")
            elif "/" in self.path:
                new_location = self.path.replace(self.path.split("/")[-1], "")
        if "\\" in new_location:
            new_path = new_location + "\\" + self.path.split("\\")[-1]
        elif "/" in new_location:
            new_path = new_location + "/" + self.path.split("/")[-1]
        if os.path.isdir(self.path):
            if not os.path.isdir(new_path):
                shutil.copytree(self.path, new_path)
            elif os.path.isdir(new_path):
                if os.path.isdir(new_path):
                    new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                shutil.copytree(self.path, new_path)

    def listSubFolders(self):
        subfolders = [f.path for f in os.scandir(self.path) if f.is_dir()]
        return subfolders

    def filelist(self):
        FileList = []
        for File in os.listdir(self.path):
            if File[0] != ".":
                FileList.append(self.path + "/" + File)
        return FileList

    def downloadFile(self, url, name=None):
        if not name:
            filename = self.path + "/" + name
        else:
            filename = self.path + "/" + str(url).split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        return filename
