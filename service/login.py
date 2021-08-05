import constant
from service import Hooker
from service.lifecycle import LifeCycleMixin
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class LoginHooker(Hooker, LifeCycleMixin):

    def __init__(self, browser: str):
        Hooker.__init__(self, browser)
        LifeCycleMixin.__init__(self)
        self.login_info = None

    def _start(self):
        self.open()
        self.get_login_page(self.driver)
        try:
            self.wait_login(self.driver)
            self.login_info = self.current_login_info(self.driver)
        except TimeoutException as e:
            print('장시간 로그인을 하지 않아 브라우저를 닫습니다.')
        finally:
            self.close()

    def get_login_page(self, driver):
        raise NotImplementedError

    def wait_login(self, driver):
        raise NotImplementedError

    def current_login_info(self, driver):
        raise NotImplementedError

class KakaoLoginHooker(LoginHooker):
    
    def __init__(self, browser: str, waits=600):
        super().__init__(browser)
        self.url = constant.url.get('kakao').get('login_page')
        self.waits = waits
        self.wait_condition = lambda driver: driver.current_url == constant.url.get('kakao').get('continue_page')
    
    def get_login_page(self, driver):
        driver.get(self.url)
        self.persist_login(driver)
    
    def persist_login(self, driver):
        check_btn = driver.find_element_by_css_selector('span.ico_check')
        check_btn.click()

    def wait_login(self, driver):
        driver_wait = WebDriverWait(driver, self.waits).until(self.wait_condition)

    def current_login_info(self, driver):
        return list(
            filter(lambda it: it['domain'].startswith('.kakao.com'), self.driver.get_cookies())
        )

def kakaoUserValidity(login_cookie):
    import requests, json
    user_info_api = constant.url.get('kakao').get('user_info_api')
    user_info_response = requests.get(user_info_api, cookies=login_cookie, verify=False)
    user_info_json = json.loads(user_info_response.text)
    if user_info_json.get('error'):
        return 'E_RESPONSE'
    elif user_info_json.get('user'):
        user_info = user_info_json['user']
        user_status = user_info['status']
        if user_status == 'NORMAL':
            return 'OK'
        elif user_status is None:
            return 'E_INVALID_STATUS'
        else:
            return 'E_ARLEADY_RESERVED'
                