from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class CustomWebElement(WebElement):
    """
    Custom WebElement class to add custom methods to WebElement class.
    Methods:
        double_click() : Double click on the element.
        enter(): Enter text in the element.
        tab(): Tab on the element.
        escape(): Escape on the element.
        backspace(): Backspace on the element.
        write(text): Write text in the element.
        clear(): Clear the element.
        get_text(): Get text from the element.
        get_link(): Get link from the element.
        get_attribute(attribute): Get attribute from the element.
    """
    def double_click(self, driver):
        """
        Double click on the element.
        Arguments:
            driver: WebDriver object.
        """
        actionChains = ActionChains(driver)
        actionChains.double_click(self).perform()
        return self

    def enter(self):
        """
        Send enter key to the element.
        """
        self.send_keys(Keys.ENTER)
        return self

    def tab(self):
        """
        Send tab key to the element.
        """
        self.send_keys(Keys.TAB)
        return self

    def escape(self):
        """
        Send escape key to the element.
        """
        self.send_keys(Keys.ESCAPE)

    def backspace(self):
        """
        Send backspace key to the element.
        """
        self.send_keys(Keys.BACKSPACE)
        return self

    def write(self, text):
        """
        Write text in the element.
        """
        self.send_keys(text)
        return self

    def clear(self):
        """
        Clear the text in the element.
        """
        self.send_keys(Keys.CONTROL + "a")
        self.send_keys(Keys.DELETE)
        return self

    def get_text(self):
        """
        Get the text of the element.
        """
        return self.text

    def get_link(self):
        """
        Get the link of the element.
        """
        return self.get_attribute("href")

    def get_attribute(self, attribute):
        """
        Get the attribute of the element.
        """
        return self.get_attribute(attribute)

