import settings # this line runs settings' bootstrap
import os.path
import logging
import json
from threading import Thread

from PyQt5.QtWidgets import QApplication
from view.main import MainView
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture, Region
from service.reservation import LegacyVaccineReservation

login_cookie = region = run_interval = None
reservation = None
running = False

def config_load(path):
    global login_cookie, region, run_interval
    if os.path.isfile(path):
        with open(path, 'r') as file:
            json_data = json.load(file)
        login_cookie = json_data['login_cookie']
        region = Region.from_json(json_data['region'])
        run_interval = json_data['run_interval']

def config_dump(path):
    data = {
        'login_cookie': login_cookie,
        'region': region.__dict__,
        'run_interval': run_interval
    }
    with open('context.json', 'w') as file:
        json.dump(data, file)

def main():
    from constant import CONTEXT_PATH, APP_NAME, QAPP_STYLE
    from constant import BROWSER, LOGIN_WAITS, USER_VALIDITY_TO_VIEW_VALIDITY, USER_VALIDITY_TEXT

    app = view = None
    login_hooker = region_capture = None
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def create_app_and_view():
        app = QApplication([])
        app.setApplicationName(APP_NAME)
        app.setStyle(QAPP_STYLE)
        view = MainView()
        return app, view

    def create_login_hooker():

        def phase_description(hooker):
            logger.info(f'login_hooker> {hooker.browser}에서 카카오 계정에 로그인 합니다.')
        
        def validate_login_info(hooker):
            global login_cookie
            login_cookie_list = hooker.login_info
            login_cookie = {item['name']:item['value'] for item in login_cookie_list}
            user_validity = kakaoUserValidity(login_cookie)
            view.notifyUserValidity(USER_VALIDITY_TO_VIEW_VALIDITY[user_validity])
            view.updateButtons(login_cookie, region, running)
            logger.info(USER_VALIDITY_TEXT[user_validity])

        hooker = KakaoLoginHooker(browser=BROWSER, waits=LOGIN_WAITS)
        hooker.on_start(phase_description)
        hooker.on_end(validate_login_info)
        return hooker

    def create_region_capture():

        def phase_description(capture):
            logger.info(f'region_capture> {capture.browser}에서 맵 영역을 지정하세요.\n지정된 영역에서 백신 여분을 탐색합니다.')

        def show_current_region(capture):
            current_region = capture.last_capture
            print("region_capture> 현재 보고 있는 영역")
            print('\t', current_region)
            print('\t', '브라우저를 닫으면 이 영역을 백신 검색에 사용합니다.', end='\n\n')
            view.notifyRegion(current_region)

        def commit_region(capture):
            global region
            region = capture.last_capture
            view.updateButtons(login_cookie, region, running)

        def error_handler(capture, error):
            try:
                raise error
            except RegionCapture.NullCaptureException:
                logger.warn('지정 영역을 탐지하기 전까지 브라우저를 닫지 마세요.')
                capture.start()
        
        capture = RegionCapture(BROWSER)
        capture.on_start(phase_description)
        capture.on_progress(show_current_region)
        capture.on_end(commit_region)
        capture.on_error(error_handler)
        return capture

    def register_reservation():
        global run_interval, reservation
        def phase_description(resv):
            logger.info('설정하신 계정과 장소를 토대로 백신 예약을 시도합니다.')

        def phase_summary(resv):
            logger.info('매크로 수행이 끝났습니다.')

        run_interval = view.getRunInterval(default=7)
        reservation = LegacyVaccineReservation(login_cookie, region, run_interval)
        reservation.on_start(phase_description)
        reservation.on_end(phase_summary)

    def register_view_handler():

        def run_login_hooker():
            login_hooker.start()

        def run_region_capture():
            capture_start = lambda: region_capture.start()
            capture_thread = Thread(target=capture_start)
            capture_thread.start()

        def run_reservation_macro():
            global running
            register_reservation()
            reservation_start = lambda: reservation.start()
            reservation_thread = Thread(target=reservation_start)
            reservation_thread.start()
            running = True
            view.updateButtons(login_cookie, region, running)
            config_dump(CONTEXT_PATH)

        def stop_reservation_macro():
            global running
            reservation.interrupt()
            running = False
            view.updateButtons(login_cookie, region, running)

        view.onLoginBrowserClicked(run_login_hooker)
        view.onRegionBrowserClicked(run_region_capture)
        view.onStartButtonClicked(run_reservation_macro)
        view.onStopButtonClicked(stop_reservation_macro)

    def try_use_config(path):
        config_load(path)
        if ( login_cookie is not None
                and region is not None):
            user_validity = kakaoUserValidity(login_cookie)
            view.notifyUserValidity(USER_VALIDITY_TO_VIEW_VALIDITY[user_validity])
            view.notifyRegion(region)
            view.updateButtons(login_cookie, region, running)

    app, view = create_app_and_view()
    login_hooker = create_login_hooker()
    region_capture = create_region_capture()
    register_view_handler()

    try_use_config(CONTEXT_PATH)

    app.exec()

if __name__ == '__main__':
    main()
