import random

import mplcursors
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from MplCanvas import MplCanvas
from sklearn.manifold import TSNE
import numpy as np
import time




class ResultWindow(QMainWindow):
    def __init__(self, workspace):
        super().__init__()
        self.workspace = workspace
        self.canvas = MplCanvas(self)
        self.plot_axes = self.canvas.axes
        self.init_ui()
        self.show_graphic()


    def init_ui(self):
        self.setWindowTitle("Result " + str(self.workspace.name) + " - " + str(random.randint(10000, 100000)))
        self.setGeometry(200, 200, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(toolbar)
        central_widget.setLayout(layout)

    def show_graphic(self):
        try:
            startTime = time.time()
            plot_points_size = len(self.workspace.vectorization_text)
            combined_points = np.concatenate((self.workspace.vectorization_text, self.workspace.clustering_centrs),axis=0)
            plot_points = self.vtsne(combined_points)
            plot_points_data = plot_points[:plot_points_size]
            clustr_centr_data = plot_points[plot_points_size:]
            points_colors = self.workspace.clustering_text
            points_text = self.workspace.nlp_data
            centrs_text = self.workspace.clustering_centrs_name


            x = plot_points_data[:, 0]
            y = plot_points_data[:, 1]

            centr_x = clustr_centr_data[:, 0]
            centr_y = clustr_centr_data[:, 1]

            self.plot_axes.clear()
            scatter = self.plot_axes.scatter(x, y, c=points_colors, cmap="jet")
            plot = self.plot_axes.plot(centr_x, centr_y, 'x', c="red", markersize=10)

            cursor = mplcursors.cursor(scatter, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text(f"Data:{points_text[sel.index]}"))
            cursor = mplcursors.cursor(plot, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text(f"Centr Data:{centrs_text[sel.index]}"))

            self.canvas.draw()
            endTime = time.time()
            print("Show complete by time: ", endTime - startTime)
        except Exception as e:
            print("Error in show_graphic:", e)

    def vtsne(self, points, demen=2):
        tsne = TSNE(n_components=demen)
        return tsne.fit_transform(points)
