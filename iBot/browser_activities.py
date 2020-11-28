from .undetected_chromedriver import install
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import os


class ChromeBrowser(Chrome):

    def __init__(self, pathDriver, undetectable=False):
        self.CurrentPath = os.path.dirname(__file__)
        self.driver = pathDriver
        self.options = Options()
        self.undetectable = undetectable

    def open(self):
        if self.undetectable:
            install(self.driver)
            from selenium.webdriver import Chrome
            from selenium.webdriver.chrome.options import Options
        else:
            pass
        super().__init__(self.driver, options=self.options)

    def ignoreImages(self):
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)

    def headless(self):
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--headless")

    def saveCookies(self):
        self.options.add_argument("--user-data-dir=selenium")

    def setProxy(self, proxy):
        self.options.add_argument('--proxy-server=http://%s' % proxy)

    def setUserAgent(self, userAgent):
        self.options.add_argument("user-agent=" + userAgent)

    def setprofile(self, path):
        self.options.add_argument("user-data-dir=" + path)  # Path to your chrome profile

    def scrolldown(self, h=None):
        if h is None:
            h = 100
        else:
            h = int(h)
        to_height = self.execute_script("return document.body.scrollHeight")
        to_height = int((to_height * h) / 100)

        actual_height = self.execute_script("return document.documentElement.scrollTop")

        for i in range(actual_height, to_height, 100):
            self.execute_script("window.scrollTo(0," + str(i) + ")")
            time.sleep(0.1)
