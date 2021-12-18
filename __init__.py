#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 系统环境路径添加
import os,sys
dirname,filename = os.path.split(os.path.abspath(__file__))
sys.path.append(dirname)
# print('current exec file is '+__file__)


# TODO 初始化执行添加菜单相关
import uiUntil
uiUntil.addIqiyiUI()