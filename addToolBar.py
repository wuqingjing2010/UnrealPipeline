import unreal
from collections import namedtuple

def make_menu(lable_name,command_string):
    """
    创建menu菜单目录
    :param lable_name:
    :param command_string:
    :return:
    """
    # menu_stru = namedtuple("menu_name",["entry","commond_string"])
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(lable_name)
    typ = unreal.ToolMenuStringCommandType.PYTHON
    entry.set_string_command(typ,'',command_string)
    return entry

def add_tool_button(function_str,section_name):
    """
    添加工具按钮到工具架上
    :param function_str:
    :param section_name:
    :return:
    """
    # print("add tool button")
    menus = unreal.ToolMenus.get()
    menu = menus.find_menu("LevelEditor.LevelEditorToolBar")
    menu_entry = make_menu(section_name,function_str)
    menu.add_menu_entry('Settings',menu_entry)
    menus.refresh_all_widgets()

def remove_tool_button(section_name):
    """
    移除指定的 button
    :param section_name:s
    :return:
    """
    menus = unreal.ToolMenu.get()
    menu = menus.find_menu("LevelEditor.LevelEditorToolBar")

    pass

#
# # Get the menu class
# menus = unreal.ToolMenus.get()
# menu_name = "LevelEditor.LevelEditorToolBar"
# menu = menus.find_menu(menu_name)
# # Set the button type and label
# entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
# entry.set_label("Test Button")
# # Set button command
# typ = unreal.ToolMenuStringCommandType.PYTHON
# entry.set_string_command(typ, "", 'print "Hello World!"')
# # Add and refresh
# section_name = 'Settings'
# menu.add_menu_entry(section_name, entry)
# menus.refresh_all_widgets()