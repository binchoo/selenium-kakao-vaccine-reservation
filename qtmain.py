from bootstrap import settings # this line runs settings' bootstrap
from bootstrap.model import JsonModel
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation
from view.main import MainView

from PyQt5.QtWidgets import QApplication
from threading import Thread

model = JsonModel(json=settings.initial_context)

def main():

    from constant import CONTEXT_PATH, USER_VALIDITY_TO_VIEW_VALIDITY, APP_NAME, QAPP_STYLE

    app = view = None
    login_hooker = region_capture = reservation = None

    def use_saved_model():
        try:
            saved_model = JsonModel.from_file(CONTEXT_PATH)
            saved_model = JsonModel.convert(saved_model, settings.deserialize_converter)
        except:
            return
        model.update('login_cookie', saved_model.login_cookie)
        model.update('region', saved_model.region)
        model.update('run_interval', saved_model.run_interval)
        userValidity = USER_VALIDITY_TO_VIEW_VALIDITY[kakaoUserValidity(saved_model.login_cookie)]
        model.update('user_validity', userValidity)

    def save_model():
        to_save = JsonModel.convert(model, 
                                    settings.serialize_converter, 
                                    attrs=['login_cookie', 'region', 'run_interval'])
        to_save.dump(CONTEXT_PATH)
        print(to_save.dumps())

    def create_app_and_view():
        app = QApplication([])
        app.setApplicationName(APP_NAME)
        app.setStyle(QAPP_STYLE)
        return app, MainView(model=model)

    def create_login_hooker():

        def validate_login_info(hooker):
            if hooker.login_info is not None:
                login_cookie = { item['name']:item['value'] for item in hooker.login_info}
                user_validity = kakaoUserValidity(login_cookie)
                model.update('login_cookie', login_cookie)
                model.update('user_validity', USER_VALIDITY_TO_VIEW_VALIDITY[user_validity])

        def error_handler(hooker, error):
            view.popMessageBox('브라우저 닫힘', f'브라우저가 임의로 닫혔습니다.')

        hooker = KakaoLoginHooker(browser=model.browser, waits=model.login_waits)
        hooker.on_end(validate_login_info)
        hooker.on_error(error_handler)
        return hooker

    def create_region_capture():

        def show_current_region(capture):
            current_region = capture.last_capture
            model.update('current_region', current_region)
            print("region_capture> 현재 보고 있는 영역")
            print('\t', current_region)
            print('\t', '브라우저를 닫으면 이 영역을 백신 검색에 사용합니다.', end='\n\n')
            
        def commit_region(capture):
            model.update('region', capture.last_capture)

        def error_handler(capture, error):
            try:
                raise error
            except RegionCapture.NullCaptureException:
                print('지정 영역을 탐지하기 전까지 브라우저를 닫지 마세요.')
                capture.start()
        
        capture = RegionCapture(model.browser)
        capture.on_progress(show_current_region)
        capture.on_end(commit_region)
        capture.on_error(error_handler)
        return capture

    def create_reservation():

        def set_running_true(resv):
            model.update('running', True)

        def set_running_false(resv):
            model.update('running', False)

        reservation = LegacyVaccineReservation()
        reservation.set_view_logger(view.macroLogs)
        reservation.on_start(set_running_true)
        reservation.on_end(set_running_false)
        return reservation

    def register_view_handler():

        def run_login_hooker():
            login_hooker.start()

        def run_region_capture():
            capture_start = lambda: region_capture.start()
            capture_thread = Thread(target=capture_start)
            capture_thread.start()

        def run_reservation_macro():
            model.update('run_interval', view.getRunInterval(default=7))
            model.update('vaccine_type', view.getTryVaccineTypes())
            reservation_start = lambda: reservation.start(
                                            login_cookie=model.login_cookie, 
                                            region=model.region, vaccine_types=model.vaccine_types, run_interval=model.run_interval)
            reservation_thread = Thread(target=reservation_start)
            reservation_thread.start()
            save_model()

        def stop_reservation_macro():
            reservation.interrupt()

        view.onLoginBrowserClicked(run_login_hooker)
        view.onRegionBrowserClicked(run_region_capture)
        view.onStartButtonClicked(run_reservation_macro)
        view.onStopButtonClicked(stop_reservation_macro)

    app, view = create_app_and_view()
    login_hooker = create_login_hooker()
    region_capture = create_region_capture()
    reservation = create_reservation()
    register_view_handler()

    use_saved_model()
    app.exec()

if __name__ == '__main__':
    main()
