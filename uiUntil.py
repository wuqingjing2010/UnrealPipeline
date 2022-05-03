#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unreal
print('uiUntil file exec!!!')
menus =  unreal.ToolMenus.get()
rootMenuName = 'LevelEditor.MainMenu'
rootToolBarName = "LevelEditor.LevelEditorToolBar"

def addMainMenu(name,label,tool_tip=""):
    '''
    为 unreal 添加主菜单
    :param name: 主菜单名称
    :param label:  主菜单 label
    :param tool_tip:  显示 toolTip
    :return:
    '''
    # Get the main menu class
    menu = menus.find_menu(rootMenuName)
    custom_menu_name = rootMenuName + '.' + name
    custom_menu = menus.find_menu(custom_menu_name)
    if custom_menu == None:
        # Custom menu parameters
        owner = menu.get_name()
        section_name = 'PythonTools'
        # Add and refresh
        menu.add_sub_menu(owner, section_name, name, label, tool_tip)
        menus.refresh_all_widgets()
        unreal.log('{} menu add succesful.'.format(name))
    else:
        unreal.log_warning('{} menu is exists.'.format(name))

def addSubMenu(main_menu,sub_menu,string_commond,tool_tip=''):
    '''
    添加子菜单命令
    :param main_menu: 父菜单路径
    :param sub_menu:  子菜单名称
    :param string_commond: 具体执行的命令
    :param tool_tip: 帮助信息
    :return:
    '''
    main_menu_name = rootMenuName + '.' + main_menu
    menu = menus.find_menu(main_menu_name)
    if menu == None:
        unreal.log_error('{} main menu is not exists.'.format(main_menu))
        return
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.MENU_ENTRY)
    entry.set_label(sub_menu)
    typ = unreal.ToolMenuStringCommandType.PYTHON
    entry.set_string_command(typ, "", string_commond)
    section_name = ''
    menu.add_menu_entry(section_name, entry)
    if tool_tip:
        entry.set_tool_tip(tool_tip)
    menus.refresh_all_widgets()

def removeMenu():
    '''
    TODO 是否存在移除得命令
    :return:
    '''
    pass

def addToolShelf(toolName,string_commond):
    menu = menus.find_menu(rootToolBarName)
    # Set the button type and label
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(toolName)
    # Set button command
    typ = unreal.ToolMenuStringCommandType.PYTHON
    entry.set_string_command(typ, "", string_commond)
    # Add and refresh
    section_name = 'Settings'
    menu.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()


def addIqiyiUI():
    addMainMenu('IQIYI', 'IQIYI')
    #TODO 后续添加其他工具、子菜单、或者按钮
    addSubMenu('IQIYI','mainTest','import main as main,importlib\nimportlib.reload(main)\nmain.mainTest()')




