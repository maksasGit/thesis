from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction
from workspaceTab import WorkspaceTab
from workspace import Workspace
from newWorkspaceWindow import NewWorkspaceWindow
from youtubeWindow import VideoInfoDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager")
        self.setGeometry(100, 100, 800, 600)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        comments_menu = menu_bar.addMenu("Comments")
        new_project_action = QAction("New Project", self)
        new_project_action.triggered.connect(self.add_new_project)
        youtube_action = QAction("YouTube", self)
        youtube_action.triggered.connect(self.get_youtube_comments)
        file_menu.addAction(new_project_action)
        comments_menu.addAction(youtube_action)


    def get_youtube_comments(self):
        dialog = VideoInfoDialog()
        dialog.exec()

    def add_new_project(self):
        dialog = NewWorkspaceWindow()
        dialog.exec()
        try:
            workspace = Workspace(dialog.workspace_name , dialog.file_data)
            print("Workspace: " , workspace.name , "created")
            new_tab = WorkspaceTab(workspace)
            print("WorkspaceTab created")
            self.tabs.addTab(new_tab, workspace.name)
            self.tabs.setCurrentWidget(new_tab)
        except Exception as e:
            print("Error while creating workspace")

    def close_tab(self, index):
        tab_to_remove = self.tabs.widget(index)
        if tab_to_remove:
            tab_to_remove.deleteLater()
