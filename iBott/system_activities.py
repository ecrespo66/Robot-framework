import os
import string
import random
import time


class System:
    @classmethod
    def KillProcess(process=None, name=None):
        """Kill process"""
        if process:
            return process.kill()
        if name:
            return os.system("taskkill /f /im " + name + " >nul 2>&1")
        return

    @classmethod
    def get_args(cls, args):
        """Get arguments from command line"""
        if len(args) > 1:
            args = eval(args[1].replace("'", '"'))
        else:
            args = None
        return args

    @classmethod
    def Invoke(file):
        """Execute python file"""

        os.system('python ' + file)

    @classmethod
    def id_generator(size=6):
        """Generate unique identifier from, receives numer of digits"""

        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def Wait(seconds=None):
        """Wait Seconds, receive number of seconds to wait"""
        time.sleep(seconds)
