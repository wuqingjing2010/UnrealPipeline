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
        self.path = directory_path.replace('\\','/')
        if not a_util.does_directory_exist(self.path):
            unreal.log_error("Path is not exists.")

    def children(self):
        '''
        获取当前文件夹下的子文件
        :return:
        '''

        pass

    @property
    def stem(self):
        pass

    @property
    def name(self):
        pass

    def makedir(self):

        pass

    def listdir(self):
        pass

    def is_folder(self):
        pass

    def is_file(self):
        pass


class ANode:
    # Content Browser 中的asset_data的对象封装

    def __init__(self, UAsset):
        # 实例化时候可以 传入 object 实例化  或者对 asset_data 进行实例化  或者 提供asset_path 进行实例化
        self.vaild = False
        if type(UAsset) == type(unreal.AssetData()):
            unreal.log("current Uasset is asset data")
            # 说明当前 是 AssetData 被传入进来了
            self.node_asset = UAsset

            self.node = UAsset.get_asset()
            self.node_path = UAsset.object_path
            self.node_directory = sys_util.get_system_path(self.node)
            self.node_type = self.node.asset_class
            self.vaild = True

        elif type(UAsset) == str:
            unreal.log("current Uasset is node path")
            # 如果默认传入路径字符串，首先会当文件夹类型处理，其次在会去当资产进行判断
            if a_util.does_directory_exist(UAsset):
                #  判断路径是否存在，间接的确认了传入进来的是条路径
                self.node = FolderNode(UAsset)
                self.node_path = sys_util.get_project_content_directory()+UAsset.replace('/Game/','')
                self.node_type = 'folder'
                self.node_asset = unreal.AssetData(self.node_path)
                self.node_directory = UAsset

                self.vaild = True

            elif a_util.does_asset_exist(UAsset):
                # 当前是资产路径的情况下
                self.node = a_util.load_asset(UAsset)
                self.node_type = self.node.get_full_name().split(' ')[0]
                self.node_path = self.node.get_full_name().split(' ')[1]
                self.node_asset = unreal.AssetData(self.node_path)
                self.node_directory = sys_util.get_system_path(self.node)
                self.vaild = True
            else:
                show_message('current folder is not exists。')

        elif UAsset:
            # 这个地方判别 为 object 类型方法，后续可以继续改善，目前默认上面两种情况都不是的时候就判定为 object 类型，
            # 同时获取 object 类型转换为 asset_data 方法可以继续优化，目前完全是通过字符串拼接的方式进行分离
            unreal.log("current Uasset is asset node")
            self.node_path = UAsset.get_full_name().split(' ')[1]
            self.node_type = UAsset.get_full_name().split(' ')[0]
            self.node = UAsset
            self.node_asset = unreal.AssetData(self.node_path)
            self.node_directory = sys_util.get_system_path(self.node)
            self.vaild = True
        else:
            unreal.log_error(UAsset)
            unreal.log_error('convert asset node failure.')

        if self.vaild:
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
        file_list = self.node.listdir()
        self.child = {}
        # 如果该文件是 文件夹 转换成相对路径生成 folder 类型的 node
        self.child.update({f.name:ANode(self.node_path+'/'+f.name) for f in file_list if f.is_folder()})

        # TODO 这里测试发现 list_assets 无法获得 level object
        for dp in a_util.list_assets(self.node_path, recursive=False):
            nd = ANode(dp)
            if nd.name in self.child:
                # 说明有重名 可能是 文件夹和 object 重名，将名称重新对应为
                self.child[nd.name] = (self.child[nd.name],nd)



    @property
    def parent(self):
        if self.node_path == '/Game':
            return self
        else:
            return ANode(self.node_path.replace('/'+self.node_path.split('/')[-1],''))

    def delete(self):
        if self.vaild:
            if self.node_type == "folder":
                a_util.delete_directory(self.node)
            else:
                a_util.delete_asset(self.node)

    def list_dir(self):
        if self.vaild:
            return a_util.list_assets(self.node_path) if self.node_type == "folder" else None

    def load(self, location=unreal.Vector(), rotation=unreal.Rotator()):
        if self.vaild:
            ## 将当前 node 添加到场景
            if self.node_type != 'folder':
                if self.node_type == "blueprint":
                    l_util.spawn_actor_from_class(self.node, location, rotation)
                else:
                    l_util.spawn_actor_from_object(self.node, location, rotation)
            else:
                show_message('current node is folder')

    def copy(self, des_path):
        '''
        todo 将当前节点拷贝到某个地方
        :return:
        '''
        pass




def show_message(message, level='log', window=False):
    '''
    显示消息的方式 默认两种方式 第一种 在outlog 中打印log 其中logo分三个 级别  对应 log warning error
    第二种方式弹窗的方式 进行显示， 分两种 第一种 只弹确认窗口，第二种弹出 确认与否 窗口 其中 log 方式为 确认窗口，以外为确认与否窗口
    :param message:  需要显示的内容
    :param level: 级别  log warning error 三种
    :param window: 是否开启窗口告知
    :return:
    '''
    pass


def ls(outliner=True, sl=False, node_type='', package=True):
    """
    方法 同 maya 如果需要 得到 原始 clarisse 的节点 把 package 设置成 false 即可
    :param outliner: 默认对大纲中的对象进行选择操作
    :param node_type:
    :param sl:
    :param package:
    :return:
    """
    if sl:
        # 获取当前所选择
        if node_type:
            # 找到指定类型
            all_sel_obj = selected(outliner=outliner)
            target_type_obs = [obj for obj in all_sel_obj if obj.type == node_type]
            return target_type_obs if package else [obj.node for obj in target_type_obs]
        else:
            return selected(outliner=outliner, package=package)

    else:
        # 查找场景所有 对象
        if outliner:
            all_nodes = [UNode(nd) for nd in l_util.get_all_level_actors()]
        else:
            # 获取当前 文件夹下的所有 asset
            all_nodes = [ANode(nd) for nd in a_util.list_assets(sys_util.get_project_content_directory())]
        if node_type:
            # 返回场景中所有指定类型的对象
            res_nds = [nd for nd in all_nodes if nd.type == node_type]
            return res_nds if package else [nd.node for nd in res_nds]
        else:
            # 返回场景中所有对象
            return all_nodes if package else [nd.node for nd in all_nodes]


def selected(outliner=True, cl=False, package=True):
    """
    获取当前所选择的节点
    :param outliner: 是否是大纲中进行选择
    :param cl: clear 清空当前选择
    :param package:
    :return:
    """
    if outliner:
        if cl:
            l_util.select_nothing()
            return []
        else:
            return [UNode(nd) for nd in l_util.get_selected_level_actors()] \
                if package else l_util.get_selected_level_actors()
    else:
        return [ANode(nd) for nd in e_util.get_selected_assets()] if package else e_util.get_selected_assets()


def listDir(source_dir, recursive=True):
    return a_util.list_assets(source_dir, recursive=recursive)


def remove_unuse_asset():
    """
    移除未使用的资产
    :return:
    """
    pass


def createNode(node_type, node_name=None, parent=None, package=True):
    """
    创建 node
    :param node_type:
    :param node_name:
    :param parent: <clarisseNode>
    :param package:
    :return:
    """
    pass


def listMethod(nd, r_name='', show_help=False):
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


def debug_function():
    """
    用于调试代码的函数
    :return:
    """
    print("debug_function exec!!!")
    # path = sys_util.get_project_content_directory() # 返回文件夹结构的系统路径
    nd = selected(outliner=False)[0]
    # print(nd.node_asset)
    # listMethod(unreal.FilePath)
    # listMethod(nd.node)
    unreal.log(nd.node.get_name())

    # unreal.log(dp.convert_relative_path_to_full(nd.node_path))


    # unreal.log(a_util.list_assets(node_path, recursive=False))
    # if nd:
    #     unreal.log(nd.node_path)
    #     nd_data = unreal.AssetData(nd.node_path)
    #     unreal.log(nd_data)

    # cbd = unreal.ContentBrowserDataSubsystem()
    # ds = cbd.get_active_data_sources()


    # print(a_util.does_directory_exist('/Game/VirtualProduction/testLevel'))
    # listMethod(unreal, 'main')
    # print(type(nd))

    # l_util.load_level("/Game/")
    # bp_node = a_util.load_blueprint_class(nd.node_path)
    # a_util.save_loaded_assets()
    # l_util.spawn_actor_from_class(bp_node,unreal.Vector(),unreal.Rotator())
    # nd ='/Game/VitrualProduction/testLevel.testLevel'
    # l_util.load_level(nd)
    # nd = l_util.get_selected_level_actors()[0]
    # nd = l_util.get_actor_reference(l_util.get_selected_level_actors()[0])

    # unreal.log(nd.get_class().get_name())
    # listMethod(nd.get_class())

    pass


def add_vp_setting(root_path='/Game/VirtualProduction'):
    """
    添加虚拟拍摄相关的 设置
    :return:
    """

    # unreal.log(sys_util.convert_to_relative_path(root_path))
    # TODO 添加节点
    # a_util.load_blueprint_class(root_path + '/Ndisplay/IncameraSettings.IncameraSettings')
    # a_util.load_blueprint_class(root_path + '/Ndisplay/IncameraStageSettings.IncameraStageSettings')
    # a_util.load_blueprint_class(root_path + '/Ndisplay/SamplePawn.SamplePawn')
    # a_util.load_blueprint_class(root_path + '/Ndisplay/StageOrigin.StageOrigin')
    # a_util.load_blueprint_class(root_path + '/Ndisplay/WarpMonitor.WarpMonitor')

    print("add virtual production.")

    # TODO 设置节点关联关系
    # TODO 设置节点属性

    pass
