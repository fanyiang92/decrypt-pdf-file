import os
import sys
import threading
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
import shutil
import pikepdf



class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./ui/pdfdecrypted.ui")
        self.drag_file_frame = self.ui.lineEdit
        self.choose_folder = self.ui.toolButton
        self.choose_folder.clicked.connect(self.slot_btn_chooseFolder)
        self.password = self.ui.lineEdit_2
        self.start = self.ui.startButton
        self.start.clicked.connect(self.start_decryption)
        self.msg = self.ui.textBrowser

    def slot_btn_chooseFolder(self):
        self.dir_path = QFileDialog.getExistingDirectory(self,
                                                         "select folder",
                                                         './')

        if self.dir_path == "":
            print("\n取消选择")
            self.drag_file_frame.setText('Please select a folder')
            return

        print("\n你选择的文件为:")
        print(self.dir_path)
        self.drag_file_frame.setText(f'{self.dir_path}')
        # print("文件筛选器类型: ",filetype)

    def input_password(self):
        self.str1 = self.password.text()
        return self.str1

    def get_filelist(self, filelist_path):
        self.filelist_path = filelist_path
        self.filelist = []
        for home, dirs, files in os.walk(self.filelist_path):
            for filename in files:
                # 文件名列表，包含完整路径
                if ".pdf" in filename:
                    self.filelist.append(os.path.join(home, filename))
        return self.filelist

    def reclosed(self, fn, folder):
        self.fn = fn
        self.folder = folder
        self.passwd = self.password.text()
        pdf = pikepdf.open(fn, password=self.passwd)
        dir_name = os.path.dirname(fn)
        os_name = os.path.basename(fn).split('.')[0] + '_decrypted.pdf'
        new_name = os.path.join(dir_name, os_name)
        pdf.save(new_name)
        pdf.close()
        if not os.path.exists(folder):
            os.mkdir(folder)
        shutil.move(new_name, folder)

    def start_decryption(self):
        filelist = self.get_filelist(self.dir_path)
        foldername = os.path.join(self.dir_path, 'decrypted_files')
        for file in filelist:
            print('decrypting：', file)
            file_decrypted_start = threading.Thread(target=self.reclosed, args=(file,foldername))
            file_decrypted_start.start()
            self.msg.append(f'decrypting:\t{file}')
        self.msg.append('All pdf files are decrypted. Please Enjoy ^_^')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    # 展示窗口
    w.ui.show()

    sys.exit(app.exec_())
