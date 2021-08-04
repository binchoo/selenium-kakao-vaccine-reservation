from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QComboBox, QGroupBox, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from qwidget_wrap import apply_qwidget_wrapping

apply_qwidget_wrapping()
app = QApplication([])
app.setStyle('Fusion')
app.setApplicationName('COVID-19 Vaccine Auto Reservation')

full_widget = QWidget()
full_widget.useLayout(QVBoxLayout())
full_widget.setStyleSheet('background-color: white;')

# full_widget > platform_config
platform_config = full_widget.addChild(QWidget())
platform_config.useLayout(QHBoxLayout())
platform_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# full_widget > user_config
user_config = full_widget.addChild(QWidget())
user_config.useLayout(QHBoxLayout())
user_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# full_widget > macro_config
macro_config = full_widget.addChild(QWidget())
macro_config.useLayout(QHBoxLayout())
macro_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# full_widget > macro_run
macro_run = full_widget.addChild(QWidget())
macro_run.useLayout(QVBoxLayout())


# full_widget > platform_config > platform_combobox
platform_config.addChild(QLabel('플랫폼 선택: '))
platform_combobox = platform_config.addChild(QComboBox())
platform_combobox.addItems(['kakao'])

# full_widget > user_config > login_config
login_config = user_config.addChild(QGroupBox('로그인 정보'))
login_config_layout = QVBoxLayout()
login_config.useLayout(login_config_layout)

# full_widget > user_config > region_config
region_config = user_config.addChild(QGroupBox('지역 정보'))
region_config.useLayout(QVBoxLayout())

# full_widget > macro_config > interval and buttons
macro_config.addChild(QLabel('매크로 수행 주기: '))
time_interval_input = macro_config.addChild(QLineEdit('7'))
macro_config.addChild(QLabel('sec'))

start_button = macro_config.addChild(QPushButton('시작'))
start_button.setEnabled(False)

pause_button = macro_config.addChild(QPushButton('일시정지'))
pause_button.setEnabled(False)

# full_widget > macro_run > macro_logs
macro_run.addChild(QLabel('매크로 수행 로그'))
macro_logs = macro_run.addChild(QTextEdit())
macro_logs.setTextInteractionFlags(Qt.TextSelectableByMouse)


# full_widget > user_config > login_config > login_status
login_status = login_config.addChild(QWidget())
login_status.useLayout(QHBoxLayout())

# full_widget > user_config > login_config > browser button
login_browser_button = login_config.addChild(QPushButton('브라우저 로그인'))
login_browser_button.setStyleSheet('''QPushButton {
    border: 1px solid #53B555;
    border-radius: 3px;
    color: #53B555;
    background-color: #DFF4DC;
    min-height: 30px;
}

QPushButton:hover {
    color: white;
    background-color: #53B555;
}

QPushButton:pressed {
    background-color: #3E873F;
}
''')
login_config_layout.setAlignment(login_status, Qt.AlignTop)

# full_widget > user_config > region_config > coord inputs & brwoser button
region_config.addChild(QLabel('좌상단 좌표'))
topleft_variable = region_config.addChild(QLineEdit())

region_config.addChild(QLabel('우하단 좌표'))
bottomright_variable = region_config.addChild(QLineEdit())

region_browser_button = region_config.addChild(QPushButton('브라우저 캡쳐'))
region_browser_button.setStyleSheet('''QPushButton {
    border: 1px solid #53B555;
    border-radius: 3px;
    color: #53B555;
    background-color: #DFF4DC;
    min-height: 30px;
}

QPushButton:hover {
    color: white;
    background-color: #53B555;
}

QPushButton:pressed {
    background-color: #3E873F;
}
''')


# full_widget > user_config > login_config > login_status > login_status_variable
login_status.addChild(QLabel('계정 상태:'))
login_status_variable = login_status.addChild(QLabel('정보 없음'))
login_status_variable.setStyleSheet('QLabel { color: orange; }')


full_widget.show()
app.exec()