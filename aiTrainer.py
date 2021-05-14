import os
from tkinter import messagebox
from tkinter import filedialog
import shutil
import os
import downloader
def train():
    answer = messagebox.askokcancel("Warning", "Training the AI is a time-consuming process, are you ready?")

    if answer == True:
        saveNegatives()
        savePositives()
        #downloader.download()

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