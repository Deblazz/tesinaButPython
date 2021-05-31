from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QMessageBox, QFileDialog, QDialogButtonBox, QVBoxLayout, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Analyzer
import os

class AnalyzerUI(QWidget):

    def __init__(self):
        super().__init__()
        self.imageName = None
        self.onClick()

    def onClick(self):
        # using system proprietary filedialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgName, _ = QFileDialog.getOpenFileName(self,"Select image to scan", "","Compressed images (*.jpg *.jpeg);;Uncompressed images (*.png)", options=options)
        self.imageName = imgName
        if imgName:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            cascadeName, _ = QFileDialog.getOpenFileName(self, "Select trained cascade file", "", "Cascade file(*.xml)", options=options)
            if cascadeName:
                rsNumber = Analyzer.analyze(imgName, cascadeName)
                print(rsNumber)
                if(len(rsNumber) > 0):

                   dialog = QDialog()
                   label = QLabel(f"Your object has been found {len(rsNumber)} times. Do you want to open the output picture?", dialog)
                   #Go to next line if needed
                   label.setWordWrap(True)
                   yesBtn = QPushButton("Yes", dialog)

                   #Closing current dialog then opening a new one
                   yesBtn.clicked.connect(dialog.accept)
                   yesBtn.clicked.connect(self.showImage)

                   noBtn = QPushButton("No", dialog)
                   noBtn.clicked.connect(dialog.accept)
                   yesBtn.move(310, 60)
                   noBtn.move(220, 60)
                   dialog.setFixedSize(400, 100)
                   dialog.setWindowTitle("Output")
                   dialog.setWindowModality(Qt.ApplicationModal)
                   dialog.exec_()

                else:
                    QMessageBox.about(self, "Output", f"No {os.path.splitext(os.path.basename(cascadeName))[0]} has been detected")


    def showImage(self):
        dialog = QDialog()
        label = QLabel(dialog)
        img = QPixmap(f'./output/{getEditedImageName(self.imageName)}')
        label.setPixmap(img)
        dialog.setWindowTitle(f"pyDetector - {getEditedImageName(self.imageName)}")
        dialog.setFixedSize(img.width(), img.height())
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

def getEditedImageName(imgName):
    return(os.path.splitext(os.path.basename(imgName))[0] + "-analyzed" + os.path.splitext(os.path.basename(imgName))[1])