from tkinter import Label, BOTH, X
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot.plot_canvas import PlotCanvas
from model.points_model import PointsModel

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator otoczki wypukłej")

        self.model = PointsModel()
        self.plot = PlotCanvas(self.model)

        self.canvas_widget = FigureCanvasTkAgg(self.plot.figure, master=self.root)
        self.canvas_widget.get_tk_widget().pack(fill=BOTH, expand=True)
        self.canvas_widget.mpl_connect("button_press_event", self.on_click)

        self.points_label = Label(self.root, text="Wprowadzone punkty: []", anchor="w", justify="left")
        self.points_label.pack(fill=X, padx=10, pady=5)

    def on_click(self, event):
        if event.inaxes != self.plot.ax:
            return

        self.model.add_point(event.xdata, event.ydata)
        self.plot.draw_points()
        self.update_point_list()

    def update_point_list(self):
        text = "Wprowadzone punkty:\n" + "\n".join([f"({x}, {y})" for x, y in self.model.get_points()])
        self.points_label.config(text=text)
