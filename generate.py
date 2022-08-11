'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 30-07-2022 10:59:09
'''

import bpy
import json
import random

# Import config
with open("config.json", "r") as f:
    config = json.load(f)

# Load fbx
bpy.ops.import_scene.fbx(filepath=config["fbx_model_file"])

# Selecting the head
obj_base_name = "Head"
base_obj = bpy.data.objects[obj_base_name]
base_obj.select_set(True)
bpy.context.view_layer.objects.active = base_obj

# Duplicate faces
face_objs = [base_obj]
num_faces = 12
num_faces_in_row = 4
xz_mean_gap = 0.35
assert(num_faces<1000)
for i in range(1,num_faces):
    bpy.ops.object.duplicate(linked=False)
    obj_name = obj_base_name+"."+"0"*(3-len(str(i)))+str(i)
    obj = bpy.data.objects[obj_name]
    face_objs.append(obj)

# Position them
for i, obj in enumerate(face_objs):
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    pos_z, pos_x = i//num_faces_in_row, i%num_faces_in_row
    obj.location.z -= xz_mean_gap*pos_z + (random.random()-0.5)*0.1
    obj.location.x += xz_mean_gap*pos_x + (random.random()-0.5)*0.1

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
random_jitter = lambda x: random.random()%(2*x) - x
clip_01 = lambda x: max(0, min(1, x))
keyshape_mapping = {"CH":3,"smile":5,"frown":7,"Puff":9,"AA":11,"Sneer":13,"BrowsU_C":15}

for time, values in output.items():
    for i, obj in enumerate(face_objs):
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        key_name = "Key"
        if i!=0:
            key_name = key_name+"."+"0"*(3-len(str(i)))+str(i)
        
        for keyshape, labelid in keyshape_mapping.items():
            bpy.data.shape_keys[key_name].key_blocks[keyshape].value = clip_01(values[labelid] + random_jitter(0.2))
            obj.data.shape_keys.key_blocks[keyshape].keyframe_insert('value', frame=int(time)*12+1)

        bpy.ops.object.select_all(action="DESELECT")

# Save fbx
bpy.ops.wm.save_as_mainfile(filepath=config["output_blend_file"], filter_blender=False)
