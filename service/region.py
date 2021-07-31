import settings
import json
from service.selenium import Capture
from service.lifecycle import LifeCycleMixin
from selenium.common.exceptions import WebDriverException

class Region:

    @classmethod
    def from_bytes(cls, bytes):
        region_json = json.loads(bytes.decode('utf-8'))
        top_left = (region_json['topLeft']['x'], region_json['topLeft']['y'])
        bottom_right = (region_json['bottomRight']['x'], region_json['bottomRight']['y'])
        return Region(top_left, bottom_right)

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def __str__(self):
        return "좌상 [{:.4f}, {:.4f}] 우하 [{:.4f}, {:.4f}]".format(*self.top_left, *self.bottom_right)

    def __eq__(self, other):
        if isinstance(other, Region):
            return (self.top_left == other.top_left) and (self.bottom_right == other.bottom_right)
        return False

class RegionCapture(Capture, LifeCycleMixin):

    def __init__(self, browser='chrome'):
        super().__init__(browser)
        self.url = settings.url.get('kakao').get('map_page')
        self.last_capture = None

    def _start(self):
        self.driver.get(self.url)
        try:
            while True:
                _ = self.driver.window_handles
                region_requests = list(filter(lambda it: 'left_count_by_coords' in it.url, self.driver.requests))
                if len(region_requests) > 0:
                    tmp_last_region = Region.from_bytes(region_requests[-1].body)
                    if self.last_capture != tmp_last_region:
                        self.last_capture = tmp_last_region
                        self.on_progress_listener(self)
        except WebDriverException:
            print('브라우저가 임의로 닫혔습니다.')
        except KeyboardInterrupt:
            print('키 입력으로 브라우저를 닫았습니다.')
        finally:
            self.validate_last_capture_non_null()

    def validate_last_capture_non_null(self):
        if self.last_capture is None:
            raise RuntimeError('Region이 설정되지 않았습니다.')