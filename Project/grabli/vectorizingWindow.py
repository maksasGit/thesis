
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QCheckBox, QPushButton, QLabel, QLineEdit




class VectorizationWindow(QDialog):
    def __init__(self, workspace):
        super().__init__()
        self.workspace = workspace
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Vectorization Window')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.choice_box = QComboBox(self)
        self.choice_box.addItems(["Bag of Words", "TF-IDF", "Word2Vec"])
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
        method = self.workspace.vectorization_options.get("method")
        if method == "bag_of_words":
            self.choice_box.setCurrentIndex(0)
        elif method == "tf-idf":
            self.choice_box.setCurrentIndex(1)
        elif method == "word2vec":
            self.choice_box.setCurrentIndex(2)
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
            label, line_edit = self.create_param_line_edit("Max words amount:" ,self.workspace.vectorization_options.get("max_words"))
            self.parameters_layout.addWidget(label)
            self.parameters_layout.addWidget(line_edit)
        elif index == 1:
            label, line_edit = self.create_param_line_edit("Min word freq:", self.workspace.vectorization_options.get("min_freq"))
            self.parameters_layout.addWidget(label)
            self.parameters_layout.addWidget(line_edit)
        elif index == 2:
            labels_texts = ["Vector size:", "Window size:", "Min word freq:", "Iteration amount:"]
            defaults = [self.workspace.vectorization_options.get("vector_size"),
                        self.workspace.vectorization_options.get("context_window"),
                        self.workspace.vectorization_options.get("min_count"),
                        self.workspace.vectorization_options.get("iterations")]
            for label_text, default_value in zip(labels_texts, defaults):
                label, line_edit = self.create_param_line_edit(label_text, default_value)
                self.parameters_layout.addWidget(label)
                self.parameters_layout.addWidget(line_edit)

    def apply_clicked(self):
        chosen_method_index = self.choice_box.currentIndex()
        # chosen_method = self.choice_box.currentText()
        if chosen_method_index == 0:
            max_words = self.parameters_layout.itemAt(1).widget().text()
            vectorization_options = {
                'method' : 'bag_of_words',
                'max_words' : int(max_words) if max_words else None
            }
            self.workspace.set_vectorization_options(vectorization_options)
            print(f"Max words amount: {max_words}")
        elif chosen_method_index == 1:
            min_freq = self.parameters_layout.itemAt(1).widget().text()

            # check min_freq 0 , inf , int

            vectorization_options = {
                'method' : 'tf-idf',
                'min_freq' : int(min_freq) if min_freq else None
            }
            self.workspace.set_vectorization_options(vectorization_options)
            print(f"Min word freq: {min_freq}")
        elif chosen_method_index == 2:
            vector_size = self.parameters_layout.itemAt(1).widget().text()
            context_window = self.parameters_layout.itemAt(3).widget().text()
            min_count = self.parameters_layout.itemAt(5).widget().text()
            iterations = self.parameters_layout.itemAt(7).widget().text()

            # check vector_size
            # check context_window
            # check min_count
            # check iterations


            vectorization_options = {
                'method' : 'word2vec',
                'vector_size' : int(vector_size) if vector_size else None,
                'context_window' : int(context_window) if context_window else None,
                'min_count' : int(min_count) if min_count else None,
                'iterations' : int(iterations) if iterations else None,
            }
            self.workspace.set_vectorization_options(vectorization_options)
            print(f"Vector size: {vector_size}")
            print(f"Window: {context_window}")
            print(f"Min word freq: {min_count}")
            print(f"Iteration amount: {iterations}")
        self.close()
