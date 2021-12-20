# UnrealPipeline

使用说明：
1. 克隆代码到对应工程目录的 /content/Python
2. 在/content/Python 路径下创建 init_unreal.py 文件
3. init_unreal.py 文件中 写入 import UnrealPipeline 
4. 启动工程即可。


结构说明：
UE项目启动后默认会执行 init_unreal.py 在init_unreal 中会执行 UnrealPipeline 模块的init 添加菜单。

uiUntil.py 中定义关于 ue界面上的操作。 例如添加菜单，添加子菜单，添加按钮等等。
unrealUntil.py 中定义快速便捷的操作。 操作函数使用方式参考maya 默认的 pymel 的操作模式。 
unrealLib.py 中封装了默认UE的 asset对象以及 actor对象。将使用方式从UE 原生的操作函数面向过程的模式，转变为面向对象的OOP模式。  
vpUntil.py 中存放虚拟拍摄中通用的批处理执行函数
MPath.py 中封装了路径的操作方式 将路径操作函数的面向过程的模式，转变为面向对象的OOP模式。


