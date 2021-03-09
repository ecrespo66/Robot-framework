import pyautogui
import subprocess


class Screen:
    """Screen Class find Bitmap elements in Screen"""

    def __init__(self):
        self.screenSize = pyautogui.size()
        self.mousePosition = pyautogui.position()

    @staticmethod
    def click(clicks=1, button='left'):
        """Click method clicks on current mouse position"""

        pyautogui.click(clicks=clicks, button=button)

    @staticmethod
    def moveMouseTo(pos):
        """Moves mouse to position defined as tuple """

        pyautogui.moveTo(pos[0], pos[1])

    @staticmethod
    def dragTo(to, button='left'):
        """Drags element from current mouse position to position defined as tuple.
         **optional define mouse button"""

        pyautogui.dragTo(to[0], to[1], button=button)

    @staticmethod
    def FindElement(image):
        """Find image element in screen, returns position as a tuple"""

        button = pyautogui.locateCenterOnScreen(image)
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 1:
            button = (button[0] / 2, button[1] / 2)
        return button

    @staticmethod
    def write(text):
        """Send text from keyboard"""

        for t in text:
            pyautogui.press(t)

    @staticmethod
    def clickImage(image, clicks=2):
        """Click on image element on Screen"""

        button = Screen.FindElement(image)
        pyautogui.click(button, clicks=clicks)

    @staticmethod
    def shoot(path):
        """Take a screenshoot, receives a path where the element is going to be stored."""

        pyautogui.screenshot(path)
