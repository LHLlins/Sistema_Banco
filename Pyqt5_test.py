from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle("First Work")
        self.initUI()



    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my first label")
        self.label.move(50, 50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('OK')
        self.b1.clicked.connect(self.show_popup)

    def clicked(self):
        self.label.setText("you pressed this button")
        self.update()

    def update(self) -> None:
        self.label.adjustSize()

    def show_popup(self):
        msm = QMessageBox()
        msm.setWindowTitle("First Message Box")
        msm.setText('Candela')
        msm.setIcon(QMessageBox.Critical)
        msm.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Apply)
        msm.setDefaultButton(QMessageBox.Cancel)
        msm.setInformativeText("Hello!!!!!!!")
        msm.setDetailedText("Very good!!!!")

        msm.buttonClicked.connect(self.poppup)

        msm.exec_()

    def poppup(self, i):
        print(i.text())




def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()