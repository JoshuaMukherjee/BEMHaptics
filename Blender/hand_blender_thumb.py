import bpy
import math
import mathutils # type: ignore

bpy.ops.wm.open_mainfile(filepath="hand.blend")


# bpy.ops.object.select_all(action='DESELECT')
# bpy.data.objects['Hand'].select_set(True)
# bpy.context.view_layer.objects.active = bpy.data.objects['Hand']
# hand = bpy.data.objects['Hand']
skeleton = bpy.data.objects['Skeleton']
# bpy.ops.object.mode_set(mode='EDIT')

# print(type(skeleton))
# print(typpe(skeleton.pose))
# for b in skeleton.data.edit_bones:
#     b.head.x += 10
#     print(b.head)

# bpy.ops.object.mode_set(mode='OBJECT')



bpy.data.objects['Skeleton'].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects['Skeleton']


positions = [
    ((0.1, 0.2, 0.3), (0, 0.3, 0)),
    ((0.4, 0.5, 0.6), (0.5, 0.6, 0.7)),
    ((-0.1, -0.2, -0.3), (0.0, 0.0, 0.0))
],

positions =[[mathutils.Vector(h), mathutils.Vector(t)] for h,t in positions]




bpy.ops.object.mode_set(mode='POSE')

# Set the head and tail positions for each bone
bones= bpy.context.object.pose.bones
for t in bones: 
    t.rotation_euler = ([0,0,math.radians(90)])
bpy.ops.object.mode_set(mode='OBJECT')

hand_obj = bpy.data.objects['Hand']
bpy.context.view_layer.objects.active = hand_obj


bpy.ops.object.select_all(action='DESELECT')
hand_obj.select_set(True)
bpy.context.view_layer.objects.active = hand_obj

bpy.ops.object.modifier_apply(modifier="Armature")



# Export the posed mesh as STL

# skeleton.select_set(True)
bpy.ops.export_mesh.stl(filepath='Media/exports/mesh_Thumb.stl')

# v = m.vertices[0]


