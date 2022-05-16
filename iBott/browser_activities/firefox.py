import pickle
import time
import warnings
import os
from telnetlib import EC
from iBott import CustomWebElement
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from iBott.browser_activities.driver_utils import install_firefox, get_firefox_version
from iBott.system_activities.system import System


class FirefoxBrowser(Firefox):
    """

    This class is used to create a browser object.
    It Heritates from the Chrome class.
    Arguments:
        driver_path: path to the driver
        undetectable: if True, to hide bot info in the browser.
    Attributes:
        driver_path: path to the driver<
        undetectable: if True, to hide bot info in the browser.
    Methods:
          open(): This method opens firefox browser to start the navigation. Set Custom options before using this method.
          ignore_images(): This method ignores images in the browser.
          ignore_popups(): This method ignores popups in the browser.
          ignore_notifications(): This method ignores notifications in the browser.
          ignore_errors(): This method ignores errors in the browser.
          headless(): This method ignores
          save_cookies(): This method saves cookies in the browser.
          load_cookies(): This method loads cookies in the browser.
          set_proxy(): This method sets proxy in the browser.
          set_user_agent(): This method sets user agent in the browser.
          set_profile(): This method sets profile in the browser.
          set_download_folder(): This method sets download folder in the browser.
          scrolldown(): This method scrolls down the browser.
          scrollup(): This method scrolls up the browser.
          scroll_to_element(): This method scrolls to the element in the browser.
          element_exists(): This method checks if the element exists in the browser.
          add_tab(): This method adds a new tab in the browser.
          get_tabs(): This method gets all the tabs in the browser.
          switch_tab(): This method switches to the tab in the browser.
          wait_for_element(): This method waits for the element in the browser.
          wait_for_element_to_disappear(): This method waits for the element to disappear in the browser.
          wait_for_element_to_be_clickable(): This method waits for the element to be clickable in the browser.
    """

    _web_element_cls = CustomWebElement

    def __init__(self, driver_path=None, undetectable=False):
        self.default_directory = os.path.dirname(__file__) + '/drivers'
        if not driver_path:

            self.driver = install_firefox(cwd=self.default_directory)
        else:
            self.driver = Service(driver_path)
        self.options = Options()
        self.profile = FirefoxProfile()
        self.undetectable = undetectable
        self.firefox_version = get_firefox_version()
        self.firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX

    def open(self):
        """
        This method opens firefox browser to start the navigation.
        Set Custom options before using this method.
        """
        if self.undetectable:
            PROXY_HOST = "12.12.12.123"
            PROXY_PORT = "1234"
            self.profile.set_preference("network.proxy.type", 1)
            self.profile.set_preference("network.proxy.http", PROXY_HOST)
            self.profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
            self.profile.set_preference("dom.webdriver.enabled", False)
            self.profile.set_preference('useAutomationExtension', False)
            self.profile.update_preferences()
        else:
            warnings.warn("You are using a default configuration of Firefox")
        super().__init__(firefox_profile=self.profile,
                         options=self.options,
                         executable_path=self.driver,
                         desired_capabilities=self.firefox_capabilities,
                         service_log_path=f'{self.default_directory}/firefox_data/firefox.log')

    def ignore_images(self):
        """Disable images in browser for a better performane"""
        self.options.set_preference('permissions.default.image', 2)
        self.options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    def ignore_popups(self):
        """
        Ignore popups in the browser
        *Use this method before opening the browser
        """
        self.options.set_preference('dom.disable_open_during_load', True)
        self.options.set_preference('dom.disable_beforeunload', True)
        self.options.set_preference('dom.disable_window_flip', True)
        self.options.set_preference('dom.disable_window_move_resize', True)
        self.options.set_preference('dom.disable_window_open_feature.close', True)
        self.options.set_preference('dom.disable_window_open_feature.titlebar', True)

    def ignore_notifications(self):
        """
        Ignore notifications in the browser
        *Use this method before opening the browser
        """
        self.options.set_preference('permissions.default.desktop-notification', 2)

    def ignore_errors(self):
        """
        Ignore errors in the browser
        *Use this method before opening the browser
        """
        self.options.set_preference('webdriver_assume_untrusted_issuer', True)
        self.options.set_preference('webdriver_enable_native_events', False)
        self.options.set_preference('webdriver_accept_untrusted_certs', True)
        self.options.set_preference('webdriver_unexpected_alert_behaviour', 'dismiss')

    def headless(self):
        """
        Set browser to headless mode
        *Use this method before opening the browser
        """
        self.options.set_preference('browser.tabs.remote.autostart.2', False)

    def save_cookies(self, file_path=None):
        """
        Save session cookies
        """
        if file_path is None:
            pickle.dump(self.get_cookies(), open(f"{self.default_directory}/firefox_data/cookies.pkl", "wb"))
        else:
            file = os.path.join(file_path, "cookies.pkl")
            pickle.dump(self.get_cookies(), open(file, "wb"))

    def load_cookies(self, path=None):
        """
        Load session cookies
        """
        if path is None:
            cookies = pickle.load(open(f"{self.default_directory}/firefox_data/cookies.pkl", "rb"))
        else:
            file = os.path.join(path, "cookies.pkl")
            cookies = pickle.load(open(file, "rb"))
        for cookie in cookies:
            try:
                self.add_cookie(cookie)
            except Exception as e:
                print(e)

    def set_proxy(self, proxy):
        """
        set proxy to use in browser session
        Arguments:
            proxy: string with the proxy with the format "user:password@host:port"
        """
        # HOST can be IP or name
        self.firefox_capabilities['proxy'] = {
            "httpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }

    def set_user_agent(self, userAgent):
        """
        Change default user agent
        Arguments:
            userAgent: string with the user agent
        """
        self.profile.set_preference("general.useragent.override", userAgent)

    def set_profile(self, path):
        """
        Use firefox profile
        Arguments
            path: path to the profile
        """

        self.profile = FirefoxProfile(path)

    def set_download_folder(self, folder):
        """
        Set download folder
        *Use this method to set the download folder
        Arguments:
            folder: path to the folder
        """
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", folder)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

    def scrolldown(self, h=100):
        """
        Scroll down to % of the current page
        Arguments:
            h: percentage of the page to scroll down
        """
        actual_height = self.execute_script("return document.documentElement.scrollTop")
        to_height = round(round(self.execute_script("return document.body.scrollHeight"))* int(h)/ 100)
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
        to_height = round(round(self.execute_script("return document.body.scrollHeight"))* int(h)/ 100)
        actual_height = self.execute_script("return document.documentElement.scrollTop")

        for i in range(actual_height, to_height, -100):
            self.execute_script(f'window.scrollTo(0,{str(i)})')
            time.sleep(0.1)

    def scroll_to_element(self, method: str, selector: str):
        """
        Scroll to element
        Arguments:
           method: method to use to find the element
           selector: selector to find the element
        Returns
            WebElement if element is found
            False if element is not found
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

    def element_exists(self, method: str, selector: str):
        """Check if element exists
        Arguments:
            method: By.CSS, By.XPATH, By.ID, By.CLASS_NAME
            selector: css selector, xpath, id, class name
        Returns:
            True if element exists, False if not
            """
        searchBy = self.get_method(method)
        if len(self.find_elements(searchBy, selector)) > 0:
            return self.find_element(searchBy, selector)
        else:
            return False

    def add_tab(self):
        """Add a new tab
        Use this method to add a new tab to the browser
        """
        self.execute_script("window.open('');")
        self.switch_to.window(self.window_handles[-1])

    def get_tabs(self):
        """Returns the number of tabs opened"""
        return self.window_handles

    def switch_tab(self, tab_number: int):
        """Switch to tab number
        Arguments:
            tab_number: number of the tab to switch to
        """

        self.switch_to.window(self.window_handles[tab_number])

    def wait_for_element(self, method: str, selector: str, timeout=10):
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
