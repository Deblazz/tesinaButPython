import tkinter
import cv2
import mxnet
import numpy
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import shutil
import os
import pickle
import subprocess

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
    for filePath in filePaths:
        imagesCount = 0
        with open(filePath, 'rb') as file:
            dsContent = pickle.load(file, encoding='bytes')
        imgs = dsContent[b'data']
        imgs = numpy.reshape(imgs, (10000, 3, 32, 32))
        lbls = dsContent[b'labels']
        imgArr = mxnet.nd.array(imgs)
        lblArr = mxnet.nd.array(lbls)
        answer = askCatToTrain(categories['label_names'])

        bg = open("./training/cifar10/bg.txt", "w")
        info = open("./training/cifar10/info.dat", "w")
        filterVal = categories['label_names'].index(answer)
        nPos = 0
        nNeg = 0
        emptyFolder("./training/cifar10/negatives")
        emptyFolder("./training/cifar10/positives")

        for img in imgArr:
            # @TODO Implement loading bar
            print(imagesCount)
            if (lblArr[imagesCount] == filterVal):
                path = f"./training/cifar10/positives/img{imagesCount}.jpg"
                saveCifar10Image(img, path)
                path = os.path.abspath(f"./training/cifar10/positives/img{imagesCount}.jpg")
                info.write(f"{path}  1  0 0 32 32\n")
                nPos+=1

            else:
                path = f"./training/cifar10/negatives/img{imagesCount}.jpg"
                saveCifar10Image(img, path)
                path = os.path.abspath(f"./negatives/img{imagesCount}.jpg")
                bg.write(f"{path}\n")
                nNeg+=1
            imagesCount += 1
        bg.close()
        startCifar10Training(nPos, nNeg)






def askCatToTrain(categories):
    top = Toplevel()
    top.geometry("500x100")
    top.title("Select your descriptor")
    label = Label(top, text="Choose which item you'll want to recognize")
    label.pack()

    answer = tkinter.StringVar(top)
    answer.set(categories[0])

    drop = OptionMenu(top, answer, *categories)
    drop.pack()

    returnVal = Label(top)
    returnVal.pack()

    def callback():
        top.quit()
        returnVal["text"] = answer.get()

    button = Button(top, text = "Select", command=callback)
    button.pack()
    top.mainloop()
    while returnVal["text"] == "":
        pass

    return returnVal["text"]


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


def startCifar10Training(nPos, nNeg):
    print(f"{nPos}, {nNeg}")

    os.chdir("./training/cifar10")
    os.system("ls")

    command = f"opencv_createsamples -info \"info.dat\" -vec \"positives.vec\" -w 32 -h 32 -num {nPos}"
    os.system(command)

    command = f"opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos {nPos*0.8} -numNeg {nNeg} -numStages 10 -w 32 -h 32 -featureType LBP"
    os.system(command)


def emptyFolder(path):
    #Note: You can choose two approaches here. You can either delete the folder as a whole or cycle through files, deleting each single one. For this example we used the first case scenario
    shutil.rmtree(path)
    os.mkdir(path)