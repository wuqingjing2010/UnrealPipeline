#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unreal
from MPath import MPath
from unrealLib import ANode,UNode


e_util = unreal.EditorUtilityLibrary()
a_util = unreal.EditorAssetLibrary()
str_util = unreal.StringLibrary()
sys_util = unreal.SystemLibrary()
l_util = unreal.EditorLevelLibrary()


def show_message(message, level='log', window=False):
    '''
    显示消息的方式 默认两种方式 第一种 在outlog 中打印log 其中logo分三个 级别  对应 log warning error
    第二种方式弹窗的方式 进行显示， 分两种 第一种 只弹确认窗口，第二种弹出 确认与否 窗口 其中 log 方式为 确认窗口，以外为确认与否窗口
    TODO 后续需要添加窗口方式显示
    :param message:  需要显示的内容
    :param level: 级别  log warning error 三种
    :param window: 是否开启窗口告知
    :return:
    '''
    if level == 'log':
        unreal.log(message)
    elif level=='warning':
        unreal.log_warning(message)
    elif level=='error':
        unreal.log_error(message)
    else:
        unreal.log(message)

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

