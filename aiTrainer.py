import os

import cv2
import mxnet
import numpy
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
import shutil
import os
import pickle
import UI
def train():
    answer = messagebox.askokcancel("Warning", "Training the AI is a time-consuming process, are you ready?")

    if answer == True:
        answer = messagebox.askyesno("", "Do you want to access a CIFAR-10 compatible dataset?")
        if answer == True:
            openCifar10()
        else:
            saveNegatives()
            savePositives()

def getCifar10Cat():
    categoriesPath = filedialog.askopenfilename(title="Select your batches.meta file", initialdir="/media/deblazz/CEBAE294BAE2787")
    with open(categoriesPath, 'rb') as file:
        cat = pickle.load(file)
    return cat

def saveCifar10Image(img, path):
    img = img.asnumpy().transpose(1, 2, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img)


def openCifar10():
    categories = getCifar10Cat()
    filePaths = filedialog.askopenfilenames(title="Select the corresponding dataset(s)", initialdir="/media/deblazz/CEBAE294BAE2787")
    imagesCount = 0
    for filePath in filePaths:
        with open(filePath, 'rb') as file:
            dsContent = pickle.load(file, encoding='bytes')
        imgs = dsContent[b'data']
        imgs = numpy.reshape(imgs, (10000, 3, 32, 32))
        lbls = dsContent[b'labels']
        imgArr = mxnet.nd.array(imgs)
        lblArr = mxnet.nd.array(lbls)

        answer = UI.askCatToTrain(categories['label_names'])



        #for img in imgArr:
         #   path = f"./training/cifar10/img{imagesCount}.jpg"
          #  saveCifar10Image(img, path)
           # imagesCount+=1











def saveNegatives():
    messagebox.showinfo("Info", "Select your negative samples, you'll need at least 500 of them to get a good result")
    filePaths = filedialog.askopenfilenames(title="Select your files", filetypes=[('image files', '.jpg')])
    emptyFolder()
    bgFile = open("./training/bg.txt", "w")

    for index, file in enumerate(filePaths):
        shutil.copyfile(file, f"./training/negativesTraining/img{index}.jpg")
        print(f"negativesTraining/img{index}.jpg", file=bgFile)

    bgFile.close()

def savePositives():
    answer = messagebox.askyesno("Positive samples", "Have you already got a positive samples collection?")

    if answer:
        infoFilePath = filedialog.askopenfilename(title="Select your .info file", filetypes=[('info files', '.info')])
        filePaths = filedialog.askopenfilenames(title="Select your files", filetypes=[('image files', '.jpg')])
            #TODO Check if info file and pictures are coherent
        for index, file in enumerate(filePaths):
            shutil.copyfile(file, f"./training/positivesTraining/img{index}.jpg")


    else:
        print("Devi pagare le tasse")





def emptyFolder():
    #Note: You can choose two approaches here. You can either delete the folder as a whole or cycle through files, deleting each single one. For this example we used the first case scenario
    shutil.rmtree("./training/negativesTraining")
    os.mkdir("./training/negativesTraining")