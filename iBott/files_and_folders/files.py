import os
import uuid
import warnings
from datetime import time
from shutil import copyfile
from time import sleep, ctime


class File:
    """
    Class to handle files.
    Arguments:
        file_path (str): path to the file
    Attributes:
        file_path (str): path to the file
        exists (bool): whether the file exists
        file_name (str): name of the file
        byte_size (int): size of the file in bytes
        creation_datetime (datetime): datetime of the file's creation
        modification_datetime (datetime): datetime of the file's last modification
    Methods:
        rename(new_file_name): renames the file
        move(new_location): moves the file to a new location
        remove(): removes the file
        copy(new_location): copies the file to a new location
        wait_for_file_to_exist(timeout=10): waits for the file to exist
    """

    def __init__(self, path):
        self.path = os.path.normpath(path).replace("\\", "/")
        self.exists = os.path.isfile(self.path)
        self.file_name = self.path.split("/")[-1]
        if self.exists:
            self.byte_size = self.__convert_bytes(os.stat(self.path).st_size)
            self.creation_datetime = ctime(os.path.getctime(self.path))
            self.modification_datetime = ctime(os.path.getmtime(self.path))
        else:
            self.byte_size = None
            self.creation_time = None
            self.modification_time = None

    def __str__(self):
        return f"file: {self.path}"

    def rename(self, new_file_name):
        """
        Rename file
        Arguments:
            new_file_name (str): new name of the file
        """

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
        """
        Move file to new location
        Arguments:
            new_location: new location of file
            """
        new_path = "/".join(new_location, self.file_name)
        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                os.rename(self.path, new_path)
        elif os.path.exists(new_path):
            new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + self.file_name
            os.rename(self.path, new_path)
        self.path = new_path

    def remove(self):
        """
        Remove file
        """
        if os.path.isfile(self.path):
            os.remove(self.path)
        else:
            raise Exception("File doesn't exists")

    def copy(self, new_location=None):
        """
        Copy file into new location, if location is None
        File will be copied into current location
        Arguments:
            new_location (str): new location of file (optional)
        """

        if new_location is None:
            new_location = self.path.replace(self.path.split("/")[-1], "")
            new_path = new_location + "\\" + self.file_name

        if os.path.exists(self.path):
            if not os.path.exists(new_path):
                copyfile(self.path, new_path)
            elif os.path.exists(new_path):
                new_path = new_location + "/" + "(" + str(uuid.uuid4())[:8] + ") " + self.file_name
                copyfile(self.path, new_path)

    def wait_for_file_to_exist(self, timeout=10):
        """
        Wait for file to appear in forlder
        Arguments:
            timeout: time to wait for file to appear
        """
        time = 0
        while not os.path.isfile(self.path):
            sleep(1)
            time += 1
            if time > timeout:
                raise Exception("File didn't appear in folder")
        self.__init__(self.path)

    @staticmethod
    def __convert_bytes(num):
        """
        Convert file to Bytes
        Arguments:
            num (int): file size in bytes
        Returns:
            str: file size in Bytes
        """

        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0
