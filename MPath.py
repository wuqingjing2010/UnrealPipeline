#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os


class MPath(str):
    def __init__(self, path):
        super(MPath, self).__init__(path)
        self._path = path.replace('\\', '/')
        self.init_path()

    def init_path(self):
        self.is_folder = False
        self.is_file = False
        self._exists = False
        path_list = os.path.split(self._path)
        isdir = os.path.isdir(self._path)
        isfile = os.path.isfile(self._path)
        if isdir:
            self.is_folder = True
            self._exists = True
        else:
            if isfile:
                self.is_file = True
                self._exists = True
            else:
                if '.' in path_list[1]:
                    self.is_file = True
                else:
                    self.is_folder = True

        self._parent = path_list[0]
        self.file_name = path_list[1]

        if '.' in self.file_name:
            self._stem = self.file_name.split('.')[-1]
        else:
            self._stem = ''

        self.base_name = self.file_name.split('.')[0]

    @property
    def parent(self):
        return MPath(self._parent)

    def child(self, *sub_folder):
        new_path = self._path
        for sf in sub_folder:
            new_path += '/' + sf
        return MPath(new_path)

    @property
    def stem(self):
        return self._stem

    @property
    def name(self):
        return self.file_name

    @property
    def exists(self):
        return self._exists

    def isFile(self):
        return self.is_file

    def isFolder(self):
        return self.is_folder

    def listdir(self):
        if self._exists:
            return [MPath(f) for f in os.listdir(self._path)]
        else:
            return []

    def makedir(self):
        if not self._exists:
            os.makedirs(self._path)
            self._exists = True
        self.init_path()
        return self

    # def check_path(self):
    #     '''
    #     检查路径合法问题
    #     :return:
    #     '''
    #     pass
    def __copy__(self):
        print('copy')
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        print('deepcopy')
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, __import__("copy").deepcopy(v, memo))
        return result

    def __repr__(self):
        return self._path

    def __str__(self):
        return self._path


