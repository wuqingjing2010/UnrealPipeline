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







# 用于获取 content browser 中的选择对象
# print(unreal.EditorUtilityLibrary.get_selected_assets())


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
