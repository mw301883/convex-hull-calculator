from tkinter import Tk
from ui.main_window import MainWindow

if __name__ == "__main__":
    root = Tk(className="Kalkulator otoczki wypuklej")
    app = MainWindow(root)
    root.mainloop()
