#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2
import numpy as np

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


class ImageData():
    """
    cv 读取图片后得数据封装
    """

    def __init__(self, image_node):
        self.image_data = image_node
        self._height,self._width,self.channel = self.image_data.shape
        self._center = ((self._width-1)/2,(self._height-1)/2)
        self.source_data = image_node

    def changing_color_space(self, convert_space_mode):
        """
        转换当前 颜色得色彩数据模式
        :param convert_space_mode: 参考cv 文档中 cv2.COLOR_xxxx 定义得模式
        :return:
        """
        return ImageData(cv2.cvtColor(self.image_data, convert_space_mode))

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def center(self):
        return self._center


    def show(self, time=2000):
        """
        显示当前得 image
        :return:
        """
        cv2.imshow('img', self.image_data)
        cv2.waitKey(time)
        cv2.destroyWindow('img')


class ImageNode():
    def __init__(self, file_path):
        self.image_node = ImageData(cv2.imread(file_path))
        self.source_node = ImageData(cv2.imread(file_path))

    def threashold(self, thresh, maxval, threashold_type):
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
        return ImageData(cv2.threshold(self.image_node, thresh, maxval, threashold_type))

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
            self.image_node = cv2.blur(self.image_node, size, borderType=border_list[border_type])
        elif blur_type == 1:
            self.image_node = cv2.medianBlur(self.image_node, size, borderType=border_list[border_type])
        else:
            self.image_node = cv2.GaussianBlur(self.image_node, size, radius, borderType=border_list[border_type])
        return self.image_node

    # def bilateral_filter(self,):

    def pixel_color(self,x,y):
        '''
        获取像素得颜色
        :return:
        '''
        return self.image_node.image_data[x,y]

    def set_pixel_color(self,x,y,color):
        """
        设置像素颜色
        :param x:
        :param y:
        :param color: <list> BGR 数组
        :return:
        """
        self.image_node.image_data [x,y] = color

    def show(self, time=2000):
        """
        显示当前得 image
        :return:
        """
        cv2.imshow('img', self.image_node)
        cv2.waitKey(time)
        cv2.destroyWindow('img')

    def resize(self, height, width):
        """
        对图像进行缩放操作，将图像缩放到指定大小
        :param height:
        :param width:
        """
        self.image_node = ImageData(cv2.resize(self.image_node, (width, height), interpolation=cv2.INTER_CUBIC))

    def translation(self,translationX,translationY):
        """
        对图像进行平移操作
        :param translationX:
        :param translationY:
        """
        self.image_node = ImageData(cv2.warpAffine(self.image_node,
                                        np.float32([[1,0,translationX],[0,1,translationY]]),
                                        (self.height,self.width)
                                                   )
                                    )


    def rotation(self,angle,scale=1):
        """
        对图像进行旋转操作
        :param angle: 旋转角度
        :param scale: 缩放值
        :return:
        """
        self.image_node = ImageData(cv2.getRotationMatrix2D(self.center,angle,scale))

    @property
    def height(self):
        return self.image_node.height

    @property
    def width(self):
        return self.image_node.width

    @property
    def center(self):
        return self.image_node.center


if __name__ == '__main__':
    file_path = r'C:\Users\Administrator\Desktop\preview2.jpg'
    img = ImageNode(file_path)
    res = cv2.bilateralFilter(img.image_node.image_data, 100, 500, 500)
    cv2.imshow('res',res)
    cv2.waitKey(0)

    # listMethod(img.image_node)
