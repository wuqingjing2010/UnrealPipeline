#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unreal
from MPath import MPath
e_util = unreal.EditorUtilityLibrary()
a_util = unreal.EditorAssetLibrary()
str_util = unreal.StringLibrary()
sys_util = unreal.SystemLibrary()
l_util = unreal.EditorLevelLibrary()


class UNode:
    '''
    对大纲种Actor 对象的封装，目前可以通过该对象修改的属性有
    '''

    def __init__(self, UActor):
        # TODO 需要考虑实例化的时候 方式有哪几类
        self.node = UActor
        self.node_name = UActor.get_name()
        self.node_type = UActor.get_class().get_fname()
        self.node_path = UActor.get_path_name()
        # self.node_asset =
        self.vaild = False
        self.hidden = False
        self.hidden_game = False

        # self.attribute_list = ['hidden']

        pass

    def hidden(self, game=False):
        '''
        隐藏该对象
        :return:
        '''
        if game:
            if self.hidden_game:
                self.node.set_actor_hidden_in_game(False)
                self.hidden_game = False
            else:
                self.node.set_actor_hidden_in_game(True)
                self.hidden_game = True
        else:
            if self.hidden:
                self.node.hidden

        pass

    def delete(self):
        '''
        删除该对象
        :return:
        '''
        pass

    def parent(self):
        '''
        放在某个父节点下
        :return:
        '''
        pass

    def __getattr__(self, item):
        '''
        绑定该类和封装类的属性设置
        :param item:
        :return:
        '''
        return getattr(self.node, 'get_' + item)

    def __setattr__(self, key, value):
        '''
        绑定该类和封装类的属性设置
        :param key:
        :param value:
        :return:
        '''
        set_func = getattr(self.node, 'set_' + key)
        if set_func:
            set_func(value)

    def component(self):
        '''
        获取当前 node 下的所有component
        :return:
        '''
        pass

    def child(self):
        '''
        获取当前节点的子节点
        :return:
        '''
        return self.node.get_all_child_actors()

    def distance(self, actor):
        '''
        返回当前 actor 到其他actor 的距离
        :return:
        '''
        pass
        return self.node.get_distance_to(actor)

class FolderNode:

    def __init__(self,directory_path):
        self.node_path = MPath(directory_path)
        self.node_directory = MPath(sys_util.get_project_content_directory()+directory_path.replace('/Game/',''))
        if not a_util.does_directory_exist(self.node_path):
            unreal.log_error("Path is not exists.")

    @property
    def children(self):
        '''
        获取当前文件夹下的子文件
        :return:
        '''
        file_list = self.node_directory.listdir()

        self._children = []
        for f in file_list:
            # 从系统文件层面获取到该路径下都有哪些文件 会有 三种情况
            # 第一种 是文件夹的情况
            # 第二种 是UE资产类的文件
            # 第三种 是非UE资产类的文件
            if f.is_folder:
                self._children.append(ANode(str(self.node_path.child(f.base_name))))
            else:
                a_node = ANode(str(self.node_path.child('{name}.{name}'.format(name=f.base_name))))
                if a_node.vaild:
                    self._children.append(a_node)

        return self._children

    @property
    def name(self):
        return self.node_path.name

    def get_name(self):
        return self.name

    def makedir(self,folder_name):
        new_dir = self.node_directory.child(folder_name)
        if not a_util.does_directory_exist(new_dir):
            new_dir.makedir()
        else:
            unreal.log_warning('{} folder directory exists.'.format(new_dir))
        return ANode(str(self.node_path.child(folder_name)))

    def listdir(self):
        return self.children

    def isNull(self,delete=True):
        '''
        判断当前文件夹是否为空，如果为空的状态，默认执行完后会将当前文件夹删除掉
        :param delete:
        :return:
        '''
        if delete:
            if self.children:
                a_util.delete_directory(self.node_path)
                return True
            else:
                return False
        else:
            return False if self.children else True

    def rename(self,newname):
        a_util.rename_directory(self.node_path,self.node_path.parent.child(newname))
        self.node_path = self.node_path.parent.child(newname)
        self.node_directory = MPath(sys_util.get_project_content_directory()+self.node_path.replace('/Game/',''))

class ANode:
    # Content Browser 中的asset_data的对象封装

    def __init__(self, UAsset):
        # 实例化时候可以 传入 object 实例化  或者对 asset_data 进行实例化  或者 提供asset_path 进行实例化
        self.vaild = False
        self._children = []
        if type(UAsset) == type(unreal.AssetData()):
            unreal.log("current {} is asset data".format(UAsset))
            # 说明当前 是 AssetData 被传入进来了
            self.node_asset = UAsset

            self.node = UAsset.get_asset()
            self.node_path = MPath(UAsset.object_path)
            self.node_directory = MPath(sys_util.get_system_path(self.node))
            self.node_type = self.node.get_class().get_name()
            self.vaild = True

        elif type(UAsset) == str:
            unreal.log("current {} is node path".format(UAsset))
            # 如果默认传入路径字符串，首先会当文件夹类型处理，其次在会去当资产进行判断
            if a_util.does_directory_exist(UAsset):
                #  判断路径是否存在，间接的确认了传入进来的是条路径
                self.node = FolderNode(UAsset)
                self.node_path = MPath(UAsset)
                self.node_type = 'folder'
                self.node_asset = unreal.AssetData(self.node_path)
                self.node_directory = MPath(sys_util.get_project_content_directory()+UAsset.replace('/Game/',''))
                self.vaild = True

            elif a_util.does_asset_exist(UAsset):
                # 当前是资产路径的情况下
                self.node_asset = unreal.AssetData(UAsset)
                self.node = self.node_asset.get_asset()
                self.node_type = self.node.get_class().get_name()
                self.node_path = MPath(self.node.get_path_name())
                self.node_directory = MPath(sys_util.get_system_path(self.node))
                self.vaild = True
            else:
                show_message('current folder is not exists。')

        elif UAsset:
            # 这个地方判别 为 object 类型方法，后续可以继续改善，目前默认上面两种情况都不是的时候就判定为 object 类型，
            # 同时获取 object 类型转换为 asset_data 方法可以继续优化，目前完全是通过字符串拼接的方式进行分离
            unreal.log("current {} is asset node".format(UAsset))
            self.node_path = MPath(UAsset.get_path_name())
            self.node_type = UAsset.get_class().get_name()
            self.node = UAsset
            self.node_asset = unreal.AssetData(self.node_path)
            self.node_directory = MPath(sys_util.get_system_path(self.node))
            self.vaild = True
        else:
            unreal.log_error(UAsset)
            unreal.log_error('convert asset node failure.')

        if self.vaild:
            # 这个地方后续可以根据 实际 得到不同类型的 节点进行针对性定制化的操作
            self.name = self.node.get_name()
            if self.node_type == 'folder':
                self.init_folder()
            elif self.node_type == 'blueprint':
                self.init_blueprint()
            else:
                self.init_asset()


    def init_asset(self):
        '''
        如果是asset 需要处理哪些事情
        :return:
        '''
        # unreal.log(self.node_type+' init exec.')
        pass

    def init_blueprint(self):
        '''
        如果是蓝图需要处理的事情
        :return:
        '''
        # unreal.log('blueprint init exec.')
        pass


    def init_folder(self):
        '''
        如果是folder类型需要针对folder 类型处理的事情，例如获取父文件夹，获取子列表
        :return:
        '''
        # 获取该文件夹下的 文件情况 如果是 文件夹依然返回 文件夹的 ANode 如果是资产返回 ANode 资产类
        self._children = self.node.children

    @property
    def children(self):
        if self.node_type == 'folder':
            return self._children
        else:
            unreal.log_error('cuurent object is not folder type!')


    @property
    def parent(self):
        if self.node_path == '/Game':
            return self
        else:
            return ANode(self.node_path.replace('/'+self.node_path.split('/')[-1],''))

    def delete(self):
        if self.vaild:
            if self.node_type == "folder":
                a_util.delete_directory(self.node_path)
            else:
                a_util.delete_asset(self.node_path)

    def list_dir(self):
        if self.vaild:
            return a_util.list_assets(self.node_path) if self.node_type == "folder" else None

    def load(self, location=unreal.Vector(), rotation=unreal.Rotator()):
        '''
        将当前节点加载到场景
        :param location:  actor的位置
        :param rotation:  actor的旋转
        :return:  返回Actor 对象
        '''
        if self.vaild:
            ## 将当前 node 添加到场景
            if self.node_type != 'folder':
                if self.node_type == "blueprint":
                    actor = l_util.spawn_actor_from_class(self.node, location, rotation)
                else:
                    actor = l_util.spawn_actor_from_object(self.node, location, rotation)
                return actor
            else:
                show_message('current node is folder')

    def rename(self,newname):
        if self.node_type != 'folder':
            a_util.rename_asset(self.node_path,self.node_path.parent.child(newname))
            self.node_path = self.node_path.parent.child(newname)

        else:
            self.node.rename(newname)


    def copy(self, des_path):
        '''
        todo 将当前节点拷贝到某个地方
        :return:
        '''
        pass




############# 测试函数 ###############
if __name__ == '__main__':
    uactor = UNode(actor)



















