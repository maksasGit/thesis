
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QCheckBox, QPushButton, QLabel, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets


class ClusteringWindow(QtWidgets.QDialog):
    def __init__(self , workspace):
        super().__init__()
        self.workspace = workspace
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Clustering Window')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.choice_box = QComboBox(self)
        self.choice_box.addItem("DBSCAN")
        self.choice_box.addItem("K-Means")
        self.choice_box.currentIndexChanged.connect(self.choice_changed)
        layout.addWidget(self.choice_box)
        self.parameters_widget = QWidget()
        self.parameters_layout = QVBoxLayout()
        self.parameters_widget.setLayout(self.parameters_layout)
        layout.addWidget(self.parameters_widget)
        self.apply_button = QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.apply_clicked)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)
        method = self.workspace.clustering_options.get("method")
        if method == "dbscan":
            self.choice_box.setCurrentIndex(0)
            self.choice_changed(0)
        elif method == "k-means":
            self.choice_box.setCurrentIndex(1)
        else:
            print("Unknown vectorization method:", method)

    def create_param_line_edit(self, label_text, default_value=None):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        if default_value is not None:
            line_edit.setText(str(default_value))
        return label, line_edit


    def choice_changed(self, index):
        for i in reversed(range(self.parameters_layout.count())):
            widget = self.parameters_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        if index == 0:
            labels_texts = ["MinPts:", "Epsilon:"]
            defaults = [self.workspace.clustering_options.get("minpts"),
                        self.workspace.clustering_options.get("epsilon")]
            for label_text, default_value in zip(labels_texts, defaults):
                print(label_text, default_value)
                label, line_edit = self.create_param_line_edit(label_text, default_value)
                self.parameters_layout.addWidget(label)
                self.parameters_layout.addWidget(line_edit)
        elif index == 1:
            labels_texts = ["Amount clusters:", "Max iteration amount:"]
            defaults = [self.workspace.clustering_options.get("num_clusters"),
                        self.workspace.clustering_options.get("max_iterations")]
            for label_text, default_value in zip(labels_texts, defaults):
                label, line_edit = self.create_param_line_edit(label_text, default_value)
                self.parameters_layout.addWidget(label)
                self.parameters_layout.addWidget(line_edit)

    def apply_clicked(self):
        chosen_method_index = self.choice_box.currentIndex()
        if chosen_method_index == 0:
            minpts = self.parameters_layout.itemAt(1).widget().text()
            epsilon = self.parameters_layout.itemAt(3).widget().text()
            # check minpts diapasone 0 , inf , int
            # check epsilon diaposone 0 , inf , double

            clustering_options = {
                'method' : 'dbscan',
                'minpts' :  int(minpts) if minpts else None,
                'epsilon' : float(epsilon) if epsilon else None
            }
            self.workspace.set_clustering_options(clustering_options)
            print(f"MinPts: {int(minpts) if minpts else None}")
            print(f"Epsilon: {float(epsilon) if epsilon else None}")
        elif chosen_method_index == 1:
            num_clusters = self.parameters_layout.itemAt(1).widget().text()
            max_iterations = self.parameters_layout.itemAt(3).widget().text()
            # check num_clusters 0 , inf , int
            # check max_iterations 0 , inf , int

            clustering_options = {
                'method' : 'k-means',
                'num_clusters' :  int(num_clusters) if num_clusters else None,
                'max_iterations' : int(max_iterations) if max_iterations else None
            }
            self.workspace.set_clustering_options(clustering_options)
            print(f"Amount clusters: {int(num_clusters) if num_clusters else None}")
            print(f"Max iteration amount: {int(max_iterations) if max_iterations else None}")
        self.close()