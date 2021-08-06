import logging
import requests

from selenium.webdriver.remote.remote_connection import LOGGER
import selenium.webdriver as webdriver
import seleniumwire.webdriver as webdriver2
from webdriver_manager import chrome, firefox, microsoft, opera

from service import Hooker, Capture
from dto import Region
from bootstrap.model import JsonConfigModel

### Selenium LOGGER settings
LOGGER.setLevel(logging.WARNING)

### requests module's settings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

### Selenium Driver & Driver Manager IoC
Hooker.driver_dependency_map = {
    'chrome': (webdriver.Chrome, chrome.ChromeDriverManager),
    'chromium': (webdriver.Chrome, chrome.ChromeDriverManager),
    'firefox': (webdriver.Firefox, firefox.GeckoDriverManager),
    'ie': (webdriver.Ie, microsoft.IEDriverManager),
    'edge': (webdriver.Edge, microsoft.EdgeChromiumDriverManager),
    'opera': (webdriver.Opera, opera.OperaDriverManager)
}

Capture.driver_dependency_map = {
    'chrome': (webdriver2.Chrome, chrome.ChromeDriverManager),
    'chromium': (webdriver2.Chrome, chrome.ChromeDriverManager),
    'firefox': (webdriver2.Firefox, firefox.GeckoDriverManager),
}

initial_context = {
    'platforms': ['kakao'],
    'user_validity': 'expired',
    'status_display': {
        'none': {
            'text': '정보 없음',
            'color': 'orange'
        },
        'expired': {
            'text': '만료됨',
            'color': 'red'
        },
        'ok': {
            'text': '유효함',
            'color': 'green'
        }
    },
    'region': Region((0, 0), (0, 0)),
    'default_vaccines': ['ANY'],
    'run_interval': 7,
    'running': False,
}