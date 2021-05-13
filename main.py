import cv2 as cv
from tkinter import filedialog
import tkinter as tk
class UI:
    window = None


    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select image")
        self.window.geometry("200x200")
        self.initUi()
        self.window.mainloop()


    def initUi(self):
        greeting = tk.Label(text="Recognize streets")
        button = tk.Button(self.window, text="Open file chooser", command=self.openImage)
        greeting.pack()
        button.pack()

    def openImage(self):
        filename = filedialog.askopenfilename()
        img = cv.imread(filename)

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





