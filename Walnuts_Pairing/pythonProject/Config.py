import os
import yaml
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# def __init__(self, ui_file, main_window):
#     super().__init__()
#     self.config_file = 'config.yaml'
#     self.config = {}
#     self.main_window = main_window  # 保存主窗口实例

# 配置窗口类
class ConfigWindow(QMainWindow):
    def __init__(self, ui_file, main_window):
        super().__init__()
        self.config_file = 'config.yaml'
        self.config = {}
        self.main_window = main_window  # 保存主窗口实例

        # 创建一个 QUiLoader 实例
        loader = QUiLoader()

        # 打开 .ui 文件
        ui_file = QFile(ui_file)
        if not ui_file.open(QFile.ReadOnly):
            raise IOError(f"Cannot open {ui_file}: {ui_file.errorString()}")

        # 使用 QUiLoader 从 .ui 文件加载界面
        self.ui = loader.load(ui_file, self)

        # 确保界面加载成功
        if not self.ui:
            raise Exception("Failed to load UI file")

        # 关闭文件
        ui_file.close()

        # 设置父窗口
        self.setCentralWidget(self.ui)

        # 设置窗口大小
        self.resize(475, 400)  # 根据你的 .ui 文件中的大小设置

        # 设置窗口标题
        self.setWindowTitle("配置")

        # 初始化控件
        self.init_ui()

        # 显示界面
        self.show()

    def init_ui(self):
        # 尝试从配置文件中加载配置
        self.load_config()

        # 更新界面显示新的配置值
        self.ui.lineEdit_6.setText(str(self.config.get('root_folder', '')))
        self.ui.lineEdit_7.setText(str(self.config.get('yuppie', 0.8)))
        self.ui.lineEdit_5.setText(str(self.config.get('data_folder', 'example.db')))
        self.ui.lineEdit_9.setText(str(self.config.get('color', 0.1)))
        self.ui.lineEdit_11.setText(str(self.config.get('texture', 0.6)))
        self.ui.lineEdit_10.setText(str(self.config.get('edge', 2.3)))
        self.ui.lineEdit_8.setText(str(self.config.get('G', 0.88)))
        self.ui.lineEdit_4.setText(str(self.config.get('Goal', 0)))  # 注意这里使用了同一个 lineEdit 控件两次，可能需要检查是否正确

        # 保存按钮点击事件
        self.ui.pushButton_4.clicked.connect(self.save_config)

        # 选择根目录按钮点击事件
        self.ui.pushButton_2.clicked.connect(self.select_root)

        # 选择数据文件按钮点击事件
        self.ui.pushButton_3.clicked.connect(self.select_data)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file) or {}

                # 更新界面显示新的配置值
                self.ui.lineEdit_6.setText(str(self.config.get('root_folder', '')))
                self.ui.lineEdit_7.setText(str(self.config.get('yuppie', 0.8)))
                self.ui.lineEdit_5.setText(str(self.config.get('data_folder', 'example.db')))
                self.ui.lineEdit_9.setText(str(self.config.get('color', 0.1)))
                self.ui.lineEdit_11.setText(str(self.config.get('texture', 0.6)))
                self.ui.lineEdit_10.setText(str(self.config.get('edge', 2.3)))
                self.ui.lineEdit_8.setText(str(self.config.get('G', 0.88)))
                self.ui.lineEdit_4.setText(str(self.config.get('Goal', 0)))  # 注意这里使用了同一个 lineEdit 控件两次，可能需要检查是否正确

                # 将配置值设置到 QMainWindow 类上
                # self.root_folder = self.config.get('root_folder')
                # self.yuzhi = self.config.get('yuzhi')
                # self.data_folder = self.config.get('data_folder')

                # 弹出提示框
                QMessageBox.information(self, "Success", "Config loaded successfully.")
        except FileNotFoundError:
            # 弹出提示框
            QMessageBox.warning(self, "Error", f"{self.config_file} not found.")
        except yaml.YAMLError:
            # 弹出提示框
            QMessageBox.warning(self, "Error", f"Failed to parse {self.config_file}.")
        except Exception as e:
            # 捕获其他异常
            QMessageBox.warning(self, "Error", f"An error occurred while loading the configuration: {str(e)}")

    def save_config(self):
        try:
            # 从界面上获取新的配置值
            self.config['root_folder'] = self.ui.lineEdit_6.text()
            self.config['yuppie'] = float(self.ui.lineEdit_7.text())
            self.config['data_folder'] = self.ui.lineEdit_5.text()
            self.config['color'] = float(self.ui.lineEdit_9.text())
            self.config['texture'] = float(self.ui.lineEdit_11.text())
            self.config['edge'] = float(self.ui.lineEdit_10.text())
            self.config['G'] = float(self.ui.lineEdit_8.text())
            self.config['Goal'] = int(self.ui.lineEdit_4.text())  # 注意这里使用了同一个 lineEdit 控件两次，可能需要检查是否正确

            # 将配置写入文件
            with open(self.config_file, 'w') as file:
                yaml.safe_dump(self.config, file)

            # # 将配置值设置到 QMainWindow 类
            self.main_window.root_folder = self.config['root_folder']
            self.main_window.data_folder = self.config['data_folder']
            # self.main_window.lineEdit_5
            # self.main_window.lineEdit_5 = self.config['root_folder']
            # self.main_window.lineEdit= self.config['data_folder']
            self.main_window.ui.lineEdit_5.setText(str(self.config['root_folder']))
            self.main_window.ui.lineEdit.setText(str(self.config['data_folder']))
            print("更改成功")

            # 弹出提示框
            QMessageBox.information(self, "Success", "Config saved successfully.")
        except ValueError:
            # 处理类型转换错误
            QMessageBox.warning(self, "Error", "Invalid input. Please enter valid numbers.")
        except Exception as e:
            # 捕获所有其他异常
            QMessageBox.warning(self, "Error", f"An error occurred while saving the configuration: {str(e)}")

    def select_root(self):
        # 打开文件选择器选择数据文件
        data_file, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "Database Files (*.db);;All Files (*)")
        if data_file:
            self.ui.lineEdit_5.setText(data_file)
            self.config['data_folder'] = data_file

    def select_data(self):


        # 打开文件选择器选择根目录
        root_folder = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if root_folder:
            self.ui.lineEdit_6.setText(root_folder)
            self.config['root_folder'] = root_folder


if __name__ == '__main__':
    app = QApplication([])
    ui_file = "config.ui"
    config_window = ConfigWindow(ui_file)

    app.exec()

