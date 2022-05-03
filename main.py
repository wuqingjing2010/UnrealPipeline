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
    import unrealUntil as uutil
    from MPath import MPath
    importlib.reload(uutil)
    sel = lUtil.get_selected_level_actors()[0]
    # listMethod(sel[0])
    print(type(sel))

    # print(sel.get_folder_path()) ## 大纲中的文件夹层级结构
    # print(sel.get_full_name()) ## level 中的文件层级结构 包括类型名称
    # print(sel.get_path_name()) ## level 中的文件层级结构

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
