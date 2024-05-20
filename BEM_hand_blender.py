import bpy


bpy.ops.wm.open_mainfile(filepath="hand.blend")


# bpy.ops.object.select_all(action='DESELECT')
# bpy.data.objects['Hand'].select_set(True)
# bpy.context.view_layer.objects.active = bpy.data.objects['Hand']
# hand = bpy.data.objects['Hand']
skeleton = bpy.data.objects['Skeleton']
bpy.ops.object.mode_set(mode='EDIT')

print(type(skeleton))
print(type(skeleton.pose))
for b in skeleton.data.edit_bones:
    b.head.x += 10
    print(b.head)

bpy.ops.object.mode_set(mode='OBJECT')



skeleton.select_set(True)
bpy.ops.export_mesh.stl(filepath='Media/exports/mesh.stl')

# v = m.vertices[0]


