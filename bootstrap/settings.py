import logging
import requests

from selenium.webdriver.remote.remote_connection import LOGGER
import selenium.webdriver as webdriver
import seleniumwire.webdriver as webdriver2
from webdriver_manager import chrome, firefox, microsoft, opera

from service import Hooker, Capture
from dto import Region, VaccineVendor

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
    'user_validity': 'none',
    'user_validity_display': {
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
    'region': None,
    'login_waits': 600,
    'browser': 'chrome',
    'run_interval': 1,
    'running': False,
    'vaccine_types': (VaccineVendor.PFIZER, VaccineVendor.MODERNA),
    'vaccine_type_opts': [
        {
            'default': True,
            'text': '화이자/모더나',
            'ref': (VaccineVendor.PFIZER, VaccineVendor.MODERNA),
        }, {
            'default': False,
            'text': '화이자',
            'ref': (VaccineVendor.PFIZER),
        }, {
            'default': False,
            'text': '모더나',
            'ref': (VaccineVendor.MODERNA),
        }, {
            'default': False,
            'text': '아스트라제네카',
            'ref': (VaccineVendor.ASTRAZENECA),
        }, {
            'default': False,
            'text': '아무거나',
            'ref': (VaccineVendor.ANY),
        }
    ]
}

serialize_converter = {
    'region': lambda it: it.__dict__
}

deserialize_converter = {
    'region': lambda it: Region(it['top_left'], it['bottom_right'])
}