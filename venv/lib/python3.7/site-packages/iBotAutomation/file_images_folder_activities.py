import PyPDF2
import os
import time

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

class File:

    def __init__(self , path):
        
        self.exists = os.path.isfile(path)
        self.path = path
        self.byteSize =convert_bytes(os.stat(path).st_size) 
        self.creationTime = time.ctime(os.path.getctime(path))
        self.modificationTime = time.ctime(os.path.getmtime(path))
        
  
    def Open(self):
        if os.path.isfile(self.path):
            os.startfile(self.path)
        return
    
    
    def rename(self, new_file_name):
        old_path = self.path
        if os.path.isfile(old_path):
            base_path = old_path.split("\\")[:-1]
            new_path = "\\".join(base_path)+"\\" + new_file_name
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
        return
        

    def move(self, new_location):
        import uuid
        self.path = old_path
        name = old_path.split("\\")[-1]
        new_path = new_location + "\\" + name
        if os.path.exists(old_path):
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
        elif os.path.exists(new_path):
            new_path = new_location + "\\" + \
                "(" + str(uuid.uuid4())[:8] + ") " + name
            os.rename(old_path, new_path)
        return


    def remove(self):

        if os.path.isfile(self.path):
            os.remove(self.path)
        return

    
    def copy(self, new_path):
        from shutil import copyfile
        copyfile(self.path, new_path)



    def WaitFor(self):
        from time import sleep
        while not os.path.exists(self.path):
            sleep(1)
        return


# llama a la funcion downloadfiles para bajar archivos de la web, recibe 2 argumentos obligatorios y un argumento opcional.
# los argumentos son obligatorios son: la url y la ruta donde se encuentra alojado el archivo
# El arcgumento opcional es el nombre del archivo "name", en caso de no recibir name, se asignará automaticamente un nombre


def downloadfiles(url , path, **kwargs):
    import requests
    
    name= kwargs.get('name', None)
    
    if name == False:
        filename= path + "/" + name
    else:
        filename = path + "/" + str(url).split('/')[-1]
        
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    
    return filename


#The first two arguments are the PDF's that need to be merged, entered as a path. The pages from pdf2 
#will be added to pdf2. The merged PDF receives a new path specefied by the third argument.


class PDF(File):
    
    def __init__(self, path):

        File.__init__(self,path)

        self.path = path
        self.pages =  PyPDF2.PdfFileReader(open(path, "rb")).getNumPages()-1
        self.info = PyPDF2.PdfFileReader(open(path, "rb")).getDocumentInfo()
        return
        
    def readPage(self, pageNum):
        with open(self.path, "rb") as filehandle:
            pdf = PdfFileReader(filehandle)
            page = pdf.getPage(pageNum)
            text= page.extractText()
            return text
        
    def merge(self, pdf_document2, merged_path):
        from PyPDF2 import PdfFileMerger
        
        pdfs = [str(self.path), str(pdf_document2)]
        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append(pdf)

        merger.write(merged_path)
        return


import sys
import PIL


# Displays an image specified by the path variable on the default imaging program.
class Image(File):
    def __init__(self,path):

        File.__init__(self,path)

        self.size= str(Image.open(path).size)
        self.format = Image.open(path).format
        
        
    def open(self):
        im = Image.open(self.path)
        return im.show()

# Entering "C:\\Users\\Pictures\\Automagica.jpg" as path and an a angle of 90 rotates the picture specified by the first
# argument over 90 degrees. Pay attention, because angles other than 90, 180, 270, 360 can resize the picture. 
    
    def rotate(self, angle):
        im = Image.open(self.path)
        return im.rotate(angle, expand=True).save(self.path)
    
# Resizes the image specified by the path variable. The size is specifie by the second argument. This is a tuple with the
# width and height in pixels. E.g. ResizeImage("C:\\Users\\Pictures\\Automagica.jpg", (300, 400)) gives the image a width
# of 300 pixels and a height of 400 pixels.

    def resize(self, size):
        im = Image.open(self.path)
        return im.resize(size).save(self.path)
    


# Crops the image specified by path to a region determined by the box variable. This variable is a 4 tuple who defines the
# left, upper, right and lower pixel coördinate e.g.: (left, upper, right, lower).

    def crop(path, box=None):
 

        im = Image.open(path)
        return im.crop(box).save(path)



# Mirrors an image with a given path from left to right.

    def mirrorH(self):
        im = Image.open(self.path)
        return im.transpose(Image.FLIP_LEFT_RIGHT).save(self.path)

#    Mirrors an image with a given path from top to bottom.

    def mirrorV(self):
        im = Image.open(self.path)
        return im.transpose(Image.FLIP_TOP_BOTTOM).save(path)



    
class Folder:
    def __init__(self,path):
        self.path = path
        self.name = path.split("\\")[-1:]
        self.exists = os.path.isdir(path)
        self.fileList = self.filelist()                       
        self.subFoldersList = self.listSubFolders()
                                   
                                                                   
# Entering "C:\\Users\\OldFolder as old_path" and "NewFolder" as new_folder_name changes
# the name of the directory in C:\\Users from "OldFolder" to "NewFolder".

    def rename(self, new_folder_name):

        old_path= self.path
        if os.path.exists(old_path):
            base_path = old_path.split("\\")[:-1]
            new_path = "\\".join(base_path)+"\\" + new_folder_name
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
        return new_path

# Entering "C:\\Users\\Downloads\\Automagica" will open the folder "Automagica" if the path exists.
    
    def open(self):
        if os.path.isdir(self.path):
            os.startfile(self.path)
        return

# Entering "C:\\Users\\Oldlocation\\Automagica" as old_path and "C:\\Users\\Newlocation"
# as new_location moves the folder "Automagica" from directory "Oldlocation" to directory "Newlocation".
# If the new location already contains a folder with the same name, a random 8 character uid is added to the name.

    def move(self, new_location):

        old_path = self.path
        import uuid
        name = old_path.split("\\")[-1]
        new_path = new_location + "\\" + name
        if os.path.isdir(old_path):
            if not os.path.isdir(new_path):
                os.rename(old_path, new_path)
            elif os.path.isdir(new_path):
                new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                os.rename(old_path, new_path)
        return

# Entering "C:\\Users\\Documents\\Automagica" removes the folder "Automagica" including all of its subdirectories and files.
# Standard, the safety variable allow_root is False. When False the function checks whether the path lenght has a minimum of 10 characters. 
# This is to prevent entering for example "\\" as a path resulting in deleting the root and all of its subdirectories.
# To turn off this safety check, explicitly set allow_root to True. For the function to work optimal, all files present in the
# directory must be closed.


    def remove(self, allow_root=False, delete_read_only=True):
        
        if len(self.path) > 10 or allow_root:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path, ignore_errors=delete_read_only)
        return
    
# Entering "C:\\Users\\Documents\\Automagica" removes all the files and folders saved in the "Automagica" folder but maintains the folder itself.
# Standard, the safety variable allow_root is False. When False the function checks whether the path lenght has a minimum of 10 characters. 
# This is to prevent entering for example "\\" as a path resulting in deleting the root and all of its subdirectories.
# To turn off this safety check, explicitly set allow_root to True. For the function to work optimal, all files present in the directory
# must be closed.

    def empty(self, allow_root=False):
        path = self.path
        if len(path) > 10 or allow_root:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
        return
    
    
# By entering "C:\\Users\\Documents\\Automagica" as old_path and "C:\\Users\\Downloads" as new_location...
# the function copies the folder "Automagica" together with all its contents to the new location. The folder name...
# remains unchanged, except when the folder already exists a 8 character random uid will be added to the name.

    def copy(self, new_location):
        
        old_path= self.path
        
        import uuid
        new_path = new_location + "\\" + old_path.split("\\")[-1]
        if os.path.isdir(old_path):
            if not os.path.isdir(new_path):
                shutil.copytree(old_path, new_path)
            elif os.path.isdir(new_path):
                if os.path.isdir(new_path):
                    new_path = new_path + " (" + str(uuid.uuid4())[:8] + ")"
                shutil.copytree(old_path, new_path)
        return



    def listSubFolders(self):
        subfolders = [f.path for f in os.scandir(self.path) if f.is_dir() ]  
        return subfolders


    def filelist(self):
            import pathlib
            #path = pathlib.Path(self.path)
            FileList= []
            for File in  os.listdir(self.path):
                if File[0] != ".":
                    FileList.append(self.path + "/" + File)
            return FileList


    # Creates new folder at the given path          
    def create(self):
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            return self.path
            


        





