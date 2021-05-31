import pickle

import cv2
from PyQt5.QtWidgets import QWidget, QFileDialog, QDialog, QLabel, QMessageBox, QPushButton, QComboBox, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Trainer

class TrainerUI(QWidget):

    def __init__(self):
        super().__init__()
        self.selectedCat = None
        self.onClick()

    def onClick(self):
        buttonReply = QMessageBox.question(None, 'Info', "Training the AI is a time-consuming process, are you ready?",QMessageBox.Yes | QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            dialog = QDialog()
            dialog.setFixedSize(400, 100)
            dialog.setWindowTitle("Trainer settings")
            dialog.setWindowModality(Qt.ApplicationModal)

            lbl = QLabel("Would you like to use a Cifar-10 compatible dataset or create one from scratch?", dialog)
            lbl.setWordWrap(True)
            btnCifar = QPushButton("Cifar-10", dialog)
            btnManual = QPushButton("Manual", dialog)
            btnCifar.move(310, 60)
            btnManual.move(220, 60)

            btnCifar.clicked.connect(dialog.accept)
            btnCifar.clicked.connect(self.trainCifar)

            btnManual.clicked.connect(dialog.accept)
            btnManual.clicked.connect(self.trainManual)
            dialog.exec_()



        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # #using system proprietary filedialog
        # fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        # if fileName:
        #     print(fileName)

    def trainCifar(self):
        categories = None

        while(categories is None):
            categories = self.getCifar10Cat()
            if(categories is None):
                error = QMessageBox()
                error.critical(None, "Error", "You didn't select a .meta file!", QMessageBox.Ok)

        filePaths = []
        while(len(filePaths) <= 0):
            filePaths = self.getCifar10Batches()
            if(len(filePaths) <= 0):
                error = QMessageBox()
                error.critical(None, "Error", "You didn't select a batch!", QMessageBox.Ok)

        catToTrain = None
        while(catToTrain is None):
            catToTrain = self.askCatToTrain(categories['label_names'])
            if(catToTrain is None):
                error = QMessageBox()
                error.critical(None, "Error", "You didn't select a category!", QMessageBox.Ok)
        Trainer.startCifar10Training(filePaths, catToTrain)



    def getCifar10Cat(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #using system proprietary filedialog
        categoriesPath, _ = QFileDialog.getOpenFileName(None,"Select your batches.meta file", "","Cifar10 meta files(*.meta)", options=options)
        if categoriesPath:
            with open(categoriesPath, 'rb') as file:
                cat = pickle.load(file)
                return cat


    def getCifar10Batches(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # using system proprietary filedialog
        batchesPaths, _ = QFileDialog.getOpenFileNames(None, "Select the corresponding dataset(s)", "","Cifar10 batches files(*)", options=options)
        return batchesPaths

    def askCatToTrain(self, categories):

        dialog = QDialog()
        dialog.setWindowTitle("Select your descriptor")
        dialog.setFixedSize(400, 150)

        label = QLabel("Choose which item you'll want to recognize", dialog)

        combobox = QComboBox(dialog)
        combobox.addItems(categories)
        combobox.move(100, 50)

        okButton = QPushButton("Ok", dialog)
        okButton.move(310, 70)
        okButton.clicked.connect(dialog.accept)
        okButton.clicked.connect(lambda: self.getCat(combobox.currentIndex()))

        dialog.exec_()
        return [self.selectedCat, categories[self.selectedCat]]

    def getCat(self, currentCat):
        self.selectedCat = currentCat

    def trainManual(self):
        negativePaths = []
        while(len(negativePaths) < 2):
            negativePaths = self.getManualNegatives()
            if (len(negativePaths) < 2):
                error = QMessageBox()
                error.critical(None, "Error", "You selected too few negatives!", QMessageBox.Ok)

        answer = False
        positivePaths = []
        while(len(positivePaths) < 2):
            while(answer is False):
                positivePaths = self.getManualPositives()
                if(len(positivePaths) >= 2):
                    if(self.checkCoherentSizes(positivePaths) is True):
                        answer = True
                    else:
                        error = QMessageBox()
                        error.critical(None, "Error", "The images you selected have different sizes", QMessageBox.Ok)
                else:
                    error = QMessageBox()
                    error.critical(None, "Error", "You selected too few positives!", QMessageBox.Ok)

        positiveName = ['']
        while(len(positiveName[0]) == 0):
            positiveName = self.getPositiveName()
            if(len(positiveName[0]) == 0):
                error = QMessageBox()
                error.critical(None, "Error", "Name cannot be left empty!")
        Trainer.startManualTraining(negativePaths, positivePaths, positiveName)



    def getManualNegatives(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # using system proprietary filedialog
        negativesPaths, _ = QFileDialog.getOpenFileNames(None, "Select negative samples", "", "Compressed images(*.jpg *.jpeg);;Uncompressed images(*.png)", options=options)
        return negativesPaths

    def getManualPositives(self):
        QMessageBox.information(None, "Info","Insert tiny positives, images should only contain the object")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        positivePath, _ = QFileDialog.getOpenFileNames(None, "Select positive samples", "", "Compressed images(*.jpg *.jpeg);;Uncompressed images(*.png)", options=options)
        return positivePath

    def getPositiveName(self):
        text = QInputDialog.getText(None, "Insert name", "Insert name of the positive descriptor")
        return text

    def checkCoherentSizes(self, imgs):
        index = 0
        vSizes = []
        for img in imgs:
            if(index != 0):
                oImg = cv2.imread(img)
                vSizes.append(oImg.shape)
                if (vSizes[index] != vSizes[index-1]):
                    return False
            else:
                oImg = cv2.imread(img)
                vSizes.append(oImg.shape)
            index += 1

        return True
