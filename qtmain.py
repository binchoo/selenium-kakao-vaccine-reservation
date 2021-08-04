import settings # this line runs settings' bootstrap
import pprint
import time
from threading import Thread

from PyQt5.QtWidgets import QApplication
from view.main import MainView
from service.login import KakaoLoginHooker, kakaoUserValidity
from service.region import RegionCapture
from service.reservation import LegacyVaccineReservation

def main():
    coords = run_interval = login_cookie = None
    app, view = None
    login_hook = region_capture = reservation = None


def create_app_and_view():
    app = QApplication([])
    app.setStyle('Fusion')
    app.setApplicationName('COVID-19 Vaccine Auto Reservaion')

if __name__ == '__main__':
    main()