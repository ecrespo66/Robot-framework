import pyautogui
import subprocess


class Screen:
    """
    Screen Class finds and interacts with Bitmap elements on the screen

    """

    screenSize = pyautogui.size()
    mousePosition = pyautogui.position()

    @staticmethod
    def click(clicks=1, button='left'):
        """
        Click method clicks on current mouse position
            :param clicks: number of clicks
            :param button: button to click

            :return: None
        """

        pyautogui.click(clicks=clicks, button=button)

    @staticmethod
    def moveMouseTo(pos):
        """
        Moves mouse to position defined as tuple
            :param pos: position to move to
            :type pos: tuple of int

            :return: None
        """

        pyautogui.moveTo(pos[0], pos[1])

    @staticmethod
    def dragTo(to, button='left'):
        """
        Drags element from current mouse position to position defined as tuple.
            :param to: position to drag to
            :type to: tuple of int

            :param button: button to use for dragging
            :type button: str

            :return: None
        """
        pyautogui.dragTo(to[0], to[1], button=button)

    @staticmethod
    def FindElement(image):
        """
        Find image element in screen, returns position as a tuple
            :param image: image to find
            :type image: str

            :return: position of image
            :rtype: tuple
        """

        button = pyautogui.locateCenterOnScreen(image)
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 1:
            button = (button[0] / 2, button[1] / 2)
        return button

    @staticmethod
    def write(text):
        """
        Send text from keyboard
            :param text: text to send
            :type text: str
            :return: None
        """

        for t in text:
            pyautogui.press(t)

    @staticmethod
    def clickImage(image, clicks=2):
        """
        Click on image element on Screen
            :param image: image to click on
            :type image: str
            :param clicks: number of clicks
            :type clicks: int
        """

        button = Screen.FindElement(image)
        pyautogui.click(button, clicks=clicks)

    @staticmethod
    def shoot(path):
        """
        this function takes a screenshoot of the current screen and saves it to the specified path
        :param path: path to save the screenshot
        :return: None

        """

        pyautogui.screenshot(path)
