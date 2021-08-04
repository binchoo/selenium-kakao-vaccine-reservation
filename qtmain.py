from PyQt5.QtWidgets import QApplication
from view.main import MainView

app = QApplication([])
app.setStyle('Fusion')
app.setApplicationName('COVID-19 Vaccine Auto Reservation')

view = MainView()

app.exec()