#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import unreal
# import unreal_until as util

# def cout(obj):
#     unreal.log(obj)



# e_util = unreal.EditorUtilityLibrary()
# a_util = unreal.EditorAssetLibrary()
# str_util = unreal.StringLibrary()
# sys_util = unreal.SystemLibrary()
# l_util = unreal.EditorLevelLibrary()


# menus = unreal.ToolMenus.get()
# main_menu = menus.find_menu("LevelEditor.MainMenu")


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

import socket

localIP = "127.0.0.1"

localPort = 6308

bufferSize = 11

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while (True):
    print('rev')
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)