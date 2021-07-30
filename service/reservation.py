import settings
import requests, json
from datetime import datetime
import time
from service.lifecycle import LifeCycleMixin

class LegacyVaccineReservation(LifeCycleMixin):

    def __init__(self, login_cookie):
        self.search_time = settings.vaccine_search_time
        self.login_cookie = login_cookie
        self.header = settings.header.get('kakao')
        self.reservation_url = settings.url.get('kakao').get('reservation')

    def start(self, region):
        self.on_start_listener(self)
        self.find_vaccine(self.vaccine_type_input(), region)
        self.on_end_listener(self)

    def vaccine_type_input(self):
        vaccine_type = None
        while vaccine_type is None:
            print("""
                <백신 코드 일람>
                화이자         : VEN00013
                모더나         : VEN00014
                아스크라제네카   : VEN00015
                얀센          : VEN00016
                아무거나       : ANY
            """)
            vaccine_type = str.upper(input("예약시도할 백신 코드를 알려주세요."))
        return vaccine_type

    def find_vaccine(self, vaccine_type, region):
        left_by_coords_url = settings.url.get('kakao').get('left_by_coords')
        data = {
            "bottomRight": {
                "x": region.bottom_right[0], 
                "y": region.bottom_right[1]
            }, 
            "onlyLeft": False, 
            "order": "latitude",
            "topLeft": {
                "x": region.top_left[0], 
                "y": region.top_left[1]
            }
        }

        done = False
        found = None
        while not done:
            try:
                response = requests.post(left_by_coords_url, headers=self.header, json=data, verify=False)
                response_json = json.loads(response.text)
                print(response_json)
                self.pretty_print(response_json)
                for x in response_json.get("organizations"):
                    if x.get("status") == "AVAILABLE" or x.get("leftCounts") != 0:
                        found = x
                        done = True
                        break
            except requests.exceptions.Timeout as timeouterror:
                print("Timeout Error : ", timeouterror)
                close()
            except requests.exceptions.ConnectionError as connectionerror:
                print("Connecting Error : ", connectionerror)
                close()
            except requests.exceptions.HTTPError as httperror:
                print("Http Error : ", httperror)
                close()
            except requests.exceptions.SSLError as sslerror:
                print("SSL Error : ", sslerror)
                close()
            except requests.exceptions.RequestException as error:
                print("AnyException : ", error)
                close()

            if not done:
                time.sleep(self.search_time)

        if found is None:
            self.find_vaccine(vaccine_type, region)

        print(f"주소는 : {found.get('address')} 입니다.")

        organization_code = found.get('orgCode')
        if vaccine_type == "ANY":
            try_vaccine_types = ['VEN00013', 'VEN00014', 'VEN00015', 'VEN00016']
        else:
            try_vaccine_types = [vaccine_type]
        
        for vaccine_type in try_vaccine_types:
            print(f"{vaccine_type} 으로 예약을 시도합니다.")
            if self.try_reservation(organization_code, vaccine_type) is not None:
                return None

        self.find_vaccine(vaccine_type, region)

    def try_reservation(self, organization_code, vaccine_type):
        for i in range(3):
            data = {
                "from": "Map", 
                "vaccineCode": vaccine_type, 
                "orgCode": organization_code, 
                "distance": None
            }
            response = requests.post(self.reservation_url, 
                                    headers=self.header, json=data, cookies=self.login_cookie, verify=False, timeout=7)
            response_json = json.loads(response.text)
            print(response_json)
            for key in response_json:
                value = response_json[key]
                if key != 'code':
                    continue
                if key == 'code' and value == "NO_VACANCY":
                    print("잔여백신 접종 신청이 선착순 마감되었습니다.")
                    time.sleep(0.08)
                elif key == 'code' and value == "SUCCESS":
                    print("백신접종신청 성공!!!")
                    organization_code_success = response_json.get("organization")
                    print(
                        f"병원이름: {organization_code_success.get('orgName')}\t전화번호: {organization_code_success.get('phoneNumber')}\t주소: {organization_code_success.get('address')}\t운영시간: {organization_code_success.get('openHour')}")
                    play_tada()
                    close()
                else:
                    print("ERROR. 아래 메시지를 보고, 예약이 신청된 병원 또는 1339에 예약이 되었는지 확인해보세요.")
                    print(response.text)
                    close()
        return None

    def pretty_print(self, response_json):
        for org in response_json["organizations"]:
            if org.get('status') == "CLOSED" or org.get('status') == "EXHAUSTED":
                continue
            print(
                f"잔여갯수: {org.get('leftCounts')}\t상태: {org.get('status')}\t기관명: {org.get('orgName')}\t주소: {org.get('address')}")
        print(datetime.now())

    def play_tada(self):
        print("*****************************따단따단따단**************************************")
        #playsound(resource_path('tada.mp3'))

def close():
    input("Press Enter to close...")
    sys.exit()