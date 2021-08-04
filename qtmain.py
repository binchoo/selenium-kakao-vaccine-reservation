import settings # this line runs settings' bootstrap

import logging
from threading import Thread

from PyQt5.QtWidgets import QApplication
from view.main import MainView
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation

def main():

    from constant import APP_NAME, QAPP_STYLE
    from constant import BROWSER, LOGIN_WAITS, USER_VALIDITY_TO_VIEW_VALIDITY, USER_VALIDITY_TEXT
    from constant import MACRO_INTERVAL

    app = view = None
    login_hooker = region_capture = reservation = None
    login_cookie = region = run_interval = None
    running = False
    logger = logging.getLogger(__name__)

    def create_app_and_view():
        app = QApplication([])
        app.setApplicationName(APP_NAME)
        app.setStyle(QAPP_STYLE)
        return app, MainView()

    def create_login_hooker():

        def phase_description(hooker):
            logger.info(f'login_hooker> {hooker.browser}에서 카카오 계정에 로그인 합니다.')
        
        def validate_login_info(hooker):
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
            logger.info(f'region_capture> {hooker.browser}에서 맵 영역을 지정하세요.\n지정된 영역에서 백신 여분을 탐색합니다.')

        def show_current_region(capture):
            current_region = capture.last_capture
            print("region_capture> 현재 보고 있는 영역")
            print('\t', current_region)
            print('\t', '브라우저를 닫으면 이 영역을 백신 검색에 사용합니다.', end='\n\n')
            view.notifyRegion(current_region)
            view.updateButtons(login_cookie, region, running)

        def commit_region(capture):
            region = capture.last_capture

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
        return capture

    def register_reservation():

        def phase_description(resv):
            logger.info('설정하신 계정과 장소를 토대로 백신 예약을 시도합니다.')

        def phase_summary(resv):
            logger.info('매크로 수행이 끝났습니다.')

        reservation = LegacyVaccineReservation(login_cookie)
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
            register_reservation()
            run_interval = view.getRunInterval(default=MACRO_INTERVAL)
            reservation_start = lambda: reservation.start(region, run_interval)
            reservation_thread = Thread(target=reservation_start)
            reservation_thread.start()
            running = True
            view.updateButtons(login_cookie, region, running)

        def stop_reservation_macro():
            running = False
            view.updateButtons(login_cookie, region, running)

        view.onLoginBrowserClicked(run_login_hooker)
        view.onRegionBrowserClicked(run_region_capture)
        view.onStartButtonClicked(run_reservation_macro)
        view.onStopButtonClicked(stop_reservation_macro)

    app, view = create_app_and_view()
    login_hooker = create_login_hooker()
    region_capture = create_region_capture()
    register_view_handler()

    app.exec()

if __name__ == '__main__':
    main()