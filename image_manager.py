import os, shutil


class ImageManager:
    """
    图片管理器
    """

    def __init__(self, folder_path):
        self.folder_path = folder_path

        self.favorites_folder_path = os.path.join(folder_path, "Favorites")
        self.keep_folder_path = os.path.join(folder_path, "Keep")
        self.delete_folder_path = os.path.join(folder_path, "Delete")

        self.images = None
        self.index = 0
        self.load_images()

    def get_current_image(self):
        """
        :return: 当前图片
        """
        return self.images[self.index]

    def get_previous_image(self):
        """
        :return: 上一张图片
        """
        if self.index == 0:
            return None
        self.index -= 1
        return self.images[self.index]

    def get_next_image(self):
        """
        :return: 下一张图片
        """
        if self.index == len(self.images) - 1:
            return None
        self.index += 1
        return self.images[self.index]

    def get_image(self, index):
        """
        :return: 指定索引的图片
        """
        if index < 0 or index >= len(self.images):
            return None
        self.index = index
        return self.images[self.index]

    def move_favorites(self):
        """
        将当前图片复制后移动到收藏夹, 保留原路径中的文件
        """
        file_name = os.path.basename(self.images[self.index])
        shutil.copy(self.images[self.index], os.path.join(self.favorites_folder_path, file_name))

    def move_keep(self):
        """
        将当前图片复制到保留文件夹
        """
        file_name = os.path.basename(self.images[self.index])
        shutil.copy(self.images[self.index], os.path.join(self.keep_folder_path, file_name))

    def move_delete(self):
        """
        将当前图片复制到删除文件夹
        """
        file_name = os.path.basename(self.images[self.index])
        shutil.copy(self.images[self.index], os.path.join(self.delete_folder_path, file_name))

    def get_image_count(self):
        """
        :return: 图片总数
        """
        return len(self.images)

    def get_progress_string(self):
        """
        :return: 获取进度字符串
        """
        if self.images is None:
            return "No images"

        return f"{self.index + 1}/{len(self.images)}"

    def load_images(self):
        """
        从文件夹中读取图片
        """
        self.images = []

        for file_name in os.listdir(self.folder_path):
            if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png') or file_name.lower().endswith('.jpeg'):
                self.images.append(os.path.join(self.folder_path, file_name))
        self.index = 0

    def delete_all_images(self):
        """
        删除self.images中的所有图片
        """
        for image in self.images:
            os.remove(image)

    def get_folder_path(self):
        """
        :return:  图片文件夹路径
        """
        return self.folder_path

    def set_favorites_folder_path(self, path):
        """
        设置收藏夹路径
        :param path:
        """
        self.favorites_folder_path = path

    def set_keep_folder_path(self, path):
        """
        设置保留文件夹路径
        :param path:
        """
        self.keep_folder_path = path

    def set_delete_folder_path(self, path):
        """
        设置删除文件夹路径
        :param path:
        """
        self.delete_folder_path = path
