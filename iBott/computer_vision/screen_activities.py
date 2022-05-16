import pyautogui
import subprocess


class Screen:
    """
    Screen Class finds and interacts with Bitmap elements on the screen.
    Attributes:
        screen_size (tuple): The size of the screen.
        mousePosition (tuple): The position of the mouse.
    Methods:
        click(clicks, button) - Perform click action on the screen.
        move_mouse_to(pos) - Move mouse to the specified position.
        drag_mouse_to(pos) - Drag mouse to the specified position.
        find_element(image_path) - Find the specified element on the screen.
        write(text) - Write text to the screen.
        click_image(image_path) - Click the specified image on the screen.
        shoot(image_path) - Take a screenshot of the screen.
    """
    screenSize = pyautogui.size()
    mousePosition = pyautogui.position()

    @staticmethod
    def click(clicks=1, button='left'):
        """
        Click method clicks on current mouse position
        Arguments:
            clicks: number of clicks
            button: button to click with (default: left)
        """

        pyautogui.click(clicks=clicks, button=button)

    @staticmethod
    def move_mouse_to(pos):
        """
        Moves mouse to position defined as tuple
        Arguments:
            pos: position to move to as tuple
        """

        pyautogui.moveTo(pos[0], pos[1])

    @staticmethod
    def drag_mouse_to(to, button='left'):
        """
        Drags element from current mouse position to position defined as tuple.
        Arguments:
            to: position to drag to as tuple
            button: button to drag with (default: left)
        """
        pyautogui.dragTo(to[0], to[1], button=button)

    @staticmethod
    def find_element(image_path):
        """
        Find image element in screen, returns position as a tuple
        Arguments:
            image_path: image to find
        """

        element = pyautogui.locateCenterOnScreen(image_path)
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 1:
            element = (element[0] / 2, element[1] / 2)
        return element

    @staticmethod
    def write(text):
        """
        Send text from keyboard
        Arguments:
            text: text to send
        """

        for t in text:
            pyautogui.press(t)

    @staticmethod
    def click_image(image_path, clicks=2):
        """
        Click on image element on Screen
        Arguments:
            image: image to click on
            clicks: number of clicks

        """

        button = Screen.FindElement(image_path)
        pyautogui.click(button, clicks=clicks)

    @staticmethod
    def shoot(image_path):
        """
        this function takes a screenshoot of the current screen and saves it to the specified path
        Arguments:
            image_path: path to save the screenshot
        """
        pyautogui.screenshot(image_path)
