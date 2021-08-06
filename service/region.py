import constant
import json
from dto.region import Region
from service import Capture
from service.lifecycle import LifeCycleMixin

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