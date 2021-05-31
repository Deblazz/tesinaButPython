import math
import _thread
import cv2
import mxnet
import numpy
import shutil
import os
import pickle
import psutil
from PyQt5.QtWidgets import QProgressDialog, QDialog, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from trainerSettingsDialog import Ui_Dialog

# def saveNegatives():
#     messagebox.showinfo("Info", "Select your negative samples, you'll need at least 500 of them to get a good result")
#     filePaths = filedialog.askopenfilenames(title="Select your files", filetypes=[('image files', '.jpg')])
#     emptyFolder()
#     bgFile = open("./training/bg.txt", "w")
#
#     for index, file in enumerate(filePaths):
#         shutil.copyfile(file, f"./training/negativesTraining/img{index}.jpg")
#         print(f"negativesTraining/img{index}.jpg", file=bgFile)
#
#     bgFile.close()
#
# def savePositives():
#     answer = messagebox.askyesno("Positive samples", "Have you already got a positive samples collection?")
#
#     if answer:
#         infoFilePath = filedialog.askopenfilename(title="Select your .info file", filetypes=[('info files', '.info')])
#         filePaths = filedialog.askopenfilenames(title="Select your files", filetypes=[('image files', '.jpg')])
#             #TODO Check if info file and pictures are coherent
#         for index, file in enumerate(filePaths):
#             shutil.copyfile(file, f"./training/positivesTraining/img{index}.jpg")
#
#
#     else:x
#         print("Devi pagare le tasse")
#
#

def startManualTraining(negFilePaths, posFilePaths, posName):
    emptyFolder("./training/negatives")
    emptyFolder("./training/positives")
    tasks = len(negFilePaths) + 1

    bg = open("./training/bg.txt", "w")
    info = open("./training/info.dat", "w")

    for index, negImg in enumerate(negFilePaths):
        shutil.copyfile(negImg, f"./training/negatives/img{index}{os.path.splitext(os.path.basename(negImg))[1]}")
        bg.write(f"./negatives/img{index}{os.path.splitext(os.path.basename(negImg))[1]}\n")
    bg.close()

    for index, posImg in enumerate(posFilePaths):
        shutil.copyfile(posImg, f"./training/positives/img{index}{os.path.splitext(os.path.basename(posImg))[1]}")
        img = cv2.imread(posImg)
        info.write(f"./positives/img{index}{os.path.splitext(os.path.basename(posImg))[1]}  1  0 0 {img.shape[0]} {img.shape[1]}\n")
    info.close()

    trainMultiplePos(posName[0], len(posFilePaths))




def startCifar10Training(filePaths, catToTrain):
    nPos = 0
    nNeg = 0
    imagesCount = 0

    emptyFolder("./training/negatives")
    emptyFolder("./training/positives")
    tasks = len(filePaths)*10000
    progress = QProgressDialog("Progress is being made...", "Cancel", 0, tasks, None)
    progress.setWindowTitle("pyDetect")
    progress.setWindowModality(Qt.WindowModal)
    bg = open("./training/bg.txt", "w")
    info = open("./training/info.dat", "w")

    for filePath in filePaths:
        currentBatchImages = 0
        with open(filePath, 'rb') as file:
            dsContent = pickle.load(file, encoding='bytes')
        imgs = dsContent[b'data']
        imgs = numpy.reshape(imgs, (10000, 3, 32, 32))
        lbls = dsContent[b'labels']
        imgArr = mxnet.nd.array(imgs)
        lblArr = mxnet.nd.array(lbls)



        for img in imgArr:
            if(progress.wasCanceled()):
                return

            if (lblArr[currentBatchImages] == catToTrain[0]):
                path = f"./training/positives/img{imagesCount}.jpg"
                saveCifar10Image(img, path)
                info.write(f"./positives/img{imagesCount}.jpg  1  0 0 32 32\n")
                nPos+=1

            else:
                path = f"./training/negatives/img{imagesCount}.jpg"
                saveCifar10Image(img, path)
                bg.write(f"./negatives/img{imagesCount}.jpg\n")
                nNeg+=1
            currentBatchImages += 1
            imagesCount += 1
            progress.setValue(imagesCount)
    info.close()
    bg.close()
    print(f"OFRAT {catToTrain}")
    trainMultiplePos(catToTrain, nPos)

def saveCifar10Image(img, path):
    img = img.asnumpy().transpose(1, 2, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(path, img)

def trainMultiplePos(answer, numPos):
    emptyFolder("./training/data")
    files = os.listdir("./training/positives/")
    img = cv2.imread(f"./training/positives/{files[0]}")
    print(f"$> opencv_createsamples -w {img.shape[0]} -h {img.shape[1]} -vec ./training/positives.vec -info ./training/info.dat -num {numPos}")
    _thread.start_new_thread(os.system, (f"opencv_createsamples -w {img.shape[0]} -h {img.shape[1]} -vec ./training/positives.vec -info ./training/info.dat -num {numPos}",))

    dialog = trainerSettingsDialog(None, numPos, img.shape[0], img.shape[1], answer)
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.setWindowTitle("Trainer properties")
    dialog.setFixedSize(650, 300)
    dialog.exec_()




def emptyFolder(path):
    #Note: You can choose two approaches here. You can either delete the folder as a whole or cycle through files, deleting each single one. For this example we used the first case scenario
    shutil.rmtree(path)
    os.mkdir(path)


def trainCascade(alg, nStages, minHitRate, numSamples, w, h, answer):
    systemRam = psutil.virtual_memory()
    os.system(f"touch ./training/data/cascade.xml; cd training; opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos {numSamples - 100} -numNeg {math.floor((numSamples - 100) / 2)} -numStages {nStages} -w {w} -h {h} -featureType {alg} -minHitRate {minHitRate/100} -precalcValBufSize {math.floor(systemRam.available / 4000000)} -precalcIdxBufSize {math.floor(systemRam.available / 4000000)}; cd data; mv cascade.xml {answer[1]}.xml")
    dialog = QMessageBox.information(None, "Good news!", f"Training finished, you'll find your trained cascade at:\n /PhYnder/training/data/{answer[1]}.xml", QMessageBox.Ok)

    # We use half of the available system RAM to run the trainer

class trainerSettingsDialog(QDialog):
    def __init__(self, parent=None, nPositives=None, w = None, h = None, answer = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self, nPositives, w, h, answer)