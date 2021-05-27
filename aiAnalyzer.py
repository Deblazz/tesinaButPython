import cv2 as cv
from tkinter import filedialog
import os

def analyze():
    filename = filedialog.askopenfilename()
    img = cv.imread(filename)

    filename = filedialog.askopenfilename(filetypes = [("Cascade files","*.xml")])
    cascade = cv.CascadeClassifier(filename)
    name = os.path.splitext(os.path.basename(filename))[0]

    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgDetection = cascade.detectMultiScale(grayScaleImg, 30, 30)
    for (x, y, w, h) in imgDetection:
        cv.putText(img, name, (x-w, y-h), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.imshow('img',img)
    cv.waitKey()




