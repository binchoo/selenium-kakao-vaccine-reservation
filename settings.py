import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

import selenium.webdriver as webdriver
import seleniumwire.webdriver as webdriver2
from webdriver_manager import (chrome, firefox, microsoft, opera)
from service import (Hooker, Capture) # Apply IoC
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

# Constants
url = {
    'kakao': {
        'login_page': "https://accounts.kakao.com/login?continue=https%3A%2F%2Fcs.kakao.com%2F",
        'continue_page': "https://cs.kakao.com/",
        'map_page': "https://vaccine-map.kakao.com/map2?v=1",
        'user_info_api': "https://vaccine.kakao.com/api/v1/user",
        'left_by_coords': "https://vaccine-map.kakao.com/api/v2/vaccine/left_count_by_coords",
        'check_organization_format': 'https://vaccine.kakao.com/api/v2/org/org_code/{}',
        'reservation': 'https://vaccine.kakao.com/api/v1/reservation'
    }
}
header = {
    'kakao': {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; SM-G977N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.164 Mobile Safari/537.36;KAKAOTALK 2309420",
        'Origin': 'https://vaccine.kakao.com',
        'Connection': 'Keep-Alive',
        'Keep-Alive': 'timeout=5, max=1000'
    }
}
login_sleep = 600   # 10 minutes until login done.
vaccine_search_time = 7


