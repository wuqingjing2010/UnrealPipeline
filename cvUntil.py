#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2
import numpy as np
from MPath import MPath
"""
CV 的封装

"""


def listMethod(nd, r_name='', show_help=False):
    print("current object type {}".format(type(nd)))
    for i in dir(nd):
        if r_name:
            if r_name.lower() in i.lower():
                print(i)
                if show_help:
                    help(getattr(nd, i))
            continue
        print(i)
        if show_help:
            help(getattr(nd, i))

class ImageNode():
    def __init__(self, file):
        if type(file) == str:
            ## 作为路径的输入
            self.file_path = MPath(file)
            self.image_data = cv2.imread(file_path)
            self.file_type = "FILE"
        elif type(file) == np.ndarray:
            self.image_data = file
            self.file_type = "ARRAY"
            self.file_path = None
        self.shape = self.image_data.shape

        self._height = self.shape[0]
        self._width = self.shape[1]

        self._center = ((self._width - 1) / 2, (self._height - 1) / 2)
        self.source_node = self.image_data.copy()
    def changing_color_space(self, convert_space_mode):
        """
        转换当前 颜色得色彩数据模式
        :param convert_space_mode: 参考cv 文档中 cv2.COLOR_xxxx 定义得模式
        :return:
        """
        return ImageNode(cv2.cvtColor(self.image_data, convert_space_mode))

    def blur(self, size, blur_type=2, radius=2, border_type=3):
        """
        对当前图像进行模糊操作
        :param blur_type: 0 blur
                          1 medianBlur
                          2 GaussianBlur
        :param size:   模糊大小以及强度
        :param radius: 高斯模糊得时候需要设置 高斯核得大小
        :param border_type: 边缘扩展类型 默认类型给 3
                         0  BORDER_REPLICATE
                         1  BORDER_REFLECT
                         2  BORDER_WRAP
                         3  BORDER_REFLECT_101
                         4  BORDER_TRANSPARENT

        :return:
        """
        border_list = [cv2.BORDER_REPLICATE,
                       cv2.BORDER_REFLECT,
                       cv2.BORDER_WRAP,
                       cv2.BORDER_REFLECT101,
                       cv2.BORDER_TRANSPARENT]

        if blur_type == 0:
            res = ImageNode(cv2.blur(self.image_data, size, borderType=border_list[border_type]))
        elif blur_type == 1:
            res = ImageNode(cv2.medianBlur(self.image_data, size, borderType=border_list[border_type]))
        else:
            res = ImageNode(cv2.GaussianBlur(self.image_data, size, radius, borderType=border_list[border_type]))
        return res

    def binary_image(self):
        self.image_gray = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
        return ImageNode(cv2.threshold(self.image_gray,127,255,0)[1])


    def threashold(self, thresh=127, maxval=255, threashold_type=0):
        """
        对该图像进行阈值操作
        :param thresh:  阈值分界点
        :param maxval:  最大阈值
        :param threashold_type: 阈值类型
                        cv.THRESH_BINARY
                        cv.THRESH_BINARY_INV
                        cv.THRESH_TRUNC
                        cv.THRESH_TOZERO
                        cv.THRESH_TOZERO_INV
        :return:  <ImageData>
        """
        return ImageNode(cv2.threshold(self.image_data, thresh, maxval, threashold_type)[1])

    def erode(self, radius):
        """
        形态学操作  腐蚀操作
        :return:
        """
        kernel = np.ones((radius, radius), np.uint8)
        return ImageNode(cv2.erode(self.image_data, kernel, anchor=(0, 0), iterations=3))

    def dilate(self, radius):
        kernel = np.ones((radius, radius), np.uint8)
        return ImageNode(cv2.dilate(self.image_data, kernel, anchor=(-1, -1), iterations=3))

    def morphology(self, operation, radius):
        """
        形态学操作
        :param operation: 操作方式 int 类型
        :param radius:  卷积核大小
        :return:
        """
        operation_method = [
            cv2.MORPH_OPEN,  # 0
            cv2.MORPH_CLOSE,  # 1
            cv2.MORPH_GRADIENT,  # 2
            cv2.MORPH_CROSS,  # 3
            cv2.MORPH_BLACKHAT,  # 4
            cv2.MORPH_TOPHAT,  # 5
            cv2.MORPH_RECT,  # 6
            cv2.MORPH_HITMISS  # 7
        ]
        kernel = np.ones((radius, radius), np.uint8)
        return ImageNode(cv2.morphologyEx(self.image_data, operation_method[operation], kernel))

    def sobel(self,ksize=3):
        """
        索贝算子
        :param ksize:  1 3 5 7 9
        :return:
        """
        x = cv2.Sobel(self.image_data,-1,1,0,ksize=ksize)
        y = cv2.Sobel(self.image_data,-1,0,1,ksize=ksize)
        return ImageNode(cv2.addWeighted(cv2.convertScaleAbs(x),0.5,cv2.convertScaleAbs(y),0.5,0))

    def Scharr(self):
        """
        scharr 算子
        :param ksize:  1 3 5 7 9
        :return:
        """
        x = cv2.Scharr(self.image_data,-1,1,0)
        y = cv2.Scharr(self.image_data,-1,0,1)
        return ImageNode(cv2.addWeighted(cv2.convertScaleAbs(x),0.5,cv2.convertScaleAbs(y),0.5,0))

    def laplacian(self):
        """
        拉普拉斯算子
        :return:
        """
        return ImageNode(cv2.convertScaleAbs(cv2.Laplacian(self.image_data,-1)))

    def bilateral_filter(self, distance=10, sigmaColor=50, sigmaSpace=50):
        """
        双边滤波函数
        :return:
        """
        return ImageNode(cv2.bilateralFilter(self.image_data, distance, sigmaColor, sigmaSpace))

    def canny(self,threshold1,threshold2):
        """
        canny 边缘查找
        :return:
        """
        return cv2.Canny(self.image_data,threshold1,threshold2)

    def mipmap(self):
        """
        对图像进行
        :return:
        """
        pass
    


    def contour_detection(self,index=-1,color=(0,255,0),thinkness=1):
        """

        :return:
        """
        contours,hierarchy = cv2.findContours(self.binary_image().image_data,
                                              cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE
                                              )
        for cnt in contours:

            if cv2.arcLength(cnt,True)< 20:
                continue
            # approx = cv2.approxPolyDP(cnt,epsilon,True)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(self.image_data,(x,y),(x+w,y+h),color,1)
        return self
        # return ImageNode(cv2.drawContours(self.image_data,contours,index,color,thinkness))

    def corner_detection(self,blockSize=3,ksize=3,k=0.001):

        return ImageNode(cv2.cornerHarris(np.float32(self.binary_image().image_data),blockSize,ksize,k)).dilate(10)




    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def center(self):
        return self._center

    def pixel_color(self, x, y):
        '''
        获取像素得颜色
        :return:
        '''
        return self.image_data[x, y]

    def set_pixel_color(self, x, y, color):
        """
        设置像素颜色
        :param x:
        :param y:
        :param color: <list> BGR 数组
        :return:
        """
        self.image_data[x, y] = color

    def combin_image_data(self,image_nodes,direction=True):
        """
        合并图片数据
        :param image_dataes: <tuple> ImageData
        :param direction: 默认为 横向， direction 给False 指定纵向
        :return:
        """
        images = tuple([data.image_data for data in image_nodes])
        if direction:
            res = np.hstack(images)
        else:
            res = np.vstack(images)
        return ImageNode(res)


    def show(self, time=2000, name='img'):
        """
        显示当前得 image
        :return:
        """
        cv2.imshow(name, self.image_data)
        cv2.waitKey(time)
        cv2.destroyWindow(name)

    def save(self, path):
        """
        保存当前图像到指定地址
        :param path:
        :return:
        """
        cv2.imwrite(path, self.image_data)

    def resize(self, height, width):
        """
        对图像进行缩放操作，将图像缩放到指定大小
        :param height:
        :param width:
        """
        self.image_data = cv2.resize(self.image_data, (width, height), interpolation=cv2.INTER_CUBIC)

    def translation(self, translationX, translationY):
        """
        对图像进行平移操作
        :param translationX:
        :param translationY:
        """
        self.image_data = cv2.warpAffine(self.image_data,
                                                   np.float32([[1, 0, translationX], [0, 1, translationY]]),
                                                   (self.height, self.width)
                                                   )


    def rotation(self, angle, scale=1):
        """
        对图像进行旋转操作
        :param angle: 旋转角度
        :param scale: 缩放值
        :return:
        """
        self.image_data = cv2.getRotationMatrix2D(self.center, angle, scale)




if __name__ == '__main__':
    # file_path = r'C:\Users\Administrator\Desktop\preview2.jpg'
    # file_path = r'A:\Users\Administrator\Desktop\bg2017121301.jpg'
    file_path = r'A:\Users\Administrator\Desktop\65cd01d83da55cfdabca7969c4ccb79b.jpg'
    # file_path = r'A:\Users\Administrator\Desktop\624629610785903385.jpg'
    img = ImageNode(file_path)
    # img.threashold()
    img.corner_detection().show(0)
    # img.show(0,'start')
    # img.resize(540,960)
    # edge = img.bilateral_filter(50,50,250).canny(240,255)
    # img.sobel()
    # nd.show(0)
    # cnd = nd.canny(240,255)
    # cv2.imshow('tt',edge)
    # cv2.waitKey(0)
    # cv2.destroyWindow('tt')