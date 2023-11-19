import os
from pathlib import Path

"""Folders to store Chrome"""
ROBOT_FOLDER = Path(os.path.dirname(os.path.realpath(__file__))).parent
CHROMEDRIVER_PATH = os.path.join(ROBOT_FOLDER, "Driver")
