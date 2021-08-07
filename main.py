from bootstrap import settings
from bootstrap.model import JsonModel
from constant import CONTEXT_PATH, USER_VALIDITY_TEXT
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation

def login(ctx):

    def phase_description(hooker):
        print('='*100)
        print(f"[[1단계]] {hooker.browser} 브라우저에서 카카오 계정에 로그인합니다.")

    def phase_summary(hooker):
        import json
        print("[[1단계]] 로그인 정보를 얻었습니다.")
        print(json.dumps(hooker.login_info))
        print('='*100)

    login_hooker = KakaoLoginHooker(ctx.browser, ctx.login_waits)
    login_hooker.on_start(phase_description)
    login_hooker.on_end(phase_summary)

    login_hooker.start()
    login_cookie_list = login_hooker.login_info
    login_cookie_dict = {item['name']:item['value'] for item in login_cookie_list}
    
    print(USER_VALIDITY_TEXT[kakaoUserValidity(login_cookie_dict)])
    return login_cookie_dict

def region_selection(ctx):

    def phase_description(capture):
        print('='*100)
        print(f"[[2단계]] {capture.browser} 브라우저에서 맵 영역을 지정해 주세요.\n 지정한 영역에서 잔여 백신을 물색할 것입니다.")

    def show_current_region(capture):
        print("현재 보고있는 영역:")
        print('\t', capture.last_capture)
        print('\t', 'CMD 창에서 Ctrl + C하면 이 영역을 백신 검색에 사용합니다.', end='\n\n')

    def phase_summary(capture):
        print('[[2단계]] ', capture.last_capture, '를 좌표 영역으로 사용합니다.')
        print('='*100)

    def error_handler(capture, error):
        try:
            raise error
        except RegionCapture.NullCaptureException:
            print('앱이 지정 영역을 탐지하기 전까지 브라우저를 닫지 마세요.')
            exit()

    region_capture = RegionCapture(ctx.browser)
    region_capture.on_start(phase_description)
    region_capture.on_progress(show_current_region)
    region_capture.on_end(phase_summary)
    region_capture.on_error(error_handler)

    region_capture.start()
    region = region_capture.last_capture
    return region

def reservation(login_cookie, region):

    def phase_description(resv):
        print('='*100)
        print(f"[[3단계]] 설정하신 계정과 장소를 토대로 백신 예약을 시도합니다.")

    def phase_summary(resv):
        print(f"[[3단계]] 어플리케이션을 종료합니다.")
        print('='*100)

    vaccine_reservation = LegacyVaccineReservation()
    vaccine_reservation.on_start(phase_description)
    vaccine_reservation.on_end(phase_summary)

    vaccine_reservation.start(login_cookie=login_cookie, region=region, 
                                run_interval=ctx.run_interval, vaccine_type='ANY')

if __name__ == '__main__':
    ctx = JsonModel(json=settings.initial_context)
    reservation(login(ctx), region_selection(ctx))