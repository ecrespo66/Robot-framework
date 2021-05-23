import base64
import os
import string
import random
import time
from iBott.files_activities import Folder
import robot.settings as settings


def KillProcess(process=None, name=None):
    """Kill process"""

    if process:
        return process.kill()
    if name:
        return os.system("taskkill /f /im " + name + " >nul 2>&1")
    return


def Invoke(file):
    """Execute python file"""

    os.system('python ' + file)


def id_generator(size=6):
    """Generate unique identifier from, receives numer of digits"""

    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def Wait(seconds=None):
    """Wait Seconds, receive number of seconds to wait"""

    time.sleep(seconds)


def saveFileFromOrchestrator(string):
    folder = Folder(settings.FILES_PATH)
    base = string.split(",")[-1]
    filename = string.split(",")[0]
    file = base64.b64decode(base)
    f = open(os.path.join(folder.path, filename), "wb")
    f.write(file)
    f.close()
