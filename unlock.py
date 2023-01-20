import shutil

import pikepdf
import os


def get_filelist(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路径
            if ".pdf" in filename:
                Filelist.append(os.path.join(home, filename))
    return Filelist


def reclosed(fn, passwd, folder):
    pdf = pikepdf.open(fn, password=passwd)
    dir_name = os.path.dirname(fn)
    os_name = os.path.basename(fn).split('.')[0] + '_decrypted.pdf'
    new_name = os.path.join(dir_name, os_name)
    pdf.save(new_name)
    pdf.close()
    if not os.path.isdir(folder):
        os.mkdir(folder)
    shutil.move(new_name, folder)


def removal(fn):
    os.remove(fn)


if __name__ == "__main__":
    path = input('please input the folder path (e.g. D:\venv3):')
    password = input('please input the password of pdf file:')
    filelist = get_filelist(path)
    foldername = os.path.join(path, 'decrypted_files')
    for file in filelist:
        print('decrypting：', file)
        reclosed(fn=file, passwd=password, folder=foldername)
input("please press any key to exit ^_^")