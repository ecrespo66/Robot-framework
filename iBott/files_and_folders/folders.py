import os
import shutil
import uuid
import requests
from iBott.files_and_folders.files import File


class Folder:
    """
    Folder Class.
    If folder doesn't exist it automatically creates a new one.
    Arguments:
       path {string} -- path to folder to be instanced.
    Attributes:
       path {string} -- path to folder to be instanced.
       name {string} -- name of folder
    Methods:
       rename(new_folder_name) : Rename folder
       move(new_location): move folder to new location
       remove(allow_root=False, delete_read_only=True) : remove folder and all files and folders inside
       empty(allow_root=False): delete all files and folders in folder, receives allow_root as parameter
       copy(new_location=None) : Copy folder to new location
       subfolder_list(): list of subfolders
       file_list(): list of files in folder
       download_file(url, name=None): downloads file from url
    """
    def __init__(self, path):
        self.path = os.path.normpath(path).replace("\\", "/")
        if not os.path.exists(self.path):
            os.makedirs(path)
        self.name = path.split("/")[-1:]

    def __str__(self):
        return f"folder: {self.path}"

    def rename(self, new_folder_name):
        """
        Rename folder
        Arguments:
            new_folder_name {string} -- new name of folder
        """

        base_path = self.path.split("/")[:-1]
        new_path = "/".join(base_path) + "/" + new_folder_name
        if not os.path.exists(new_path):
            os.rename(self.path, new_path)
        self.path = new_path

    def move(self, new_location):
        """
        Move folder to new location
        Arguments:
            new_location {string} -- new location of folder
        """

        new_path = new_location + "/" + self.name
        if os.path.isdir(self.path):
            if not os.path.isdir(new_path):
                os.rename(self.path, new_path)
            elif os.path.isdir(new_path):
                new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                os.rename(self.path, new_path)
        self.path = new_path

    def remove(self, allow_root=False, delete_read_only=True):
        """
        Remove folder
        Arguments:
            allow_root {bool} -- allow root folder to be removed
            delete_read_only {bool} -- delete read only files
        """

        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path, ignore_errors=delete_read_only)

    def empty(self, allow_root=False):
        """
        Delete all files and folders in folder, receives allow_root as parameter
        Arguments:
            allow_root {bool} -- allow root folder to be removed
        """

        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                for root, dirs, files in os.walk(self.path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))

    def copy(self, new_location=None):
        """
        Copy folder  into new location, if new_location is none,
        folder will be cloned into current directory
        Arguments:
            new_location {string} -- new location of folder
        """

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

    def subfolder_list(self):
        """
        Get list of subfolders in folder
        Returns:
            list -- list of subfolders
        """
        subfolders = [Folder(f.path) for f in os.scandir(self.path) if f.is_dir()]
        return subfolders

    def file_list(self):
        """
        Get List of files, in folder
        Returns:
            list -- list of files
        """

        file_list = []
        for file in os.listdir(self.path):
            if File[0] != ".":
                file_list.append(File(self.path + "\\" + file))
        return file_list

    def download_file(self, url, name=None):
        """
        Download file from url
        Arguments:
            url {string} -- url of file to be downloaded
            name {string} -- name of file to be downloaded (optional)
        """

        if not name:
            filename = self.path + "/" + name
        else:
            filename = self.path + "/" + str(url).split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        return File(filename)
