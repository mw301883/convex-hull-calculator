from tkinter import Label, Button, Frame, Canvas, Scrollbar, BOTH, X, LEFT, RIGHT, Y, VERTICAL
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot.plot_canvas import PlotCanvas
from model.points_model import PointsModel

class MainWindow:
    MAX_POINTS = 30

    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator otoczki wypukłej")

        self.model = PointsModel()
        self.plot = PlotCanvas(self.model)

        self.canvas_widget = FigureCanvasTkAgg(self.plot.figure, master=self.root)
        self.canvas_widget.get_tk_widget().pack(fill=BOTH, expand=True)
        self.canvas_widget.mpl_connect("button_press_event", self.on_click)

        container = Frame(self.root)
        container.pack(fill=X, padx=10, pady=5)

        self.canvas_points = Canvas(container, height=150)
        self.canvas_points.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(container, orient=VERTICAL, command=self.canvas_points.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas_points.configure(yscrollcommand=scrollbar.set)

        self.points_frame = Frame(self.canvas_points)
        self.canvas_points.create_window((0, 0), window=self.points_frame, anchor="nw")

        self.points_frame.bind("<Configure>", lambda e: self.canvas_points.configure(scrollregion=self.canvas_points.bbox("all")))

        self.update_point_list()

    def on_click(self, event):
        if event.inaxes != self.plot.ax:
            return

        if len(self.model.get_points()) >= self.MAX_POINTS:
            messagebox.showwarning("Limit punktów", f"Można dodać maksymalnie {self.MAX_POINTS} punktów.")
            return

        self.model.add_point(event.xdata, event.ydata)
        self.plot.draw_points()
        self.update_point_list()

    def update_point_list(self):
        for widget in self.points_frame.winfo_children():
            widget.destroy()

        points = self.model.get_points()
        if not points:
            Label(self.points_frame, text="Brak punktów").pack(anchor="w")
            return

        for idx, (x, y) in enumerate(points):
            point_str = f"({x:.2f}, {y:.2f})"
            point_row = Frame(self.points_frame)
            point_row.pack(fill=X, anchor="w", pady=1)

            Label(point_row, text=point_str, width=20, anchor="w").pack(side=LEFT)

            btn = Button(point_row, text="Delete", command=lambda i=idx: self.delete_point(i))
            btn.pack(side=RIGHT)

    def delete_point(self, index):
        self.model.remove_point(index)
        self.plot.draw_points()
        self.update_point_list()
