import matplotlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from resultWindow import ResultWindow
from MplCanvas import MplCanvas
from clusterWindow import ClusteringWindow
from textProcessingWindow import TextProcessingWindow
from vectorizingWindow import VectorizationWindow
matplotlib.use('Qt5Agg')


class WorkspaceTab(QWidget):
    def __init__(self, workspace):
        super().__init__()
        self.workspace = workspace
        self.result_windows = []
        self.current_graph_index = 0
        self.canvas = MplCanvas(self)
        self.plot_axes = self.canvas.axes
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.canvas)
        self.plot1_button = QPushButton("Prev")
        self.plot2_button = QPushButton("Next")
        layout.addWidget(self.plot1_button)
        layout.addWidget(self.plot2_button)
        self.plot1_button.clicked.connect(self.switch_graph)
        self.plot2_button.clicked.connect(self.switch_graph)
        self.switch_graph()

        apply_button = QPushButton("Apply Changes")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        text_button = QPushButton("Text")
        text_button.clicked.connect(self.text_button_clicked)
        vector_button  = QPushButton("Vector")
        vector_button.clicked.connect(self.vector_button_clicked)
        cluster_button  = QPushButton("Cluster")
        cluster_button.clicked.connect(self.cluster_button_clicked)

        layout.addWidget(text_button)
        layout.addWidget(vector_button)
        layout.addWidget(cluster_button)

        self.setLayout(layout)

    def text_button_clicked(self):
        dialog = TextProcessingWindow(self.workspace)
        dialog.exec()
        self.update_graph()


    def vector_button_clicked(self):
        dialog = VectorizationWindow(self.workspace)
        dialog.exec()
        self.update_graph()

    def cluster_button_clicked(self):
        dialog = ClusteringWindow(self.workspace)
        dialog.exec()
        self.update_graph()


    # def create_param_input(self, param_name):
    #     widget = QWidget()
    #     layout = QHBoxLayout()
    #     widget.setLayout(layout)
    #     label = QLabel(param_name)
    #     input_field = QLineEdit()
    #     layout.addWidget(label)
    #     layout.addWidget(input_field)
    #     input_field.setText(str(self.workspace.parameters[param_name]))
    #     input_field.textChanged.connect(lambda text, key=param_name: self.update_workspace_param(key, text))
    #     return widget

    def update_workspace_param(self, key, text):
        try:
            value = int(text)
            self.workspace.set_parameter(key, value)
        except ValueError:
            print("Error value:", text)
            pass

    def switch_graph(self):
        sender_button = self.sender()
        if sender_button == self.plot1_button:
            self.current_graph_index = (self.current_graph_index - 1) % 3
        elif sender_button == self.plot2_button:
            self.current_graph_index = (self.current_graph_index + 1) % 3
        if self.current_graph_index == 0:
            self.plot_text_freq()
        elif self.current_graph_index == 1:
            self.plot_text_length()
        elif self.current_graph_index == 2:
            self.plot_k_nears()

    def update_graph(self):
        if self.current_graph_index == 0:
            self.plot_text_freq()
        elif self.current_graph_index == 1:
            self.plot_text_length()
        elif self.current_graph_index == 2:
            self.plot_k_nears()

    def plot_text_freq(self):
        try:
            x = self.workspace.words_sorted
            y = self.workspace.counts_sorted
            self.plot_axes.clear()
            self.plot_axes.bar(x[:20], y[:20])
            self.plot_axes.tick_params(axis='x', rotation=45)
            self.canvas.draw()
        except Exception as e:
          print("Error during plot_text_freq:", e)

    def plot_text_length(self):
        try:
            # hardcode
            # max_size = self.workspace.max_size
            max_size = 100
            length = self.workspace.lengths
            self.plot_axes.clear()
            self.plot_axes.hist(range(max_size), bins=max_size, weights=length[:max_size], edgecolor='black')
            self.canvas.draw()
        except Exception as e:
          print("Error during plot_text_length:", e)

    def plot_k_nears(self):
        try:
            distances = self.workspace.k_dist
            self.plot_axes.clear()
            self.plot_axes.plot(distances)
            self.plot_axes.grid(True, linestyle="--", color='black', alpha=0.4)
            self.canvas.draw()
        except Exception as e:
          print("Error during plot_text_length:", e)

    def apply_changes(self):
        self.workspace.apply()
        try:
            result_window = ResultWindow(self.workspace)
            self.result_windows.append(result_window)
            result_window.show()
        except Exception as e:
            print("Error during making Result:", e)

