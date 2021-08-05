import constant
import json
from service import Capture
from service.lifecycle import LifeCycleMixin

class Region:

    @classmethod
    def from_bytes(cls, bytes):
        region_json = json.loads(bytes.decode('utf-8'))
        top_left = (region_json['topLeft']['x'], region_json['topLeft']['y'])
        bottom_right = (region_json['bottomRight']['x'], region_json['bottomRight']['y'])
        return Region(top_left, bottom_right)

    @classmethod
    def from_json(cls, region_json):
        top_left = (region_json['top_left'][0], region_json['top_left'][1])
        bottom_right = (region_json['bottom_right'][0], region_json['bottom_right'][1])
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

    def convert_to_dto(self):
        return {
            "bottomRight": {
                "x": self.bottom_right[0], 
                "y": self.bottom_right[1]
            }, 
            "onlyLeft": False, 
            "order": "latitude",
            "topLeft": {
                "x": self.top_left[0], 
                "y": self.top_left[1]
            }
        }

class RegionCapture(Capture, LifeCycleMixin):

    def __init__(self, browser='chrome'):
        Capture.__init__(self, browser)
        LifeCycleMixin.__init__(self)
        self.url = constant.url.get('kakao').get('map_page')
        self.last_capture = None

    def _start(self):
        self.open()
        self.driver.get(self.url)
        try:
            while True:
                self.validate_driver_non_null()
                region_requests = list(filter(lambda it: 'left_count_by_coords' in it.url, self.driver.requests))
                if len(region_requests) > 0:
                    self.update_last_capture(Region.from_bytes(region_requests[-1].body))
        except RegionCapture.WebDriverException as e:
            print(e)
        except KeyboardInterrupt:
            print(RegionCapture.KeyboardInterrupt())
        self.validate_last_capture_non_null()

    def validate_driver_non_null(self):
        try:
            _ = self.driver.window_handles
        except:
            raise RegionCapture.WebDriverException()

    def update_last_capture(self, tmp_capture):
        if self.last_capture != tmp_capture:
            self.last_capture = tmp_capture
            self.on_progress_listener(self)

    def validate_last_capture_non_null(self):
        if self.last_capture is None:
            raise RegionCapture.NullCaptureException()

    class KeyboardInterrupt(RuntimeError):
        
        def __init__(self, message='키보드 입력으로 종료되었습니다.'):
            super().__init__(message)

    class WebDriverException(RuntimeError):
        
        def __init__(self, message='웹 드라이버가 임의로 종료되었습니다.'):
            super().__init__(message)

    class NullCaptureException(RuntimeError):
        
        def __init__(self, message='캡쳐한 정보가 없습니다.'):
            super().__init__(message)