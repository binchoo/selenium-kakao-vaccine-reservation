import selenium.webdriver as webdriver
import seleniumwire.webdriver as webdriver2
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import webdriver_manager.chrome
import webdriver_manager.firefox
import webdriver_manager.microsoft
import webdriver_manager.opera

DriverDependencyMap = {
    'chrome': (webdriver.Chrome, webdriver_manager.chrome.ChromeDriverManager),
    'chromium': (webdriver.Chrome, webdriver_manager.chrome.ChromeDriverManager),
    'firefox': (webdriver.Firefox, webdriver_manager.firefox.GeckoDriverManager),
    'ie': (webdriver.Ie, webdriver_manager.microsoft.IEDriverManager),
    'edge': (webdriver.Edge, webdriver_manager.microsoft.EdgeChromiumDriverManager),
    'opera': (webdriver.Opera, webdriver_manager.opera.OperaDriverManager)
}

RequestCaptureDependencyMap = {
    'chrome': (webdriver2.Chrome, webdriver_manager.chrome.ChromeDriverManager),
    'chromium': (webdriver2.Chrome, webdriver_manager.chrome.ChromeDriverManager),
    'firefox': (webdriver2.Firefox, webdriver_manager.firefox.GeckoDriverManager),
}

LOGGER.setLevel(logging.WARNING)

url = {
    'kakao': {
        'login_page': "https://accounts.kakao.com/login?continue=https%3A%2F%2Fvaccine-map.kakao.com%2Fmap2%3Fv%3D1",
        'continue_page': "https://vaccine-map.kakao.com/map2?v=1",
        'map_page': "https://vaccine-map.kakao.com/map2?v=1",
        'user_info_api': "https://vaccine.kakao.com/api/v1/user",
        'left_by_coords': "https://vaccine-map.kakao.com/api/v2/vaccine/left_count_by_coords",
        'check_organization_format': 'https://vaccine.kakao.com/api/v2/org/org_code/{}',
        'reservation': 'https://vaccine.kakao.com/api/v1/reservation'
    }
}

login_sleep = 600   # 10 minutes until login done.

vaccin_search_time = 21