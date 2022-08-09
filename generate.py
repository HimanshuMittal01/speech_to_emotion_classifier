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
    output = json.load(f)

# Get meaningful format
emotions_list = ["neutral","calm","happy","sad","angry","fearful","disgust","surprised"]
id2emotions = {}
idx = 0
for emotion in emotions_list:
    id2emotions[idx] = "female_"+emotion
    id2emotions[idx+1] = "male_"+emotion
    idx += 2

# Set blendshapes
for time, values in output.items():
    # TODO: animation using different timestamps
    bpy.data.shape_keys['Key'].key_blocks["CH"].value = values[3]
    bpy.data.shape_keys['Key'].key_blocks["smile"].value = values[5]
    bpy.data.shape_keys['Key'].key_blocks["frown"].value = values[7]
    bpy.data.shape_keys['Key'].key_blocks["Puff"].value = values[9]
    bpy.data.shape_keys['Key'].key_blocks["AA"].value = values[11]
    bpy.data.shape_keys['Key'].key_blocks["Sneer"].value = values[13]
    bpy.data.shape_keys['Key'].key_blocks["BrowsU_C"].value = values[15]

# Save fbx
bpy.ops.wm.save_as_mainfile(filepath=config["output_blend_file"], filter_blender=False)
