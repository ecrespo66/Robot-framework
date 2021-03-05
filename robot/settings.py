import os
from pathlib import Path

ROBOT_FOLDER = Path(os.path.dirname(os.path.realpath(__file__)))
CHROMEDRIVER_PATH = os.path.join(ROBOT_FOLDER, "Driver")
