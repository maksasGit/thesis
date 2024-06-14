from PyQt5 import QtWidgets

class NewWorkspaceWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Workspace")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Create New Workspace")
        self.resize(400, 300)

        # Workspace name input
        self.workspace_name_label = QtWidgets.QLabel("Workspace Name:")
        self.workspace_name_edit = QtWidgets.QLineEdit()
        self.workspace_name_edit.setPlaceholderText("Enter workspace name")

        # File selection
        self.file_label = QtWidgets.QLabel("Select .txt File:")
        self.file_edit = QtWidgets.QLineEdit()
        self.file_edit.setPlaceholderText("Select .txt file")
        self.file_button = QtWidgets.QPushButton("Browse...")
        self.file_button.clicked.connect(self.browse_file)

        # Create button
        self.create_button = QtWidgets.QPushButton("Create")
        self.create_button.clicked.connect(self.create_workspace)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.workspace_name_label)
        layout.addWidget(self.workspace_name_edit)
        layout.addWidget(self.file_label)
        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select .txt File")
        if file_path:
            self.file_edit.setText(file_path)

    def read_txt(self, file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                data.append(line)
        return data

    def create_workspace(self):
        self.workspace_name = self.workspace_name_edit.text()
        self.file_path = self.file_edit.text()
        self.file_data = self.read_txt(self.file_path)
        print("Workspace Name:", self.workspace_name)
        print("File Path:", self.file_path)
        self.close()
