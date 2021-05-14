import cv2 as cv
from tkinter import filedialog
import tkinter as tk
import aiTrainer
class UI:
    window = None


    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select image")
        self.window.geometry("200x200")
        self.initUi()
        self.window.mainloop()


    def initUi(self):
        title = tk.Label(text="Recognize streets")
        buttonAnalyzer = tk.Button(self.window, text="Analyze picture", command=self.openImage)
        buttonTrainer = tk.Button(self.window, text="Train the AI", command=aiTrainer.train)
        title.pack()
        buttonAnalyzer.pack()
        buttonTrainer.pack()

    def openImage(self):
        filename = filedialog.askopenfilename()
        img = cv.imread(filename)
        img_bw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


        if img is None:
            print("Hai inserito un'immagine non valida")
            exit(-1)

        cv.namedWindow("Image", cv.WINDOW_NORMAL)
        cv.resizeWindow("Image", 600, 600)
        cv.imshow("Image", img)

        while True:
            k = cv.waitKey(100)

            if cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
                break
            # 27 is the ascii code for escape
            elif k == 27:
                break
        cv.destroyAllWindows()

def main():
        newUi = UI()


if __name__ == '__main__':
    main()





