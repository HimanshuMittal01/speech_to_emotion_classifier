'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 30-07-2022 10:59:09
'''

import bpy
import json

# Import config
with open("config.json", "r") as f:
    config = json.load(f)

# Load fbx
bpy.ops.import_scene.fbx(filepath=config["fbx_model_file"])
    
# Selecting the head
obj = bpy.data.objects[config["fbx_model_name"]]
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Read emotion output
with open(config["output_json_file"], "r") as f:
    emotion = json.load(f)

# Set blendshapes
bpy.data.shape_keys['Key'].key_blocks["CH"].value = emotion["calm"]
bpy.data.shape_keys['Key'].key_blocks["smile"].value = emotion["happy"]
bpy.data.shape_keys['Key'].key_blocks["frown"].value = emotion["sad"]
bpy.data.shape_keys['Key'].key_blocks["Puff"].value = emotion["angry"]
bpy.data.shape_keys['Key'].key_blocks["AA"].value = emotion["fearful"]
bpy.data.shape_keys['Key'].key_blocks["Sneer"].value = emotion["disgust"]
bpy.data.shape_keys['Key'].key_blocks["BrowsU_C"].value = emotion["surprised"]

# Save fbx
bpy.ops.wm.save_as_mainfile(filepath=config["output_blend_file"], filter_blender=False)
