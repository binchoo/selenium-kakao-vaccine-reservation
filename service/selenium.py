class SeleniumAware:
    
    driver_dependency_map = None
    
    def __init__(self, browser: str):
        if browser not in self.driver_dependency_map.keys():
            print(f'{browser}는 잘못된 브라우저 지정이므로, 기본값 chrome을 사용합니다.')
            browser = 'chrome'
        self.Driver, self.BinaryManager = self.driver_dependency_map.get(browser)
        self.browser = browser

    def open(self):
        self.driver = self.Driver(self.BinaryManager().install())
    
    def close(self):
        self.driver.close()   
        
class Hooker(SeleniumAware):
    pass

class Capture(SeleniumAware):
    pass
