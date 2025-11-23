import importlib
import os
import sqlite3
import subprocess
import sys

from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QLabel
from PySide6.QtCore import Slot, Qt

from MainWindows import Ui_MainWindows
import Sqldeal
from Config import ConfigWindow
from Configdeal import get_config_value


# 主界面类
# 编译 .ui 文件为 .py 文件

def compile_ui(ui_filename):
    py_filename = os.path.splitext(ui_filename)[0] + ".py"
    if not os.path.exists(py_filename) or os.path.getmtime(ui_filename) > os.path.getmtime(py_filename):
        # 使用相对路径调用 pyside6-uic
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pyside6_uic_path = os.path.join(script_dir, '.venv', 'Scripts', 'pyside6-uic.exe')
        cmd = [pyside6_uic_path, ui_filename, "-o", py_filename]
        subprocess.call(cmd)

# 加载编译后的 .py 文件
def load_ui_module(ui_filename):
    # compile_ui(ui_filename)
    module_name = os.path.splitext(os.path.basename(ui_filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
class MainWindow(QMainWindow):
    def __init__(self):
        # super().__init__()
        # self.ui = Ui_MainWindows()
        # self.ui.setupUi(self)

        super().__init__()
        # ui_file = "MainWindows.ui"
        # module = load_ui_module(ui_file)
        # Ui_MainWindows = getattr(module, "Ui_MainWindows")


        self.ui = Ui_MainWindows()
        self.ui.setupUi(self)  # 将加载的界面设置为 MainWindow 的属性

        # # 初始化全局变量
        # self.root_folder = r'C:\Users\Administrator\Desktop\shuju'
        # self.yuzhi = '0.8'
        # self.data_folder = 'example.db'

        self.root_folder = get_config_value('root_folder')
        self.yuzhi = get_config_value('yuppie')
        self.data_folder = get_config_value('data_folder')


        self.folder1_name=None
        self.folder2_name = None
        self.selected_date = ''


        # 按钮点击事件
        self.ui.pushButton.clicked.connect(self.on_unpair_button_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_similar_button_clicked)
        self.ui.pushButton_3.clicked.connect(lambda: self.setup_peiduibase_and_table_view())
        self.ui.pushButton_4.clicked.connect(lambda: self.setup_database_and_table_view())
        self.ui.pushButton_5.clicked.connect(self.on_peidui_button_clicked)

        # checkbox状态改变事件
        self.ui.checkBox_2.stateChanged.connect(self.on_DanXiangcheck_box_state_changed)

        # 菜单触发事件
        self.ui.actionSetting.triggered.connect(self.on_action_setting_triggered)

        # lineEdit文本改变事件
        self.ui.lineEdit_5.textChanged.connect(self.update_root_folder)
        self.ui.lineEdit_4.textChanged.connect(self.update_yuzhi)
        self.ui.lineEdit.textChanged.connect(self.update_data_folder)

        # 设置进度条范围和初始值
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)

        # 设置lineEdit的初始文本
        self.ui.lineEdit.setText(self.data_folder)
        self.ui.lineEdit_5.setText(self.root_folder)

        self.ui.image_label_1.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_2.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_3.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_4.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_5.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_6.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_7.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_8.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_9.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_10.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_11.setPixmap(QPixmap(u"log.png"))
        self.ui.image_label_12.setPixmap(QPixmap(u"log.png"))

        icon_path = "pic.png"  # 可以根据平台选择不同的图标文件
        self.setWindowIcon(QIcon(icon_path))
    @Slot()
    def on_unpair_button_clicked(self):
        print("取消配对选中")
        conn = sqlite3.connect(self.data_folder)
        c = conn.cursor()

        # 删除对应记录
        c.execute('''
                DELETE FROM time_stamped_similarities
                WHERE walnut_id1 = ? AND walnut_id2 = ?
            ''', (self.folder1_name, self.folder2_name))

        # 更新 walnut_selection 表中对应的记录的 selected 字段为 False
        c.execute("UPDATE walnut_selection SET selected=? WHERE walnut_name=?", (False, self.folder1_name))
        c.execute("UPDATE walnut_selection SET selected=? WHERE walnut_name=?", (False, self.folder2_name))

        # 提交更改并关闭连接
        conn.commit()
        conn.close()

        self.setup_peiduibase_and_table_view()
    @Slot()

    def on_similar_button_clicked(self):
        print("按下配对按键")
        Sqldeal.create_similarity_table(self.data_folder)
        print("初始化完成")
        Sqldeal.insert_walnut_names(self.root_folder,self.data_folder)
        print("修改全局表完成")
        Sqldeal.process_subfolders_and_store(self.data_folder,self.root_folder, self.ui.progressBar)
        print("训练按钮被按下")
    @Slot()
    def setup_peiduibase_and_table_view(self):
        global model, db
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.data_folder)
        if not db.open():
            print("无法打开数据库")
            return
        else:
            print("打开数据库")

        model = QSqlTableModel(self , db)
        model.setTable('time_stamped_similarities')

        model.select()  # 立即加载数据

        # 确认 QTableView 的名称与 Qt Designer 中的一致
        tableView = self.findChild(QTableView, 'tableView_2')
        if tableView is not None:
            print("Found QTableView with name:", tableView.objectName())
            tableView.setModel(model)



            # 隐藏不需要的列
            model.setHeaderData(1, Qt.Horizontal, "walnut_id1")  # 设置列标题
            model.setHeaderData(2, Qt.Horizontal, "walnut_id2")

            # 隐藏 id 列和 timestamp 列
            tableView.setColumnWidth(0, 0)  # 隐藏 id 列
            tableView.setColumnWidth(1, 0)  # 隐藏 timestamp 列

            model.setHeaderData(2, Qt.Horizontal, "编号1")
            model.setHeaderData(3, Qt.Horizontal, "编号2")

            # 应用日期过滤，如果 selected_date 为空，则不应用过滤

            self.selected_date = self.selected_date or ''  # 如果 selected_date 未定义，则设置为空字符串
            if self.selected_date:
                date_filter = f"timestamp >= '{self.selected_date} 00:00:00' AND timestamp <= '{self.selected_date} 23:59:59'"
                model.setFilter(date_filter)
            else:
                model.setFilter("")  # 清空过滤条件，加载所有记录
            model.select()  # 应用过滤并加载数据
            print("点击触发2")
            tableView.clicked.connect(self.on_row_clicked2)  # 添加括号

    @Slot()
    def setup_database_and_table_view(self):
        print("检索按键按下")
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.data_folder)
        if not db.open():
            print("无法打开数据库")
            return
        else:
            print("打开数据库")

        # 创建索引（如果尚未存在）
        query = QSqlQuery(db)
        query.exec_('CREATE INDEX IF NOT EXISTS idx_similarity ON similarities (similarity DESC, num DESC);')



        model = QSqlTableModel(self, db)
        model.setTable('similarities')

        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "编号1")
        model.setHeaderData(2, Qt.Horizontal, "编号2")
        model.setHeaderData(3, Qt.Horizontal, "总相似度")
        model.setHeaderData(4, Qt.Horizontal, "纹理")
        model.setHeaderData(5, Qt.Horizontal, "边缘")
        model.setHeaderData(6, Qt.Horizontal, "颜色")
        model.setHeaderData(7, Qt.Horizontal, "相似面数")

        # 设置排序
        model.setSort(3, Qt.SortOrder.DescendingOrder)  # 第3列是similarity，降序排序

        model.select()  # 立即加载数据

        # 确认 QTableView 的名称与 Qt Designer 中的一致
        tableView = self.findChild(QTableView, 'tableView')
        if tableView is not None:
            print("Found QTableView with name:", tableView.objectName())
            tableView.setModel(model)

            # 监听 clicked 信号
            self.ui.tableView.clicked.connect(self.on_row_clicked)

        if model is not None:
            model.setFilter(f"similarity > {self.yuzhi}")
            model.select()  # 应用过滤并加载数据
            # 获取应用过滤后的行数
            filtered_row_count = model.rowCount()

            # 将过滤后的行数转换为字符串并设置为lineEdit_2的文本
            self.ui.lineEdit_2.setText(str(filtered_row_count))

    @Slot()
    def on_peidui_button_clicked(self):
        print("确认配对按键按下")

        # 创建或打开数据库连接
        conn = sqlite3.connect(self.data_folder)
        c = conn.cursor()

        # 检查表是否存在，如果不存在则创建
        c.execute('''
                CREATE TABLE IF NOT EXISTS time_stamped_similarities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    walnut_id1 TEXT NOT NULL,
                    walnut_id2 TEXT NOT NULL
                );
            ''')
        print("创建成功")
        # 插入数据
        c.execute('''
                INSERT INTO time_stamped_similarities (walnut_id1, walnut_id2)
                VALUES (?, ?)
            ''', (self.folder1_name, self.folder2_name))

        c.execute("UPDATE walnut_selection SET selected=? WHERE walnut_name=?", (True, self.folder1_name))
        c.execute("UPDATE walnut_selection SET selected=? WHERE walnut_name=?", (True, self.folder2_name))

        # 提交更改并关闭连接
        conn.commit()
        conn.close()
        self.setup_peiduibase_and_table_view()
    @Slot(int)
    def on_DanXiangcheck_box_state_changed(self, state):
        pass  # 实现功能
    @Slot()
    def on_action_setting_triggered(self):
        print("触发设置")

        self.config_window = ConfigWindow("config.ui", self)  # 传递主窗口实例

    @Slot(str)
    def update_root_folder(self, text):
        self.root_folder = text
        print(f"根目录变量更新为：{self.root_folder}")
    @Slot(str)
    def update_yuzhi(self, text):
        self.yuzhi = text
        print(f"阈值变量更新为：{self.yuzhi}")
    @Slot(str)
    def update_data_folder(self, text):
        self.data_folder = text
        print(f"数据目录变量更新为：{self.data_folder}")

    def on_row_clicked(self,index):
        # 获取该行的所有列的值
        for column in range(index.model().columnCount()):
            cell_index = index.model().index(index.row(), column)
            cell_value = cell_index.data(Qt.ItemDataRole.DisplayRole)

            if column == 1:
                self.folder1_name = cell_value
            elif column == 2:
                self.folder2_name = cell_value

                print(self.folder1_name,self.folder1_name,self.root_folder)

        if self.folder1_name is not None and self.folder2_name is not None:
            self.load_images_and_names(self.root_folder, self.folder1_name, self.folder2_name)
    def on_row_clicked2(self,index):

        # 获取该行的所有列的值
        for column in range(index.model().columnCount()):
            cell_index = index.model().index(index.row(), column)
            cell_value = cell_index.data(Qt.ItemDataRole.DisplayRole)
 
            if column == 2:
                self.folder1_name = cell_value
            elif column == 3:
                self.folder2_name = cell_value

        if self.folder1_name is not None and self.folder2_name is not None:
            self.load_images_and_names(self.root_folder, self.folder1_name, self.folder2_name)
    def load_images_and_names(self, root_dir, folder1_name, folder2_name):
        # 拼接完整的文件夹路径
        folder1_path = os.path.join(root_dir, folder1_name)
        folder2_path = os.path.join(root_dir, folder2_name)

        # 获取文件夹中的文件名列表
        files1 = [f for f in os.listdir(folder1_path) if os.path.isfile(os.path.join(folder1_path, f))]
        files2 = [f for f in os.listdir(folder2_path) if os.path.isfile(os.path.join(folder2_path, f))]

        # 确保每个文件夹中有6张图片
        assert len(files1) == 6, "Folder 1 should contain exactly 6 images."
        assert len(files2) == 6, "Folder 2 should contain exactly 6 images."

        # 循环遍历文件夹中的图片和名字，并设置到对应的 QLabel
        for i in range(12):
            # 找到对应的 QLabel
            image_label_name = f'image_label_{i + 1}'
            name_label_name = f'name_label_{i + 1}'
            image_label = self.findChild(QLabel, image_label_name)
            name_label = self.findChild(QLabel, name_label_name)

            # 加载图像并设置到 QLabel
            if i < 6:
                image_path = os.path.join(folder1_path, files1[i])
                pixmap = QPixmap(image_path)
                pixmap_resized = pixmap.scaled(205, 247, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(pixmap_resized)
                name_label.setText(files1[i])  # 假设文件名即为名字
            else:
                image_path = os.path.join(folder2_path, files2[i - 6])
                pixmap = QPixmap(image_path)
                pixmap_resized = pixmap.scaled(205, 247, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(pixmap_resized)
                name_label.setText(files2[i - 6])  # 假设文件名即为名字
