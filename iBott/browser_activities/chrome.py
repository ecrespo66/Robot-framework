from iBott.browser_activities.driver_utils import install_chrome, ChromeDriverManager, get_chrome_version
from selenium.webdriver.support.wait import WebDriverWait
from telnetlib import EC
from iBott.browser_activities.web_elements import CustomWebElement
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings

import time
import os


class ChromeBrowser(Chrome):
    """
    This class is used to create a browser object.
    It Heritages from the Chrome class.
    Arguments:
        driver_path: path to the driver
        undetectable: if True, the browser will not be detected by antispam systems.
    Attributes:
        driver_path: path to the driver
        undetectable: if True, the browser will not be detected by antispam systems.
        chrome_version: version of chrome
        options: options for the browser
    Methods:
       open(): open the browser and load defined options.
       ignore_images(): ignore images in the browser.
       ignore_popups(): ignore popups in the browser.
       ignore_notifications(): ignore notifications in the browser.
       ignore_errors(): ignore errors in the browser.
       headless(): open the browser in headless mode.
       save_cookies(): save the cookies of the browser.
       load_cookies(): load the cookies of the browser.
       set_proxy(): set a proxy for the browser.
       set_user_agent(): set a user agent for the browser.
       set_profile(): set a profile for the browser.
       scrolldown(h): scroll down to % height of the page .
       scrollup(h): scroll up to % height of the page .
       scroll_to_element(element): scroll to the element.
       set_download_folder(folder): set the download folder.
       element_exists(element): check if the element exists.
       add_tab(): add a new tab.
       get_tabs(): get the tabs of the browser.
       close_tab(tab): close the current tab.
       switch_to_tab(tab): switch to the tab.
       wait_for_element(element, timeout): wait for the element to appear.
       wait_for_element_to_disappear(element, timeout): wait for the element to disappear.
       wait_for_element_to_be_clickable(element, timeout): wait for the element to be clickable.
    """

    _web_element_cls = CustomWebElement

    def __init__(self, driver_path=None, undetectable=False):
        if not driver_path:
            self.driver = install_chrome(os.path.dirname(__file__) + '/drivers')
        else:
            self.driver = driver_path
        self.options = Options()
        self.undetectable = undetectable
        self.chrome_version = get_chrome_version()

    def open(self):
        """
        This method opens Chrome browser to start the navigation.
        Set Custom options before using this method.
        """
        if self.undetectable:
            ChromeDriverManager(self.driver, self.chrome_version).install()
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option('useAutomationExtension', False)
        else:
            warnings.warn("You are using a browser that is  detectable by antispam systems.")
        super().__init__(self.driver, options=self.options)

    def ignore_images(self):
        """
        Disable images in browser for a better performane
        *Use this method before opening the browser
        """

        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)

    def ignore_popups(self):
        """
        Ignore popups in the browser
        *Use this method before opening the browser
        """
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-infobars")

    def ignore_notifications(self):
        """
        Ignore notifications in the browser
        *Use this method before opening the browser
        """
        self.options.add_argument("--disable-notifications")

    def ignore_errors(self):
        """
        Ignore errors in the browser
        *Use this method before opening the browser
        """
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-insecure-localhost")

    def headless(self):
        """
        Set browser to headless mode
        *Use this method before opening the browser
        """
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--headless")

    def save_cookies(self):
        """Save session cookies"""
        self.options.add_argument("--user-data-dir=selenium")

    def load_cookies(self, path=None):
        """Load session cookies"""
        self.options.add_argument("--user-data-dir=selenium")

    def set_proxy(self, proxy):
        """
        set proxy to use in browser session
        Arguments:
            proxy: string with the proxy
        """
        self.options.add_argument('--proxy-server=http://%s' % proxy)

    def set_user_agent(self, userAgent):
        """
        Change default user agent
        Arguments:
            userAgent: string with the user agent
        """
        self.options.add_argument("user-agent=" + userAgent)

    def set_profile(self, path):
        """
        Use system chrome profile
        Arguments
            path: path to the profile
        """
        self.options.add_argument("user-data-dir=" + path)  # Path to your chrome profile

    def scrolldown(self, h=100):
        """
        Scroll down to % of the current page
        Arguments:
            h: percentage of the page to scroll down
        """

        h = int(h)
        to_height = round(self.execute_script("return document.body.scrollHeight"))
        to_height = round((to_height * h) / 100)
        actual_height = self.execute_script("return document.documentElement.scrollTop")
        for i in range(actual_height, to_height, 100):
            self.execute_script(f'window.scrollTo(0,{str(i)})')
            time.sleep(0.1)

    def scrollup(self, h=100):
        """
        Scroll up to % of the current page
        Arguments:
            h: percentage of the page to scroll up
        """
        h = int(h)
        to_height = round(round(self.execute_script("return document.body.scrollHeight")) * int(h) / 100)
        actual_height = self.execute_script("return document.documentElement.scrollTop")

        for i in range(actual_height, to_height, -100):
            self.execute_script(f'window.scrollTo(0,{str(i)})')
            time.sleep(0.1)

    def scrolldown_to_element(self, method: str, selector: str):
        """
        Scroll to element
        Arguments:
           method: method to use to find the element
           selector: selector to find the element
        Returns
            WebElement if element is found
        """

        searchBy = self.get_method(method)
        actual_height = self.execute_script("return document.documentElement.scrollTop")
        scroll_height = self.execute_script("return document.body.scrollHeight")
        i = 100

        while True:
            self.execute_script(f'window.scrollTo(0,{str(actual_height + i)})')
            i += 100
            time.sleep(0.1)
            actual_height = self.execute_script("return document.documentElement.scrollTop")
            if WebDriverWait(self, 1).until(EC.visibility_of_element_located((searchBy, selector))):
                return self.find_element(searchBy, selector)
            if scroll_height == actual_height:
                raise Exception("Element not found")

    def set_download_folder(self, folder):
        """
        Set download folder
        *Use this method to set the download folder
        Arguments:
            folder: path to the folder
        """
        self.options.add_experimental_option("prefs", {
            "download.default_directory": f"{folder}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })

    def element_exists(self, method, selector):
        """
        Check if element exists
        Arguments:
            method: By.CSS, By.XPATH, By.ID, By.CLASS_NAME
            selector: css selector, xpath, id, class name
        Returns:
            True if element exists, False if not
            """
        searchBy = self.get_method(method)
        if len(self.find_elements(searchBy, selector)) > 0:
            return True
        else:
            return False

    def add_tab(self):
        """Add a new tab to the browser"""
        self.execute_script("window.open();")
        self.switch_to.window(self.window_handles[-1])

    def close_tab(self):
        """Close the current tab"""
        self.close()
        self.switch_to.window(self.window_handles[-1])

    def get_tabs(self):
        """Returns the number of tabs opened"""
        return self.window_handles

    def switch_tab(self, tab_number):
        """
        Switch to tab number
        Arguments:
            tab_number: number of the tab to switch to
        """

        self.switch_to.window(self.window_handles[tab_number])

    def wait_for_element(self, method, selector, timeout=10):
        """
        Wait for element to appear in the DOM
        Arguments:
            method: xpath, id, link_text, name, tag_name, class_name, css_selector
            selector: xpath, id, link_text, name, tag_name, class_name, css_selector
            timeout: time to wait for element to appear in seconds
        """
        searchBy = self.get_method(method)
        WebDriverWait(self, timeout).until(EC.visibility_of_element_located((searchBy, selector)))

    def wait_for_element_to_disappear(self, method: str, selector: str, timeout=10):
        """
        Wait for element to disappear from the DOM
        Arguments:
            method: xpath, id, link_text, name, tag_name, class_name, css_selector
            selector: xpath, id, link_text, name, tag_name, class_name, css_selector
            timeout: time to wait for element to disappear in seconds
        """
        searchBy = self.get_method(method)
        WebDriverWait(self, timeout).until(EC.invisibility_of_element_located((searchBy, selector)))

    def wait_for_element_to_be_clickable(self, method, selector, timeout=10):
        """
        Wait for element to be clickable
        Arguments:
            method: xpath, id, link_text, name, tag_name, class_name, css_selector
            selector: xpath, id, link_text, name, tag_name, class_name, css_selector
            timeout: time to wait for element to be clickable in seconds
        """
        searchBy = self.get_method(method)
        WebDriverWait(self, timeout).until(EC.element_to_be_clickable((searchBy, selector)))

    @staticmethod
    def get_method(method):
        if method.lower() == "xpath":
            return By.XPATH
        elif method.lower() == "id":
            return By.ID
        elif method.lower() == "link_text":
            return By.LINK_TEXT
        elif method.lower() == "name":
            return By.NAME
        elif method.lower() == "tag_name":
            return By.TAG_NAME
        elif method.lower() == "class_name":
            return By.CLASS_NAME
        elif method.lower() == "css_selector":
            return By.CSS_SELECTOR
        else:
            raise Exception("Method not found")
