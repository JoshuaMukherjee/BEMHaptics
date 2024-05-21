import bpy
import random
import mathutils

bpy.ops.wm.open_mainfile(filepath="hand.blend")


# bpy.ops.object.select_all(action='DESELECT')
# bpy.data.objects['Hand'].select_set(True)
# bpy.context.view_layer.objects.active = bpy.data.objects['Hand']
# hand = bpy.data.objects['Hand']
skeleton = bpy.data.objects['Skeleton']
# bpy.ops.object.mode_set(mode='EDIT')

# print(type(skeleton))
# print(type(skeleton.pose))
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
]

positions =[[mathutils.Vector(h), mathutils.Vector(t)] for h,t in positions]




bpy.ops.object.mode_set(mode='POSE')

# Set the head and tail positions for each bone
for i, bone in enumerate(bpy.context.object.pose.bones):
    print(bone)
    if i < len(positions):
        head_pos, tail_pos = positions[i]
        bone_head = bone.bone.head_local.copy()
        bone_tail = bone.bone.tail_local.copy()
        
        # Calculate the difference and apply it to the bone's location
        bone.location += head_pos - bone_head
        bone.location += tail_pos - bone_tail


bpy.ops.object.mode_set(mode='OBJECT')

hand_obj = bpy.data.objects['Hand']
bpy.context.view_layer.objects.active = hand_obj


bpy.ops.object.select_all(action='DESELECT')
hand_obj.select_set(True)
bpy.context.view_layer.objects.active = hand_obj

bpy.ops.object.modifier_apply(modifier="Armature")



# Export the posed mesh as STL

# skeleton.select_set(True)
bpy.ops.export_mesh.stl(filepath='Media/exports/mesh.stl')

# v = m.vertices[0]


