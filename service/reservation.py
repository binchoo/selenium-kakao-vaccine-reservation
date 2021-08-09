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

    setup_properties = ['login_cookie', 'region', 'run_interval', 'vaccine_types']

    def setup(self):
        self.validate_dependencies()
        self.region_data = self.region.convert_to_dto()
        self.try_vaccine_types = [enum.value for enum in self.vaccine_types]
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
                if self.try_reservation(organizations):
                    break
                else:
                    time.sleep(self.run_interval)
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
        
        inventory = []
        if response is not None:
            response_json = json.loads(response.text)
            for left in response_json['lefts']:
                if left['leftCount'] > 0:
                    inventory.append(left['vaccineCode'])
        return inventory

    def try_reservation(self, organizations):
        self._print(f"{len(organizations)}개 기관에 대해 예약 시도중..")
        for org in organizations:
            if self.kill:
                break
            org_inventory = self.get_organization_inventory(org)
            for vaccine_type in set(self.try_vaccine_types) & set(org_inventory):
                self._print(f"{vaccine_type} 으로 예약을 시도합니다.")
                self._print_orgarnization(org)

                data = { 'from': 'Map', 'vaccineCode': vaccine_type, 'orgCode': org['orgCode'], 'distance': None }
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

    def _print_orgarnization(self, organization):
        self._print(f"""
            기관명: {organization.get('orgName')}
            주소: {organization.get('address')}
            잔여갯수: {organization.get('leftCounts')}
            상태: {organization.get('status')}\n""")

    def interrupt(self):
        self.kill = True

    def set_view_logger(self, qtwidget):
        self.view_logger = qtwidget

    def mock(self):
        x =  {'orgCode': '12358681', 'orgName': '곽내과의원', 'address': '서울 종로구 자하문로 58', 'x': 126.97120895207867, 'y': 37.581253855387715, 'status': 'AVAILABLE', 'leftCounts': 11}
        y = {'orgCode': '12358681', 'orgName': '박박박의원', 'address': '서울 종로구 자하문로  11', 'x': 126.97120895207867, 'y': 37.581253855387715, 'status': 'AVAILABLE', 'leftCounts': 11}
        return [x, y]