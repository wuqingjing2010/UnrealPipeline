#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import shutil
import hashlib

class MPath(str):
    def __init__(self, path):
        # super(MPath, self).__init__(path)
        self._path = str(path).replace('\\', '/')
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

    @property
    def parent(self):
        return MPath(self._parent)

    def child(self, *sub_folder):
        """
        创建子路径对象
        :param sub_folder:
        :return:
        """
        new_path = self._path
        for sf in sub_folder:
            new_path += '/' + sf
        return MPath(new_path)

    def rename(self, new_name):
        """
        对当前对象路径的文件或者文件夹进行重命名
        :param new_name:
        :return:
        """
        os.rename(self._path, self._parent + '/' + new_name)
        self.file_name = new_name

    @property
    def stem(self):
        """
        返回后缀
        :return:
        """
        return self._stem

    @property
    def ext(self):
        """
        返回后缀
        :return:
        """
        return self._stem

    @property
    def name(self):
        return self.file_name

    @property
    def exists(self):
        return os.path.exists(self._path)

    @property
    def isFile(self):
        return self.is_file

    @property
    def isFolder(self):
        return self.is_folder

    @property
    def path(self):
        return self._path

    def move(self, target_path, remove_file=False):
        """
        移动文件夹或者 移动文件
        :param target_path:
        :return:
        """
        target_path = MPath(target_path)
        if self.is_file:
            # 移动对象是 文件 的情况
            if target_path.exists:
                # 目标路径存在的情况
                if not target_path.is_folder:
                    # 目标存在并且 目标是文件的话，执行文件拷贝覆盖操作
                    shutil.copy(self._path, target_path)
                else:
                    # 目标存在 并且目标是文件夹，执行将文件拷贝到目标文件夹下
                    shutil.copy(self._path, target_path.child(self.name))
            else:
                # target_path 不存在的情况
                if target_path.name != self.name:
                    # 判断指定的名称 是否和 当前文件名称相同，如果不相同则认为 是直接文件路径到文件夹路径的拷贝操作 需要将当前文件 放到指定文件夹路径下
                    shutil.copy(self._path, target_path.child(self.name))
                else:
                    # 如果相同 则认为 是将文件路径 拷贝到指定文件路径下。
                    shutil.copy(self._path, target_path)
        else:
            # 移动对象是 文件夹 的情况
            if target_path.exists:
                # 目标路径存在的情况
                if target_path.is_file:
                    raise FileExistsError('目标路径被指定成了文件,无法将以存在的文件作为文件夹')
                # 执行操作，将当前文件夹下的所有文件 全部拷贝到指定的 文件夹下
            shutil.copytree(self._path, target_path)
        if remove_file:
            self.delete()

    def listdir(self, recursion=False, include_folder=True):
        """
        列出当前对象路径下的所有文件，默认会跳过 以. 开头的文件以及文件夹
        :param recursion:  是否开启递归查找
        :param include_folder:  返回列表是否包含文件夹
        :return:
        """
        if recursion:
            for f, dir, fs in os.walk(self._path):
                fs = [f for f in fs if not f[0] == '.']
                dir[:] = [d for d in dir if not d[0] == '.']
                if include_folder:
                    yield MPath(f)
                for i in fs:
                    if i == "Thumbs.db":
                        continue
                    yield MPath(os.path.join(f, i))
        else:
            if self._exists:
                for f in os.listdir(self._path):
                    if f[0] == '.':
                        continue
                    if os.path.isdir(self._path + '/' + f):
                        if include_folder:
                            yield MPath(self._path + '/' + f)
                        else:
                            continue
                    else:
                        yield MPath(self._path + '/' + f)
            else:
                return []

    def find(self, pattern, is_file=False, all=True):
        '''
        查找当前 路径下是否存在 名称与pattern 相匹配的文件 或者 文件夹返回列表。
        :param pattern:  <str> 需要匹配的部分
        :param is_file:  是文件还是 文件夹
        :param all:  是否是全匹配，还是部分匹配
        :return:
        '''
        if self.is_file:
            # 当前 路径指定 是文件的情况
            if all:
                return self if self.name == pattern else []
            else:
                return self if pattern in self.name else []
        else:
            # 当前 路径指定 是文件夹的情况
            fs = self.listdir(recursion=True)
            for f in fs:
                if (is_file and f.is_file) or (not is_file and f.is_folder):
                    if all and f.name==pattern:
                        yield f
                    if not all and pattern in f.name:
                        yield f


    def delete(self):
        '''
        将当前的文件或者文件夹给删除掉
        :return:
        '''
        if self.is_file:
            os.remove(self._path)
        if self.is_folder:
            shutil.rmtree(self._path)

    def makedir(self):
        """
        创建文件夹操作
        :return:
        """
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

        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    @property
    def md5(self):
        """
        计算当前文件的 MD5
        :return:
        """
        if self.is_file:
            f = open(self._path, 'rb')
            hash_md5 = hashlib.md5()
            hash_md5.update(f.read())
            return hash_md5.hexdigest()
        else:
            return None

    @property
    def size(self):
        if self.is_file:
            return os.path.getsize(self._path)
        else:
            f_size = 0
            for f in self.listdir(recursion=True):
                f_size += os.path.getsize(f)
            return f_size

    def __deepcopy__(self, memo):
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


if __name__ == '__main__':
    # pp = "D:\BaiduNetdiskDownload"
    # fp = MPath(pp)
    # for f in fp.listdir(recursion=False, include_folder=False):
    #     print(f)
    # # for f in fp.listdir(recursion=True):
    # #     print(f)
    sp = MPath('D:/TEMP/TEST')
    sp.move('D:/TEMP/STEST')