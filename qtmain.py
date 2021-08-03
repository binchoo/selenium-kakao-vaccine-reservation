from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QComboBox, QGroupBox, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt

app = QApplication([])
app.setStyle('Fusion')
app.setApplicationName('COVID-19 Vaccine Auto Reservation')

# 1st view hierarchy
platform_config_layout = QHBoxLayout()
platform_config = QWidget()
platform_config.setLayout(platform_config_layout)
platform_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

user_config_layout = QHBoxLayout()
user_config = QWidget()
user_config.setLayout(user_config_layout)
user_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

macro_config_layout = QHBoxLayout()
macro_config = QWidget()
macro_config.setLayout(macro_config_layout)
macro_config.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

macro_run_layout = QVBoxLayout()
macro_run = QWidget()
macro_run.setLayout(macro_run_layout)

full_widget_layout = QVBoxLayout()
full_widget_layout.addWidget(platform_config)
full_widget_layout.addWidget(user_config)
full_widget_layout.addWidget(macro_config)
full_widget_layout.addWidget(macro_run)

full_widget = QWidget()
full_widget.setLayout(full_widget_layout)
full_widget.setStyleSheet('background-color: white;')

# 2nd view hierarchy
platfrom_label = QLabel('플랫폼 선택: ')
platform_combobox = QComboBox()
platform_combobox.addItems(['kakao'])
platform_config_layout.addWidget(platfrom_label)
platform_config_layout.addWidget(platform_combobox)

login_config_layout = QVBoxLayout() #3rd
login_config = QGroupBox('로그인 정보') 
login_config.setLayout(login_config_layout)
user_config_layout.addWidget(login_config)

region_config_layout = QVBoxLayout() #3rd
region_config = QGroupBox('지역 정보')
region_config.setLayout(region_config_layout)
user_config_layout.addWidget(region_config)

time_interval_label = QLabel('매크로 수행 주기: ')
time_interval_input = QLineEdit('7')
sec_label = QLabel('sec')
start_button = QPushButton('시작')
start_button.setEnabled(False)
pause_button = QPushButton('일시정지')
pause_button.setEnabled(False)
macro_config_layout.addWidget(time_interval_label)
macro_config_layout.addWidget(time_interval_input)
macro_config_layout.addWidget(sec_label)
macro_config_layout.addWidget(start_button)
macro_config_layout.addWidget(pause_button)

macro_logs_label = QLabel('매크로 수행 로그')
macro_logs = QTextEdit()
macro_logs.setTextInteractionFlags(Qt.TextSelectableByMouse)
macro_run_layout.addWidget(macro_logs_label)
macro_run_layout.addWidget(macro_logs)

# 3rd view hierarchy
login_status = QWidget()
login_status_layout = QHBoxLayout() #4th
login_status.setLayout(login_status_layout)
login_browser_button = QPushButton('브라우저 로그인')
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
login_config_layout.addWidget(login_status)
login_config_layout.addWidget(login_browser_button)
login_config_layout.setAlignment(login_status, Qt.AlignTop)

topleft_label = QLabel('좌상단 좌표')
topleft_variable = QLineEdit()
bottomright_label = QLabel('우상단 좌표')
bottomright_variable = QLineEdit()
region_browser_button = QPushButton('브라우저 캡쳐')
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
region_config_layout.addWidget(topleft_label)
region_config_layout.addWidget(topleft_variable)
region_config_layout.addWidget(bottomright_label)
region_config_layout.addWidget(bottomright_variable)
region_config_layout.addWidget(region_browser_button)

# 4th view hierarchy
login_status_label = QLabel('계정 상태:')
login_status_variable = QLabel('정보 없음')
login_status_variable.setStyleSheet('QLabel { color: orange; }')
login_status_layout.addWidget(login_status_label)
login_status_layout.addWidget(login_status_variable)

full_widget.show()
app.exec()