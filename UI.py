import tkinter as tk
import aiTrainer
import aiAnalyzer
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
        buttonAnalyzer = tk.Button(self.window, text="Analyze picture", command=aiAnalyzer.analyze)
        buttonTrainer = tk.Button(self.window, text="Train the AI", command=aiTrainer.train)
        title.pack()
        buttonAnalyzer.pack()
        buttonTrainer.pack()

def main():
        newUi = UI()


if __name__ == '__main__':
    main()





