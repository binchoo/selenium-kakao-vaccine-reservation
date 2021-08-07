import constant
import requests, json
import time
from datetime import datetime

from service.lifecycle import LifeCycleMixin
from dto.vaccine import VaccineVendor

class LegacyVaccineReservation(LifeCycleMixin):

    def __init__(self):
        super().__init__()
        self.left_by_coords_url = constant.url.get('kakao').get('left_by_coords')
        self.org_inventory_url = constant.url.get('kakao').get('org_inventory')
        self.reservation_url = constant.url.get('kakao').get('reservation')
        self.header = constant.header.get('kakao')
        self.view_logger = None

    setup_properties = ['login_cookie', 'region', 'run_interval', 'vaccine_type']

    def setup(self):
        self.validate_dependencies()
        self.region_data = self.region.convert_to_dto()
        self.vaccine_type = VaccineVendor.ANY #TODO: 백신 타입 외부 주입하기
        self.kill = False

    def validate_dependencies(self):
        if not all(
            [hasattr(self, prop) and getattr(self, prop) is not None for prop in self.setup_properties]
        ):
            raise RuntimeError('필요한 의존성이 전달되지 않았습니다.')

    def _start(self):
        self.setup()
        while not self.kill:
            self._print(datetime.now())
            organizations = self.get_available_organizations() #
            if len(organizations) > 0:
                self._print_orgarnizations(organizations)
                try_vaccine_types = [self.vaccine_type] if VaccineVendor.ANY != self.vaccine_type else VaccineVendor.values()
                if self.try_reservation(organizations, try_vaccine_types):
                    break
            else:
                time.sleep(self.run_interval)

    def get_available_organizations(self):
        response = self._fail_safe_api(self.left_by_coords_url, method='post', expects=[200],
                                        headers=self.header, json=self.region_data, verify=False)
        if response is not None:
            response_json = json.loads(response.text)
            print(response_json)
            available_organizations = list(
                filter(lambda org: org['status'] == 'AVAILABLE' or org['leftCounts'] > 0, response_json.get('organizations'))
            )
        else:
            available_organizations = []
        return available_organizations

    def get_organization_inventory(self, organization):
        org_code = organization['orgCode']
        url = self.org_inventory_url.format(org_code)
        response = self._fail_safe_api(url, method='get', expects=[200], cookies=self.login_cookie, headers=self.header, verify=False)
        if response is not None:
            response_json = json.loads(response.text)
            print(response_json)
            inventory = response_json['selectableVaccineCodes']
        else:
            inventory = []
        return inventory

    def try_reservation(self, organizations, try_vaccine_types):
        for org in organizations:
            if self.kill:
                break
            org_code = org['orgCode']
            org_inventory = self.get_organization_inventory(org)
            for vaccine_type in set(try_vaccine_types) & set(org_inventory):
                self._print(f"{vaccine_type} 으로 예약을 시도합니다.")

                data = { 'from': 'Map', 'vaccineCode': vaccine_type, 'orgCode': org_code, 'distance': None }
                response = self._fail_safe_api(self.reservation_url, method='post', expects=[200, 403], cookies=self.login_cookie,
                                                headers=self.header, json=data, verify=False, timeout=7)
                if response is not None:
                    response_json = json.loads(response.text) #
                    result_code = response_json['code']
                    
                    print(response_json)
                    if 'desc' in response_json.keys():
                        self._print(response_json['desc'])
                        
                    if result_code == 'SUCCESS':
                        org = response_json.get('organization')
                        self._print("백신 접종 신청 성공!!!")
                        self._print(f"""
                            기관명: {org.get('orgName')}
                            전화번호: {org.get('phoneNumber')}
                            주소: {org.get('address')}
                            운영시간: {org.get('openHour')}""")
                        return True
                    elif result_code == 'NO_VACANCY':
                        pass
                    else:
                        self._print("ERROR. 아래 메시지를 보고, 예약이 신청된 병원 또는 1339에 예약이 되었는지 확인해보세요.")
                        self._print(response.text)
        return False

    def _fail_safe_api(self, url, method, expects, **kwargs):
        request_func = getattr(requests, method)
        response = None
        try:
            response = request_func(url, **kwargs)
            if response.status_code not in expects:
                print('Response Error Occurred: ', response.status_code)
                print(response.text)
                raise requests.exceptions.ConnectionError
        except requests.exceptions.Timeout as timeouterror:
            print("Timeout Error : ", timeouterror)
        except requests.exceptions.ConnectionError as connectionerror:
            print("Connecting Error : ", connectionerror)
        except requests.exceptions.HTTPError as httperror:
            print("Http Error : ", httperror)
        except requests.exceptions.SSLError as sslerror:
            print("SSL Error : ", sslerror)
        except requests.exceptions.RequestException as error:
            print("AnyException : ", error)
        return response

    def _print(self, msg):
        if self.view_logger is not None:
            self.view_logger.log(str(msg))
        print(msg)

    def _print_orgarnizations(self, organizations):
        for org in organizations:
            self._print(f"""
                    기관명: {org.get('orgName')}
                    주소: {org.get('address')}
                    잔여갯수: {org.get('leftCounts')}
                    상태: {org.get('status')}\n""")

    def interrupt(self):
        self.kill = True

    def set_view_logger(self, qtwidget):
        self.view_logger = qtwidget

    def mock(self):
        x =  {'orgCode': '12358681', 'orgName': '곽내과의원', 'address': '서울 종로구 자하문로 58', 'x': 126.97120895207867, 'y': 37.581253855387715, 'status': 'AVAILABLE', 'leftCounts': 11}
        y = {'orgCode': '12358681', 'orgName': '박박박의원', 'address': '서울 종로구 자하문로  11', 'x': 126.97120895207867, 'y': 37.581253855387715, 'status': 'AVAILABLE', 'leftCounts': 11}
        return [x, y]