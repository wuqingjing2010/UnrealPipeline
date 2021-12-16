import unreal
import json
e_util = unreal.EditorUtilityLibrary()
a_util = unreal.EditorAssetLibrary()
str_util = unreal.StringLibrary()
sys_util = unreal.SystemLibrary()
l_util = unreal.EditorLevelLibrary()




result_dict = {}
actors = l_util.get_selected_level_actors()
# des = unreal.DataLayerEditorSubsystem()
layers = []
for act in actors:
    act_type = type(act)

    # actor_data_layers = act.get_editor_property('data_layers')
    # layer_names = [str(des.get_data_layer(layer).get_data_layer_label()) for layer in actor_data_layers]

    if act_type == unreal.PackedLevelInstance:
        id_name = act.get_name()
        asset_path = act.get_class().get_full_name().split(' ')[-1]
        asset_type = "PackedLevelInstance"
    elif act_type == unreal.StaticMeshActor:
        id_name = act.get_name()
        act_component = act.static_mesh_component
        asset_path = act_component.static_mesh.get_full_name().split(' ')[-1]
        asset_type = "StaticMeshActor"
    else:
        continue
    actor_folder_path = str(act.get_folder_path())
    # print(asset_path)
    # print(actor_folder_path)
    location = act.get_actor_location()
    tx = location.x
    ty = location.y
    tz = location.z
    rotation = act.get_actor_rotation()
    pitch = rotation.pitch
    yaw = rotation.yaw
    roll = rotation.roll
    scale = act.get_actor_scale3d()
    sx = scale.x
    sy = scale.y
    sz = scale.z
    result_dict [id_name] = [
        asset_path,
        asset_type,
        actor_folder_path,
        [tx,ty,tz],[pitch,yaw,roll],[sx,sy,sz]
    ]


json_path = "d:/actor_list_dark.json"
with open(json_path, 'w') as f:
    json.dump(result_dict, f, indent=4)

    # print(act.get_actor_rotation())
    # print(act.get_actor_scale3d())



import unreal
import json
e_util = unreal.EditorUtilityLibrary()
a_util = unreal.EditorAssetLibrary()
str_util = unreal.StringLibrary()
sys_util = unreal.SystemLibrary()
l_util = unreal.EditorLevelLibrary()



json_path = "d:/actor_list_dark.json"
with open(json_path) as f:
    data = json.load(f)


des = unreal.DataLayerEditorSubsystem()
# layer_names = ['Campfire Replace','Campfire Geometry','Dark World']
# [des.rename_data_layer(des.create_data_layer(),name) for name in layer_names]


for key,value in data.items():
    asset_type = value[1]
    asset_path = value[0]
    folder_path = value[2]
    data_layers = value[-1]
    location = unreal.Vector(x=value[3][0],y=value[3][1],z=value[3][2])
    rotation = unreal.Rotator(pitch=value[4][0],roll=value[4][2],yaw=value[4][1])
    scale = unreal.Vector(x=value[5][0],y=value[5][1],z=value[5][2])
    asset_node = a_util.load_asset(asset_path)
    actor_node = l_util.spawn_actor_from_object(asset_node, location, rotation)
    actor_node.set_actor_scale3d(scale)

    actor_node.set_folder_path(folder_path)













