import settings
from service.lifecycle import LifeCycleMixin

class Capture(LifeCycleMixin):
    
    driver_dependency_map = settings.RequestCaptureDependencyMap

    def __init__(self, browser: str):
        if browser not in self.driver_dependency_map.keys():
            print(f'{browser}는 잘못된 브라우저 지정이므로, 기본값 chrome을 사용합니다.')
            browser = 'chrome'
        Driver, BinaryManager = self.driver_dependency_map.get(browser)
        self.driver = Driver(BinaryManager().install())
        self.browser = browser
        
    def start(self):
        self.on_start_listener(self)
        self._start()
        self.on_end_listener(self)

    def _start(self):
        raise NotImplementedError