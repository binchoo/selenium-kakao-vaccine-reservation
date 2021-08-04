import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QComboBox, QGroupBox, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from .qwidget_wrap import apply_qwidget_wrapping

logger = logging.getLogger(__name__)
apply_qwidget_wrapping()

class MainView(QWidget):
    
    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent

        self.platformConfig = PlatformConfig(self, config)
        self.userConfig = UserConfig(self, config)
        self.macroConfig = MacroConfig(self, config)
        self.macroLogs = MacroLogs(self, config)
        self.setup()

    def setup(self):
        self.setStyleSheet('background-color: white;')
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.show()

    def setChildren(self):
        self.addChild(self.platformConfig)
        self.addChild(self.userConfig)
        self.addChild(self.macroConfig)
        self.addChild(self.macroLogs)
        
class PlatformConfig(QWidget):
    
    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent

        if config is not None:
            self.platforms = config['platforms']
        else:
            self.mock()

        self.paltfromLabel = QLabel()
        self.platformComboBox = QComboBox()
        self.setup()

    def setup(self):
        self.useLayout(QHBoxLayout())
        self.setChildren()
        self.setupLabel()
        self.setupComoboBox()

    def setChildren(self):
        self.addChild(self.paltfromLabel)
        self.addChild(self.platformComboBox)
        
    def setupLabel(self):
        self.paltfromLabel.setText('플랫폼 선택:')

    def setupComoboBox(self):
        self.platformComboBox.addItems(self.platforms)

    def mock(self):
        self.platforms = ['kakao', 'naver']

class UserConfig(QWidget):
    
    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent

        self.loginConfig = LoginConfig(self, config)
        self.regionConfig = RegionConfig(self, config)
        self.setup()

    def setup(self):
        self.useLayout(QHBoxLayout())
        self.setChildren()

    def setChildren(self):
        self.addChild(self.loginConfig)
        self.addChild(self.regionConfig)

class LoginConfig(QGroupBox):

    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent
        if config is not None:
            self.loginCookie = config['login_cookie']
        else:
            self.mock()

        self.loginStatus = LoginStatus(self, config)
        self.browserButton = QPushButton()
        self.setup()

    def setup(self):
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.setupButton()

    def setChildren(self):
        self.addChild(self.loginStatus)
        self.addChild(self.browserButton)

    def setupButton(self):
        self.browserButton.setText('브라우저 로그인')
        self.browserButton.setStyleSheet('''QPushButton {
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

    def mock(self):
        self.loginCookie = None

class LoginStatus(QWidget):

    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent
        if config is not None:
            self.statusDisplay = config['status_display']
        else:
            self.mock()

        self.statusLabel = QLabel()
        self.statusVariable = QLabel()
        self.setup()

    def setup(self):
        self.useLayout(QHBoxLayout())
        self.setChildren()
        self.setupLabel()

    def setChildren(self):
        self.addChild(self.statusLabel)
        self.addChild(self.statusVariable)

    def setupLabel(self):
        self.statusLabel.setText('계정 상태: ')
        self.notifyStatusChanged('none')

    def notifyStatusChanged(self, newStatus):
        text = self.statusDisplay[newStatus]['text']
        color = self.statusDisplay[newStatus]['color']
        self.statusVariable.setText(text)
        self.statusVariable.setStyleSheet(f'color: {color};')

    def mock(self):
        self.statusDisplay = {
            'none': {
                'text': '정보 없음',
                'color': 'orange'
            },
            'expired': {
                'text': '만료됨',
                'color': 'red'
            },
            'ok': {
                'text': '유효함',
                'color': 'green'
            }
        }

class RegionConfig(QGroupBox):
    
    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent
        if config is not None:
            self.coords = config['coords']
        else:
            self.mock()

        self.topLeftLabel = QLabel()
        self.topLeftVariable = QLineEdit()
        self.bottomRightLabel = QLabel()
        self.bottomRightVariable = QLineEdit()
        self.browserButton = QPushButton()
        self.setup()

    def setup(self):
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.setupLabel()
        self.setupLineEdit()
        self.setupButton()

    def setChildren(self):
        self.addChild(self.topLeftLabel)
        self.addChild(self.topLeftVariable)
        self.addChild(self.bottomRightLabel)
        self.addChild(self.bottomRightVariable)
        self.addChild(self.browserButton)

    def setupLabel(self):
        self.topLeftLabel.setText('좌상단 좌표')
        self.bottomRightLabel.setText('우하단 좌표')

    def setupLineEdit(self):
        self.notifyRegionChanged(self.coords['top_left'], self.coords['bottom_right'])

    def notifyRegionChanged(self, topLeft, bottomRight):
        self.topLeftVariable.setText(topLeft)
        self.bottomRightVariable.setText(bottomRight)
    
    def setupButton(self):
        self.browserButton.setText('브라우저로 탐지')
        self.browserButton.setStyleSheet('''QPushButton {
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

    def mock(self):
        self.coords = {
            'top_left': '(0, 0)',
            'bottom_right': '(0, 0)'
        }

class MacroConfig(QWidget):
    
    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent
        if config is not None:
            self.macroInterval = config['macro_interval']
        else:
            self.mock()
        self.macroIntervalLabel = QLabel()
        self.macroIntervalVariable = QLineEdit()
        self.startButton = QPushButton()
        self.pauseButton = QPushButton()
        self.setup()

    def setup(self):
        self.useLayout(QHBoxLayout())
        self.setChildren()
        self.setupLabel()
        self.setupVariable()
        self.setupButton()
        
    def setChildren(self):
        self.addChild(self.macroIntervalLabel)
        self.addChild(self.macroIntervalVariable)
        self.addChild(self.startButton)
        self.addChild(self.pauseButton)

    def setupLabel(self):
        self.macroIntervalLabel.setText('매크로 수행 주기: ')
    
    def setupVariable(self):
        self.macroIntervalVariable.setText(self.macroInterval)

    def setupButton(self):
        self.startButton.setText('시작')
        self.startButton.setEnabled(False)
        self.pauseButton.setText('일시정지')
        self.pauseButton.setEnabled(False)

    def mock(self):
        self.macroInterval = str(7)

class MacroLogs(QWidget):

    def __init__(self, parent=None, config=None):
        super().__init__()
        self.parent = parent

        self.macroLogsLabel = QLabel()
        self.marcoLogsTextEdit = QTextEdit()
        self.setup()

    def setup(self):
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.setupLabel()
        self.setupTextEdit()

    def setChildren(self):
        self.addChild(self.macroLogsLabel)
        self.addChild(self.marcoLogsTextEdit)
    
    def setupLabel(self):
        self.macroLogsLabel.setText('매크로 수행 로그')

    def setupTextEdit(self):
        self.marcoLogsTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def appendLog(self, text):
        prev = self.marcoLogsTextEdit.getText()
        self.macroLogsTextEdit.setText(prev + '\n' + text)