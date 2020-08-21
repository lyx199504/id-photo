#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/21 12:22
# @Author : LYX-夜光

from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageQt

class Photo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindow()

    def setWindow(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()  # 显示器屏幕
        self.winWidth, self.winHeight = screen.width() / 1.5, screen.height() / 1.5
        self.resize(self.winWidth, self.winHeight)  # 设置窗口大小
        self.setWindowTitle("处理证件照")

        buWidth, buHeight = self.winWidth / 13, self.winHeight / 13  # 按钮大小
        # 打开图片按钮
        button1 = QtWidgets.QPushButton("打开", self)
        button1.resize(buWidth, buHeight)
        button1.clicked.connect(self.getPhoto)
        # 保存图片按钮
        button2 = QtWidgets.QPushButton("保存", self)
        button2.resize(buWidth, buHeight)
        button2.move(buWidth, 0)
        button2.clicked.connect(self.setPhoto)
        # 参数文本框
        self.text1 = QtWidgets.QPlainTextEdit(self)
        self.text1.setPlaceholderText("像素宽度(默认319)")
        self.text1.resize(buWidth, buHeight)
        self.text1.move(buWidth * 2, 0)

        self.text2 = QtWidgets.QPlainTextEdit(self)
        self.text2.setPlaceholderText("像素高度(默认449)")
        self.text2.resize(buWidth, buHeight)
        self.text2.move(buWidth * 3, 0)

        self.text3 = QtWidgets.QPlainTextEdit(self)
        self.text3.setPlaceholderText("dpi(默认350)")
        self.text3.resize(buWidth, buHeight)
        self.text3.move(buWidth * 4, 0)
        # 裁剪按钮
        button3 = QtWidgets.QPushButton("裁剪预览", self)
        button3.resize(buWidth, buHeight)
        button3.move(buWidth * 5, 0)
        button3.clicked.connect(self.crop)
        # 中点x坐标
        self.text4 = QtWidgets.QPlainTextEdit(self)
        self.text4.setPlaceholderText("中心x坐标")
        self.text4.resize(buWidth, buHeight)
        self.text4.move(buWidth * 6, 0)

        self.text5 = QtWidgets.QPlainTextEdit(self)
        self.text5.setPlaceholderText("左下x坐标")
        self.text5.resize(buWidth, buHeight)
        self.text5.move(buWidth * 7, 0)

        self.text6 = QtWidgets.QPlainTextEdit(self)
        self.text6.setPlaceholderText("左下y坐标")
        self.text6.resize(buWidth, buHeight)
        self.text6.move(buWidth * 8, 0)
        # 使用说明
        button3 = QtWidgets.QPushButton("使用说明", self)
        button3.resize(buWidth, buHeight)
        button3.move(buWidth * 9, 0)
        button3.clicked.connect(self.description)

        # 子窗口大小
        self.swinWidth, self.swinHeight = self.winWidth / 2, self.winHeight - buHeight
        # 左侧子窗口原照片
        self.subwindow1 = QtWidgets.QPlainTextEdit(self)
        self.subwindow1.resize(self.swinWidth, self.swinHeight)
        self.subwindow1.move(0, buHeight)
        self.subwindow1.setPlaceholderText("原照片")
        # 右侧子窗口预览处理后的照片
        self.subwindow2 = QtWidgets.QPlainTextEdit(self)
        self.subwindow2.resize(self.swinWidth, self.swinHeight)
        self.subwindow2.move(self.swinWidth, buHeight)
        self.subwindow2.setPlaceholderText("处理后照片预览")

        self.label1 = QtWidgets.QLabel(self.subwindow1)  # 原照片
        self.label1.mousePressEvent = self.getPhotoPos
        self.label2 = QtWidgets.QLabel(self.subwindow2)  # 处理后照片预览
    # 获取图片的坐标
    def getPhotoPos(self, event):
        try:
            x_cen = float(self.text4.toPlainText().strip())
        except:
            x_cen = -1
        try:
            x_left = float(self.text5.toPlainText().strip())
        except:
            x_left = -1
        try:
            y_down = float(self.text6.toPlainText().strip())
        except:
            y_down = -1
        if x_cen < 0:
            self.text4.setPlainText(str(event.x()))
        else:
            if x_left < 0:
                self.text5.setPlainText(str(event.x()))
            if y_down < 0:
                self.text6.setPlainText(str(event.y()))
    # 打开图片
    def getPhoto(self):
        self.openFile = QtWidgets.QFileDialog.getOpenFileName()[0]  # 打开文件获取链接
        pix = QtGui.QPixmap(self.openFile)
        self.oriPhoWidth, self.oriPhoHeight = pix.width(), pix.height()
        widPerHei = self.oriPhoWidth / self.oriPhoHeight  # 照片的宽高比
        margin = 10  # 与方框的最小间隔
        # 重设照片的宽和高
        self.phoWidth = self.swinWidth - margin
        self.phoHeight = self.phoWidth / widPerHei
        # 若照片高度超出显示宽，则再重新设置宽高
        if self.phoHeight > self.swinHeight - margin:
            self.phoHeight = self.swinHeight - margin
            self.phoWidth = self.phoHeight * widPerHei
        self.label1.move((self.swinWidth - self.phoWidth) / 2, (self.swinHeight - self.phoHeight) / 2)
        self.label1.setPixmap(QtGui.QPixmap())
        self.label1.setPixmap(pix)
        self.label1.resize(self.phoWidth, self.phoHeight)
        self.label1.setScaledContents(True)  # 图片自适应
    # 裁剪图片
    def crop(self):
        try:
            width = float(self.text1.toPlainText().strip())
            height = float(self.text2.toPlainText().strip())
        except:
            width, height = 319, 449
        try:
            x_cen = float(self.text4.toPlainText().strip())
            x_left = float(self.text5.toPlainText().strip())
            y_down = float(self.text6.toPlainText().strip())
        except:
            QtWidgets.QMessageBox.about(self, "操作错误", "请先填写相应的坐标！")
            return
        width_mul, height_mul = self.oriPhoWidth / self.phoWidth, self.oriPhoHeight / self.phoHeight
        x_cen, x_left, y_down = x_cen*width_mul, x_left*width_mul, y_down*height_mul
        self.img = Image.open(self.openFile)
        newW = (x_cen - x_left) * 2  # 裁剪图的宽
        newH = height / width * newW  # 裁剪图的高
        self.img = self.img.crop((x_left, y_down - newH, x_left + newW, y_down))  # 裁剪
        self.img = self.img.resize((width, height))  # 重设大小
        self.previewPhoto()

    # 预览图片
    def previewPhoto(self):
        pix = ImageQt.toqpixmap(self.img)
        self.label2.move((self.swinWidth - pix.width()) / 2, (self.swinHeight - pix.height()) / 2)
        self.label2.setPixmap(QtGui.QPixmap())
        self.label2.setPixmap(pix)
        self.label2.resize(pix.width(), pix.height())
        self.label2.setScaledContents(True)  # 图片自适应

    # 保存图片
    def setPhoto(self):
        self.saveFile = QtWidgets.QFileDialog.getSaveFileName()[0]
        try:
            dpi = float(self.text3.toPlainText().strip())
        except:
            dpi = 350
        self.img.save(self.saveFile, dpi=(dpi, dpi))
        self.img.close()

    # 使用说明
    def description(self):
        QtWidgets.QMessageBox.about(self, "使用说明",
"""1. 点击“打开”按钮打开图片文件
2. 先点击照片中心（即眉心处）获取照片中心x坐标
3. 再点击照片左下角获取裁剪图的左下x和y坐标
4. 点击“保存”按钮保存图片""")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    photo = Photo()
    photo.show()
    app.exec_()