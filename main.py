#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unreal
# import unreal_until as util
#

def cout(obj):
    unreal.log(obj)

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



eUtil = unreal.EditorUtilityLibrary()
aUtil = unreal.EditorAssetLibrary()
strUtil = unreal.StringLibrary()
sysUtil = unreal.SystemLibrary()
lUtil = unreal.EditorLevelLibrary()



def mainTest():
    import importlib,os
    # unreal.EditorUtilityLibrary.get_selected_assets()
    # nd = eUtil.get_selected_assets()[0]

    # sel = unreal.AssetData('/Game/codeTest/NewAjaMediaOutput.NewAjaMediaOutput')
    # nd = aUtil.load_asset('/Game/codeTest/tttt.tttt')

    # listMethod(sel)

    # import MPath as MPath
    # importlib.reload(MPath)

    # mp = MPath.MPath(sel)
    # print(mp.parent.child('test'))
    # for f in mp.listdir():
    #     print(f.base_name)
    #

    import unrealUntil as uutil,importlib
    importlib.reload(uutil)
    sel = uutil.ls(outliner=False,sl=True)[0]
    print(sel.node_type)
    print(sel.node_path)
    print(sel.node_directory)
    parent_node = sel.parent
    fd = parent_node.node.makedir('wqj')
    # TODO 这里需要排查 改名后删除 为什么 node_path 还是之前名称，是不是因为该原因导致删除不掉
    fd.rename('qqqq')
    print(fd.node_path)
    fd.delete()

# 获取当前打开得 level
# lUtil.get_editor_world()

# 用于获取 content browser 中的选择对象
# eUtil.get_selected_assets()   # 目前发现 folder 没法获取选中

# 用于获取 world outline 中的选择对象
# lUtil.get_selected_level_actors() # 目前发现 大纲中 的folder 无法判断是否选中



# sel = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
# print(sel.get_actor_reference())
# world = unreal.World()
# world = unreal.EditorLevelLibrary.get_editor_world()
# util.listMethod(unreal.SystemLibrary,"actor_spawn")

# cone2 = world.actor_spawn(unreal.StaticMeshActor)
# cone2.StaticMeshComponent.StaticMesh = unreal.load_object(unreal.StaticMesh, '/Engine/BasicShapes/Cone')
# cone2.set_actor_label('A Better Cone')

# assets = e_util.get_selected_assets()
# for ass in assets:
#     # unreal.log(ass.get_path_name())
#     # unreal.log(ass.get_fname())
#     # # unreal.log(ass.get_display_name())
#     # unreal.log(ass.get_name())
#     cls = ass.get_class()
#     cout(ass.get_path_name())
#     cout(cls.get_name())
#
#
