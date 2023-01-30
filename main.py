import os
import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QMessageBox

from image_manager import ImageManager


class MainWindow(QMainWindow):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

        # 设置viewer
        self.message_box = None
        self.viewer = None
        self.image_label = QLabel(self)
        self.image_label.resize(600, 400)
        self.setCentralWidget(self.image_label)

        # 设置窗口标题
        self.setWindowTitle('Image Filter')

        # 创建菜单栏
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Folder')

        # 创建菜单栏中的项目
        open_folder_action = QAction('Open folder', self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

    def update_image(self):
        """
        更新图片
        """

        image_path = self.viewer.get_current_image()
        image = QPixmap(image_path)

        # 使图片适应label，保持图片比例
        image = image.scaled(self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio)

        # 使图片居中
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label.setPixmap(image)

        # 更新窗口标题
        self.setWindowTitle(f"Image Filter - {self.viewer.get_progress_string()}")

    def open_folder(self):
        """
        打开文件夹并返回文件夹路径
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "")

        # 如果用户没有选择文件夹，则直接返回
        if folder_path == "":
            return

        self.viewer = ImageManager(folder_path)

        if self.viewer.get_image_count() == 0:
            self.message_box = QMessageBox()
            self.message_box.setText("No images in the folder.")
            self.message_box.exec()
            return

        self.update_image()
        self.create_folder()

    def create_folder(self):
        """
        创建文件夹
        """

        # 在用户选择的文件夹中创建文件夹，命名为"Image Filter + 时间"
        # 在文件夹中创建文件夹，命名为"Favorites", "Keep", "Delete"

        # 以下为示例代码
        user_chosen_folder = self.viewer.get_folder_path()
        new_folder_path = os.path.join(user_chosen_folder, "Image Filter "
                                       + time.strftime("%Y%m%d%H%M%S", time.localtime()))
        os.mkdir(new_folder_path)
        os.mkdir(os.path.join(new_folder_path, "Favorites"))
        self.viewer.set_favorites_folder_path(os.path.join(new_folder_path, "Favorites"))
        os.mkdir(os.path.join(new_folder_path, "Keep"))
        self.viewer.set_keep_folder_path(os.path.join(new_folder_path, "Keep"))
        os.mkdir(os.path.join(new_folder_path, "Delete"))
        self.viewer.set_delete_folder_path(os.path.join(new_folder_path, "Delete"))

        # 判断所有文件夹是否创建成功
        if os.path.exists(new_folder_path) and os.path.exists(os.path.join(new_folder_path, "Favorites")) \
                and os.path.exists(os.path.join(new_folder_path, "Keep")) \
                and os.path.exists(os.path.join(new_folder_path, "Delete")):
            print("Folders created successfully!")

    def initialize_ui(self):
        """
        初始化界面
        """
        self.resize(600, 400)

    def keyPressEvent(self, event):
        """
        键盘事件
        :param event:
        """

        key = event.key()
        if key == Qt.Key.Key_Right:
            self.viewer.move_keep()
        elif key == Qt.Key.Key_Up:
            self.viewer.move_favorites()
        elif key == Qt.Key.Key_Down:
            self.viewer.move_delete()
        elif key == Qt.Key.Key_Left:
            self.viewer.move_previous()
        else:
            return

        if key != Qt.Key.Key_Left and self.viewer.get_next_image() is None:
            if self.selection_dialog("No more images. Do you want to delete all images in the folder?"):
                self.viewer.delete_all_images()

            self.close()

        self.update_image()

    def selection_dialog(self, message):
        """
        选择对话框
        :param message:
        :return:
        """
        reply = QMessageBox.question(self, 'Message', message, QMessageBox.StandardButton.Yes,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.initialize_ui()
    main_window.show()
    sys.exit(app.exec())
