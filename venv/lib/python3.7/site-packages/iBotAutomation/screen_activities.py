import pyautogui
import subprocess


class Screen:

    def __init__(self):
        self.screenSize = pyautogui.size()
        self.mousePosition = pyautogui.position()

    @staticmethod
    def click(clicks=1, button='left'):
        pyautogui.click(clicks, button)

    @staticmethod
    def moveMouseTo(pos):
        pyautogui.moveTo(pos[0], pos[1])

    @staticmethod
    def dragTo(to, button='left'):
        pyautogui.dragTo(to[0], to[1], button=button)

    @staticmethod
    def FindElement(image):
        button = pyautogui.locateCenterOnScreen(image)
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0:
            button = (button[0] / 2, button[1] / 2)
        return button

    @staticmethod
    def write(text):
        for t in text:
            pyautogui.press(t)

    @staticmethod
    def click_image(png_name, clicks=2):
        button = pyautogui.locateCenterOnScreen(png_name)
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0:
            button = (button[0] / 2, button[1] / 2)
        pyautogui.click(button, clicks=clicks)
        return

    @staticmethod
    def shoot(path):
        pyautogui.screenshot(path)
