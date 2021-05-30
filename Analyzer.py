import cv2 as cv
import os

def analyze(imgPath, cascadePath):
    img = cv.imread(imgPath)

    cascade = cv.CascadeClassifier(cascadePath)
    name = os.path.splitext(os.path.basename(cascadePath))[0]
    ext = os.path.splitext(os.path.basename(cascadePath))[1]

    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgDetection = cascade.detectMultiScale(grayScaleImg, 30, 30)
    if(len(imgDetection) > 0):
        for (x, y, w, h) in imgDetection:
            cv.putText(img, name, (x - w, y - h), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
        cv.imwrite(f"./output/{os.path.splitext(os.path.basename(imgPath))[0]}-analyzed{os.path.splitext(os.path.basename(imgPath))[1]}",img)
        return imgDetection
