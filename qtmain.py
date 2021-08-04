import settings # this line runs settings' bootstrap
import pprint
import time
from threading import Thread

from PyQt5.QtWidgets import QApplication
from view.main import MainView
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation

login_cookie = None

def load_config():
    return None

def init_q_app(config):
    app = QApplication([])
    app.setStyle('Fusion')
    app.setApplicationName('COVID-19 Vaccine Auto Reservation')
    view = MainView(config=config)
    return app, view

def init_login_hooker(app, view):

    user_validation_text = {
        "E_RESPONSE": """
            사용자 정보를 불러오는데 실패하였습니다. 
            Chrome 브라우저에서 카카오에 제대로 로그인되어있는지 확인해주세요.
            로그인이 되어 있는데도 안된다면, 카카오톡에 들어가서 잔여백신 알림 신청을 한번 해보세요. 정보제공 동의가 나온다면 동의 후 다시 시도해주세요.""",
        "E_INVALID_STATUS": "사용자의 상태를 조회할 수 없었습니다.",
        "E_ALREDY_RESERVED": "이미 접종이 완료되었거나 예약이 완료된 사용자입니다.",
        "OK": "사용자 정보를 불러오는데 성공했습니다."
    }

    def phase_description(hooker):
        print('='*100)
        print(f"[[1단계]] {hooker.browser} 브라우저에서 카카오 계정에 로그인합니다.")

    def phase_summary(hooker):
        login_cookie_list = login_hooker.login_info
        login_cookie_dict = {item['name']:item['value'] for item in login_cookie_list}
        login_cookie = login_cookie_dict

        import json
        print("[[1단계]] 로그인 정보를 얻었습니다.")
        print(json.dumps(login_cookie_list))
        print('='*100)

        validity = kakaoUserValidity(login_cookie_dict)
        print(user_validation_text[validity])
        
        if validity == 'OK':
            view_vailidity = 'ok'
        else:
            view_vailidity = 'expired'
        view.userConfig.loginConfig.loginStatus.notifyStatusChanged(view_vailidity)

    login_hooker = KakaoLoginHooker('chrome')
    login_hooker.on_start(phase_description)
    login_hooker.on_end(phase_summary)

    return login_hooker

def init_region_capture(app, view):

    def phase_description(capture):
        print('='*100)
        print(f"[[2단계]] {capture.browser} 브라우저에서 맵 영역을 지정해 주세요.\n 지정한 영역에서 잔여 백신을 물색할 것입니다.")

    def set_current_region(capture):
        region = capture.last_capture
        print("현재 보고있는 영역:")
        print('\t', region)
        print('\t', 'CMD 창에서 Ctrl + C하면 이 영역을 백신 검색에 사용합니다.', end='\n\n')

        view.userConfig.regionConfig.topLeftVariable.setText(str(region.top_left))
        view.userConfig.regionConfig.bottomRightVariable.setText(str(region.bottom_right))

    def phase_summary(capture):
        print('[[2단계]] ', capture.last_capture, '를 좌표 영역으로 사용합니다.')
        print('='*100)

    def error_handler(capture, error):
        try:
            raise error
        except RegionCapture.NullCaptureException:
            print('앱이 지정 영역을 탐지하기 전까지 브라우저를 닫지 마세요.')
            exit()

    region_capture = RegionCapture('chrome')
    region_capture.on_start(phase_description)
    region_capture.on_progress(set_current_region)
    region_capture.on_end(phase_summary)
    region_capture.on_error(error_handler)

    return region_capture

def init_view(view, login_hooker, region_capture):
    view.userConfig.loginConfig.browserButton.clicked.connect(login_hooker.start)

    def region_capture_th_work():
        region_capture.start()
    
    def region_capture_th_start():
        th = Thread(target=region_capture_th_work)
        th.start()
        
    view.userConfig.regionConfig.browserButton.clicked.connect(region_capture_th_start)

def main():
    config = load_config()
    application, view = init_q_app(config)
    login_hooker = init_login_hooker(application, view)
    region_capture = init_region_capture(application, view)

    init_view(view, login_hooker, region_capture)
    application.exec()

if __name__ == '__main__':
    main()