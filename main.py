from PyQt5 import QtCore, QtWidgets
import main
from AnalyzerUI import AnalyzerUI
from TrainerUI import TrainerUI



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 400)
        MainWindow.setStyleSheet("background-color: rgb(57, 62, 65);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(130, 70, 341, 31))
        self.titleLabel.setStyleSheet("font: 20pt \"Neon\";\n""color: rgb(255, 166, 48);")
        self.titleLabel.setObjectName("titleLabel")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(381, 220, 89, 25))
        self.trainButton.setStyleSheet("color: rgb(215, 232, 186);")
        self.trainButton.setObjectName("trainButton")
        self.analyzeButton = QtWidgets.QPushButton(self.centralwidget)
        self.analyzeButton.setGeometry(QtCore.QRect(130, 220, 89, 25))
        self.analyzeButton.setStyleSheet("color: rgb(215, 232, 186);")
        self.analyzeButton.setObjectName("analyzeButton")
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setGeometry(QtCore.QRect(460, 350, 121, 17))
        self.versionLabel.setStyleSheet("color: rgb(215, 232, 186);")
        self.versionLabel.setObjectName("versionLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.analyzeButton.clicked.connect(main.analyze)
        self.trainButton.clicked.connect(main.train)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "pyDetectx"))
        self.titleLabel.setText(_translate("MainWindow", "pyDetect"))
        self.trainButton.setText(_translate("MainWindow", "Train"))
        self.analyzeButton.setText(_translate("MainWindow", "Analyze"))
        self.versionLabel.setText(_translate("MainWindow", "v0.9 pre-Release"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def train():
    trainer = TrainerUI()

def analyze():
    analyzer = AnalyzerUI()