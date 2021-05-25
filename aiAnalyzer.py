import cv2 as cv
from tkinter import filedialog

def analyze():
    filename = filedialog.askopenfilename()
    img = cv.imread(filename)

    filename = filedialog.askopenfilename(filetypes = [("Cascade files","*.xml")])
    cascade = cv.CascadeClassifier(filename)

    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgDetection = cascade.detectMultiScale(grayScaleImg, 50, 100)
    for (x, y, w, h) in imgDetection:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    print(img)
    cv.imshow('img',img)
    cv.waitKey()











    # if img is None:
    #     print("Hai inserito un'immagine non valida")
    #     exit(-1)
    #
    # cv.namedWindow(f"Analyzed", cv.WINDOW_NORMAL)
    #cv.resizeWindow("Image", 600, 600)
    #cv.imshow("Image", img)
    #
    # while True:
    #     k = cv.waitKey(100)
    #
    #     if cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
    #         break
    #     # 27 is the ascii code for escape
    #     elif k == 27:
    #         break
    #cv.destroyAllWindows()
