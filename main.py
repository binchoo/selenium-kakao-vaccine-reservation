import settings
import pprint
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation

def login():

    def phase_description(hooker):
        print('='*100)
        print(f"[[1단계]] {hooker.browser} 브라우저에서 카카오 계정에 로그인합니다.")

    def phase_summary(hooker):
        print("[[1단계]] 로그인 정보를 얻었습니다.")
        pprint.pprint(hooker.login_info)
        print('='*100)

    user_validation_text = {
        "E_RESPONSE": """
            사용자 정보를 불러오는데 실패하였습니다. 
            Chrome 브라우저에서 카카오에 제대로 로그인되어있는지 확인해주세요.
            로그인이 되어 있는데도 안된다면, 카카오톡에 들어가서 잔여백신 알림 신청을 한번 해보세요. 정보제공 동의가 나온다면 동의 후 다시 시도해주세요.""",
        "E_INVALID_STATUS": "사용자의 상태를 조회할 수 없었습니다.",
        "E_ALREDY_RESERVED": "이미 접종이 완료되었거나 예약이 완료된 사용자입니다.",
        "OK": "사용자 정보를 불러오는데 성공했습니다."
    }

    login_hooker = KakaoLoginHooker('chrome')
    login_hooker.on_start(phase_description)
    login_hooker.on_end(phase_summary)

    login_hooker.start()
    login_cookie_list = login_hooker.login_info
    login_cookie_dict = {item['name']:item['value'] for item in login_cookie_list}
    
    print(user_validation_text[kakaoUserValidity(login_cookie_dict)])
    return login_cookie_dict

def region_selection():

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
        print(error)
        print('앱이 지정 영역을 탐지하기 전까지 브라우저를 닫지 마세요.')
        exit()

    region_capture = RegionCapture('chrome')
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

    vaccine_reservation = LegacyVaccineReservation(login_cookie)
    vaccine_reservation.on_start(phase_description)
    vaccine_reservation.on_end(phase_summary)

    vaccine_reservation.start(region)

if __name__ == '__main__':
    reservation(login(), region_selection())