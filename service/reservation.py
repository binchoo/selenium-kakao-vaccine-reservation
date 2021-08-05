import constant
import requests, json
from datetime import datetime
import time
from service.lifecycle import LifeCycleMixin

class LegacyVaccineReservation(LifeCycleMixin):

    def __init__(self, login_cookie, region, interval=7):
        super().__init__()
        self.login_cookie = login_cookie
        self.region = region
        self.search_time = interval
        self.header = constant.header.get('kakao')
        self.reservation_url = constant.url.get('kakao').get('reservation')
        self._kill = False
        self.vaccine_type = "ANY"

    def start(self):
        self.on_start_listener(self)
        self._start()
        self.on_end_listener(self)

    def vaccine_type_input(self): #TODO: 미아 코드 제거
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

    def _start(self):
        found = False
        while not found and not self._kill: 
            vaccine_remaining = self.find_vaccine_remaining("ANY") #TODO: 백신 타입 값 인젝션 추가하기
            if vaccine_remaining is None:
                time.sleep(self.search_time)
            else:
                print(f"주소는 : {vaccine_remaining.get('address')} 입니다.")
                organization_code = vaccine_remaining.get('orgCode')

                if self.vaccine_type == "ANY":
                    try_vaccine_types = ['VEN00013', 'VEN00014', 'VEN00015', 'VEN00016']
                else:
                    try_vaccine_types = [self.vaccine_type]
                
                for vaccine_type in try_vaccine_types:
                    if self.try_reservation(organization_code, vaccine_type):
                        found = True
                        self._kill = True
                        break

    def _print(self, msg):
        if self.on_progress_listener is not None:
            self.getMessage = lambda: msg
            self.on_progress_listener(self)
        print(msg)

    def find_vaccine_remaining(self, vaccine_type):
        left_by_coords_url = constant.url.get('kakao').get('left_by_coords')
        data = self.region.convert_to_dto()
        vaccine_remaining = None
        try:
            response = requests.post(left_by_coords_url, headers=self.header, json=data, verify=False)
            response_json = json.loads(response.text)        
            print(response_json)

            if response.status_code != 200:
                print('Response Error Occurred.')
                raise requests.exceptions.ConnectionError

            self.pretty_print(response_json)
            for x in response_json.get("organizations"):
                if x.get("status") == "AVAILABLE" or x.get("leftCounts") != 0:
                    vaccine_remaining = x
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

        return vaccine_remaining

    def try_reservation(self, organization_code, vaccine_type, try_loops=3):
        self._print(f"{vaccine_type} 으로 예약을 시도합니다.")
        for i in range(try_loops):
            if self._kill:
                break
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

            if response.status_code != 200:
                print('Response Error Occurred.')
                continue

            for key in response_json:
                value = response_json[key]
                if key != 'code':
                    continue
                if key == 'code' and value == "NO_VACANCY":
                    self._print("잔여백신 접종 신청이 선착순 마감되었습니다.")
                    time.sleep(0.08)
                elif key == 'code' and value == "SUCCESS":
                    self._print("백신접종신청 성공!!!")
                    organization_code_success = response_json.get("organization")
                    self._print(
                        f"병원이름: {organization_code_success.get('orgName')}\t전화번호: {organization_code_success.get('phoneNumber')}\t주소: {organization_code_success.get('address')}\t운영시간: {organization_code_success.get('openHour')}")
                    return True
                else:
                    self._print("ERROR. 아래 메시지를 보고, 예약이 신청된 병원 또는 1339에 예약이 되었는지 확인해보세요.")
                    self._print(response.text)
        return False

    def pretty_print(self, response_json):
        for org in response_json["organizations"]:
            if org.get('status') == "CLOSED" or org.get('status') == "EXHAUSTED":
                continue
            print(
                f"잔여갯수: {org.get('leftCounts')}\t상태: {org.get('status')}\t기관명: {org.get('orgName')}\t주소: {org.get('address')}")
        self._print(str(datetime.now()))

    def interrupt(self):
        self._kill = True

    def mock(self):
        x =  {'orgCode': '12358681', 'orgName': '곽내과의원', 'address': '서울 종로구 자하문로 58', 'x': 126.97120895207867, 'y': 37.581253855387715, 'status': 'AVAILABLE', 'leftCounts': 11}
        return x