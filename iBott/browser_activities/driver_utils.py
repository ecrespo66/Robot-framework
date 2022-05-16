import io
import logging
import os
import subprocess
import urllib.request
import urllib.error
import zipfile
import xml.etree.ElementTree as elemTree
import tarfile
import sys
import re
from io import BytesIO
logger = logging.getLogger(__name__)


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith('win'):
        return 'chromedriver.exe'
    return 'chromedriver'


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith('win'):
        return ';'
    return ':'


def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform, architecture


def get_chromedriver_url(version):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: chromedriver version string
    :return: Download URL for chromedriver
    """
    base_url = 'https://chromedriver.storage.googleapis.com/'
    platform, architecture = get_platform_architecture()
    return base_url + version + '/chromedriver_' + platform + architecture + '.zip'


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if 'PATH' not in os.environ:
        return None
    for directory in os.environ['PATH'].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, '-v'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == 'linux':
        executable_name = 'google-chrome'
        if os.path.isfile('/usr/bin/chromium-browser'):
            executable_name = 'chromium-browser'
        if os.path.isfile('/usr/bin/chromium'):
            executable_name = 'chromium'
        with subprocess.Popen([executable_name, '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Chromium', '').replace('Google Chrome', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                                   stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
    elif platform == 'win':
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    else:
        return
    return version


def get_major_version(version):
    """
    :param version: the version of chrome
    :return: the major version of chrome
    """
    return version.split('.')[0]


def get_matched_chromedriver_version(version):
    """
    :param version: the version of chrome
    :return: the version of chromedriver
    """
    doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
    root = elemTree.fromstring(doc)
    for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
        if k.text.find(get_major_version(version) + '.') == 0:
            return k.text.split('/')[0]
    return


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print(get_chromedriver_path())


def download_chromedriver(cwd=None):
    """
    Downloads, unzips and installs chromedriver.
    If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.

    :param cwd: Flag indicating whether to download to current working directory
    :return: The file path of chromedriver
    """
    chrome_version = get_chrome_version()
    if not chrome_version:
        logging.debug('Chrome is not installed.')
        return
    chromedriver_version = get_matched_chromedriver_version(chrome_version)
    if not chromedriver_version:
        logging.debug('Can not find chromedriver for currently installed chrome version.')
        return
    major_version = get_major_version(chromedriver_version)

    if cwd:
        chromedriver_dir = cwd
    else:
        chromedriver_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            major_version
        )
    chromedriver_filename = get_chromedriver_filename()
    chromedriver_filepath = os.path.join(chromedriver_dir, chromedriver_filename)
    if not os.path.isfile(chromedriver_filepath) or \
            not check_version(chromedriver_filepath, chromedriver_version):
        logging.debug(f'Downloading chromedriver ({chromedriver_version})...')
        if not os.path.isdir(chromedriver_dir):
            os.mkdir(chromedriver_dir)
        url = get_chromedriver_url(version=chromedriver_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError('Not Found')
        except urllib.error.URLError:
            raise RuntimeError(f'Failed to download chromedriver archive: {url}')
        archive = BytesIO(response.read())
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extract(chromedriver_filename, chromedriver_dir)
    else:
        logging.debug('Chromedriver is already installed.')
    if not os.access(chromedriver_filepath, os.X_OK):
        os.chmod(chromedriver_filepath, 0o744)
    return chromedriver_filepath


def install_chrome(cwd=None):
    """
    Appends the directory of the chromedriver binary file to PATH.

    :param cwd: Flag indicating whether to download to current working directory
    :return: The file path of chromedriver
    """
    directory = cwd
    chromedriver_filepath = download_chromedriver(directory)
    if not chromedriver_filepath:
        logging.debug('Can not download chromedriver.')
        return
    chromedriver_dir = os.path.dirname(chromedriver_filepath)
    if 'PATH' not in os.environ:
        os.environ['PATH'] = chromedriver_dir
    elif chromedriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = chromedriver_dir + get_variable_separator() + os.environ['PATH']
    return chromedriver_filepath


class Chrome:

    def __new__(cls, *args, **kwargs):

        if not ChromeDriverManager.installed:
            ChromeDriverManager(*args, **kwargs).install()
        if not ChromeDriverManager.selenium_patched:
            ChromeDriverManager(*args, **kwargs).patch_selenium_webdriver()
        if not kwargs.get('executable_path'):
            kwargs['executable_path'] = './{}'.format(ChromeDriverManager(*args, **kwargs).executable_path)
        if not kwargs.get('options'):
            kwargs['options'] = ChromeOptions()
        instance = object.__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
        Object.defineProperty(window, 'navigator', {
            value: new Proxy(navigator, {
              has: (target, key) => (key === 'webdriver' ? false : key in target),
              get: (target, key) =>
                key === 'webdriver'
                  ? undefined
                  : typeof target[key] === 'function'
                  ? target[key].bind(target)
                  : target[key]
            })
        })
                  """
            },
        )
        original_user_agent_string = instance.execute_script(
            "return navigator.userAgent"
        )
        instance.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": original_user_agent_string.replace("Headless", ""),
            },
        )
        logger.info(f"starting undetected_chromedriver.Chrome({args}, {kwargs})")
        return instance


class ChromeOptions:
    def __new__(cls, *args, **kwargs):
        if not ChromeDriverManager.installed:
            ChromeDriverManager(*args, **kwargs).install()
        if not ChromeDriverManager.selenium_patched:
            ChromeDriverManager(*args, **kwargs).patch_selenium_webdriver()

        instance = object.__new__(cls)
        instance.__init__()
        instance.add_argument("start-maximized")
        instance.add_experimental_option("excludeSwitches", ["enable-automation"])
        instance.add_experimental_option("useAutomationExtension", False)
        logger.info(f"starting undetected_chromedriver.ChromeOptions({args}, {kwargs})")
        return instance


class ChromeDriverManager(object):
    installed = False
    selenium_patched = False
    target_version = None

    DL_BASE = "https://chromedriver.storage.googleapis.com/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):

        _platform = sys.platform
        self.target_version = target_version
        if target_version:
            self.target_version = target_version
        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if _platform in ('win32',):
            exe_name = base_.format(".exe")
        if _platform in ('linux',):
            _platform += '64'
            exe_name = exe_name.format('')
        if _platform in ('darwin',):
            _platform = 'mac64'
            exe_name = exe_name.format('')
        self.platform = _platform
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

    def patch_selenium_webdriver(self_):
        """
        Patches selenium package Chrome, ChromeOptions classes for current session

        :return:
        """
        import selenium.webdriver.chrome.service
        import selenium.webdriver
        selenium.webdriver.Chrome = Chrome
        selenium.webdriver.ChromeOptions = ChromeOptions
        logger.warning(
            "Selenium patched. Safe to import Chrome / ChromeOptions"
        )
        self_.__class__.selenium_patched = True

    def install(self, patch_selenium=True):
        """
        Initialize the patch

        This will:
         download chromedriver if not present
         patch the downloaded chromedriver
         patch selenium package if <patch_selenium> is True (default)

        :param patch_selenium: patch selenium webdriver classes for Chrome and ChromeDriver (for current python session)
        :return:
        """
        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()
            self.patch_binary()
            self.__class__.installed = True

        if patch_selenium:
            self.patch_selenium_webdriver()

    def get_release_version_number(self):
        """
        Gets the latest major version available, or the latest major version of self.target_version if set explicitly.

        :return: version string
        """
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return urllib.urlopen(self.__class__.DL_BASE + path).read().decode()

    def fetch_chromedriver(self):
        """
        Downloads ChromeDriver from source and unpacks the executable

        :return: on success, name of the unpacked executable
        """
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number()
        if os.path.exists(self.executable_path):
            return self.executable_path
        urllib.urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != 'win32':
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

    def patch_binary(self):
        """
        Patches the ChromeDriver binary

        :return: False on failure, binary name on success
        """
        if self.__class__.installed:
            return

        with io.__open(self.executable_path, "r+b") as binary:
            for line in iter(lambda: binary.readline(), b""):
                if b"cdc_" in line:
                    binary.seek(-len(line), 1)
                    line = b"  var key = '$azc_abcdefghijklmnopQRstuv_';\n"
                    binary.write(line)
                    __IS_PATCHED__ = 1
                    break
            else:
                return False
            return True





def get_platform_architecture_firefox():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = 'os'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine geckodriver download URL for this platform.')
    return platform, architecture

def get_latest_geckodriver_version():
    """
    :return: the latest version of geckodriver
    """
    url = urllib.request.urlopen('https://github.com/mozilla/geckodriver/releases/latest').geturl()
    if '/tag/' not in url:
        return
    return url.split('/')[-1]


def get_geckodriver_path():
    """
    :return: path of the geckodriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_geckodriver_path():
    """
    Print the path of the geckodriver binary.
    """
    print(get_geckodriver_path())


def get_geckodriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith('win'):
        return 'geckodriver.exe'
    return 'geckodriver'


def get_geckodriver_url(version):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: the version of geckodriver
    :return: Download URL for geckodriver
    """
    platform, architecture = get_platform_architecture_firefox()
    return f'https://github.com/mozilla/geckodriver/releases/download/{version}' \
           f'/geckodriver-{version}-{platform}{architecture}.tar.gz'


def download_geckodriver(cwd=False):
    """
    Downloads, unzips and installs geckodriver.
    If a geckodriver binary is found in PATH it will be copied, otherwise downloaded.

    :param cwd: Flag indicating whether to download to current working directory
    :return: The file path of geckodriver
    """
    firefox_version = get_firefox_version()
    if not firefox_version:
        logging.debug('Firefox is not installed.')
        return
    geckodriver_version = get_latest_geckodriver_version()
    if not geckodriver_version:
        logging.debug('Can not find latest version of geckodriver.')
        return

    if cwd:
        geckodriver_dir = cwd
    else:
        geckodriver_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            geckodriver_version
        )
    geckodriver_filename = get_geckodriver_filename()
    geckodriver_filepath = os.path.join(geckodriver_dir, geckodriver_filename)
    if not os.path.isfile(geckodriver_filepath):
        logging.debug(f'Downloading geckodriver ({geckodriver_version})...')
        if not os.path.isdir(geckodriver_dir):
            os.mkdir(geckodriver_dir)
        url = get_geckodriver_url(geckodriver_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError('Not Found')
        except urllib.error.URLError:
            raise RuntimeError(f'Failed to download geckodriver archive: {url}')
        archive = BytesIO(response.read())

        tar = tarfile.open(fileobj=archive, mode='r:gz')
        tar.extractall(geckodriver_dir)
        tar.close()
    else:
        logging.debug('geckodriver is already installed.')
    if not os.access(geckodriver_filepath, os.X_OK):
        os.chmod(geckodriver_filepath, 0o744)
    return geckodriver_filepath


def install_firefox(cwd=False):
    """
    Appends the directory of the geckodriver binary file to PATH.

    :param cwd: Flag indicating whether to download to current working directory
    :return: The file path of geckodriver
    """
    geckodriver_filepath = download_geckodriver(cwd)
    if not geckodriver_filepath:
        logging.debug('Can not download geckodriver.')
        return
    geckodriver_dir = os.path.dirname(geckodriver_filepath)
    if 'PATH' not in os.environ:
        os.environ['PATH'] = geckodriver_dir
    elif geckodriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = geckodriver_dir + get_variable_separator() + os.environ['PATH']
    return geckodriver_filepath


def get_firefox_version():
    """
    :return: the version of firefox installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == 'linux':
        with subprocess.Popen(['firefox', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'win':
        path1 = 'C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe'
        path2 = 'C:\\PROGRA~2\\Mozilla Firefox\\firefox.exe'
        if os.path.exists(path1):
            process = subprocess.Popen([path1, '-v', '|', 'more'], stdout=subprocess.PIPE)
        elif os.path.exists(path2):
            process = subprocess.Popen([path2, '-v', '|', 'more'], stdout=subprocess.PIPE)
        else:
            return
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    else:
        return
    return version

