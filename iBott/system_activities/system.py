import os
import string
import random
import sys
import time


class System:

    @staticmethod
    def KillProcess(process=None, name=None):
        """Kill process"""
        if process:
            return process.kill()
        if name:
            return os.system("taskkill /f /im " + name + " >nul 2>&1")
        return

    @staticmethod
    def Invoke(file):
        """Execute python file"""

        os.system('python ' + file)

    @staticmethod
    def id_generator(size=6):
        """Generate unique identifier from, receives numer of digits"""

        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def Wait(seconds=None):
        """Wait Seconds, receive number of seconds to wait"""
        time.sleep(seconds)

    @staticmethod
    def get_OS():
        """Get current system"""
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'Linux'
        elif sys.platform == 'darwin':
            platform = 'Mac'
        elif sys.platform.startswith('win'):
            platform = 'Windows'
        else:
            raise RuntimeError('Could not determine  Operative system.')
        return platform
