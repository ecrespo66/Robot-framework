import os
import string
import random
import time


def KillProcess(process=None, name=None):
    if process:
        return process.kill()
    if name:
        return os.system("taskkill /f /im " + name + " >nul 2>&1")
    return


def Invoke(file):
    os.system('python ' + file)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def Wait(seconds=None):

    time.sleep(seconds)
