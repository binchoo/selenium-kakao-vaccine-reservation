from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .qwidget_wrap import apply_qwidget_wrapping

apply_qwidget_wrapping()

class MainView(QWidget):
    
    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent
        self.model = model

        self.platformConfig = PlatformConfig(self, model)
        self.userConfig = UserConfig(self, model)
        self.vaccineConfig = VaccineConfig(self, model)
        self.macroConfig = MacroConfig(self, model)
        self.macroLogs = MacroLogs(self, model)
        self.setup()

    def setup(self):
        self.setStyleSheet('background-color: white;')
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.setSubscription()
        self.show()

    def setChildren(self):
        self.addChild(self.platformConfig)
        self.addChild(self.userConfig)
        self.addChild(self.macroConfig)
        self.addChild(self.macroLogs)

    def setSubscription(self):
        if self.model is not None:
            self.model.subscribe('user_validity', self.notifyUserValidity)
            self.model.subscribe('user_validity', self.updateButtons)
            self.model.subscribe('region', self.notifyRegion)
            self.model.subscribe('region', self.updateButtons)
            self.model.subscribe('run_interval', self.notifyRunInterval)
            self.model.subscribe('running', self.updateButtons)

    def popMessageBox(self, title, text):
        try:
            messageBox = QMessageBox()
            messageBox.setWindowTitle(title)
            messageBox.setText(text)
            messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
            messageBox.setIcon(QMessageBox.Information)
            messageBox.exec()
        except:
            pass

    # event handlers
    def onLoginBrowserClicked(self, func):
        self.userConfig.loginConfig.browserButton.clicked.connect(func)

    def onRegionBrowserClicked(self, func):
        self.userConfig.regionConfig.browserButton.clicked.connect(func)

    def onStartButtonClicked(self, func):
        self.macroConfig.startButton.clicked.connect(func)

    def onStopButtonClicked(self, func):
        self.macroConfig.stopButton.clicked.connect(func)

    # data notification
    def notifyUserValidity(self, model, attr, validity):
        self.userConfig.loginConfig.loginStatus.notifyStatusChanged(validity)
    
    def notifyRegion(self, model, attr, region):
        self.userConfig.regionConfig.notifyRegionChanged(region.top_left, region.bottom_right)

    def notifyRunInterval(self, model, attr, run_interval):
        self.macroConfig.macroIntervalVariable.setText(str(run_interval))

    def updateButtons(self, model, attr, value):
        cookie_is_ok = self.model.has_value('login_cookie')
        region_is_ok = self.model.has_value('region')
        running = self.model.running
        valid_user = self.userConfig.loginConfig.loginStatus.isOk()

        if cookie_is_ok and region_is_ok and valid_user:
            if not running:
                self.macroConfig.startButton.setEnabled(True)
                self.macroConfig.stopButton.setEnabled(False)
                self.popMessageBox('정보 완성', '매크로를 수행 가능합니다.')
            else:
                self.macroConfig.startButton.setEnabled(False)
                self.macroConfig.stopButton.setEnabled(True)
        else:
            self.macroConfig.startButton.setEnabled(False)
            self.macroConfig.stopButton.setEnabled(False)

    def getRunInterval(self, default):
        try:
            interval_text = self.macroConfig.macroIntervalVariable.text()
            for ch in [' ', '-']:
                interval_text = interval_text.replace(ch, '')
            interval = float(interval_text)
        except:
            return default
        return interval
        
class PlatformConfig(QWidget):
    
    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent

        if model is not None:
            self.platforms = model['platforms']
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
        self.paltfromLabel.setText('플랫폼 선택')

    def setupComoboBox(self):
        self.platformComboBox.addItems(self.platforms)

    def mock(self):
        self.platforms = ['kakao']

class UserConfig(QWidget):
    
    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent

        self.loginConfig = LoginConfig(self, model)
        self.regionConfig = RegionConfig(self, model)
        self.setup()

    def setup(self):
        self.useLayout(QHBoxLayout())
        self.setChildren()

    def setChildren(self):
        self.addChild(self.loginConfig)
        self.addChild(self.regionConfig)

class LoginConfig(QGroupBox):

    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent

        self.loginStatus = LoginStatus(self, model)
        self.browserButton = QPushButton()
        self.setup()

    def setup(self):
        self.setTitle('로그인 정보 설정')
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

class LoginStatus(QWidget):

    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent
        self.status = 'none'
        if model is not None:
            self.statusDisplay = model.status_display
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
        self.status = newStatus

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
    
    def isOk(self):
        return self.status == 'ok'

class RegionConfig(QGroupBox):
    
    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent
        if model is not None:
            self.region = model.region
        else:
            self.mock()

        self.topLeftLabel = QLabel()
        self.topLeftVariable = QLineEdit()
        self.bottomRightLabel = QLabel()
        self.bottomRightVariable = QLineEdit()
        self.browserButton = QPushButton()
        self.setup()

    def setup(self):
        self.setTitle('지역 정보 설정')
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
        self.topLeftVariable.setReadOnly(True)
        self.bottomRightVariable.setReadOnly(True)
        self.notifyRegionChanged(self.region.top_left, self.region.bottom_right)

    def notifyRegionChanged(self, topLeft, bottomRight):
        self.topLeftVariable.setText(str(topLeft))
        self.bottomRightVariable.setText(str(bottomRight))
    
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
        from dto import Region
        self.region = Region((0, 0), (0, 0))

class VaccineConfig(QWidget):

    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent
        if model is not None:
            self.default_vaccines = model.default_vaccines
        else:
            self.mock()

        self.setup()

    def setup(self):
        pass

    def mock(self):
        self.default_vaccines = ['ANY']

class MacroConfig(QWidget):
    
    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent
        if model is not None:
            self.macroInterval = str(model.run_interval)
        else:
            self.mock()
        self.macroIntervalLabel = QLabel()
        self.macroIntervalVariable = QLineEdit()
        self.startButton = QPushButton()
        self.stopButton = QPushButton()
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
        self.addChild(self.stopButton)

    def setupLabel(self):
        self.macroIntervalLabel.setText('매크로 수행 주기(초) ')
    
    def setupVariable(self):
        self.macroIntervalVariable.setText(self.macroInterval)
        self.macroIntervalVariable.setToolTip('초 단위')

    def setupButton(self):
        self.startButton.setText('시작')
        self.startButton.setEnabled(False)
        self.stopButton.setText('정지')
        self.stopButton.setEnabled(False)

    def mock(self):
        self.macroInterval = str(7)

class MacroLogs(QWidget):

    def __init__(self, parent=None, model=None):
        super().__init__()
        self.parent = parent

        self.appendLogSignal = MacroLogs.AppendLogSignal()
        self.macroLogsLabel = QLabel()
        self.macroLogsTextEdit = QTextEdit()
        self.setup()

    def setup(self):
        self.appendLogSignal.signal.connect(self._appendLog)
        self.useLayout(QVBoxLayout())
        self.setChildren()
        self.setupLabel()
        self.setupTextEdit()

    def setChildren(self):
        self.addChild(self.macroLogsLabel)
        self.addChild(self.macroLogsTextEdit)
    
    def setupLabel(self):
        self.macroLogsLabel.setText('매크로 수행 로그')

    def setupTextEdit(self):
        self.macroLogsTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def log(self, text):
        self.appendLogSignal.run(text)

    @pyqtSlot(str)
    def _appendLog(self, text):
        self.macroLogsTextEdit.append(text)

    class AppendLogSignal(QObject):

        signal = pyqtSignal(str)

        def run(self, text):
            self.signal.emit(text)