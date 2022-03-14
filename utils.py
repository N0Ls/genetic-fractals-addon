import bpy


def find_instance(fn, objs):
    all_matches = list(filter(fn, objs))
    return len(all_matches) > 0 and all_matches[0]


def traverse_layer_collection(layer_collection, name_to_found):
    found = None
    if (layer_collection.name == name_to_found):
        return layer_collection
    for layer in layer_collection.children:
        found = traverse_layer_collection(layer, name_to_found)
        if found:
            return found


def add_uv_sphere(collection):
    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)


def add_cube(collection):
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)


def add_cone(collection):
    bpy.ops.mesh.primitive_cone_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)


def reset_float_properties(context):
    context.scene.fractal_1_like = 0.00
    context.scene.fractal_2_like = 0.00
    context.scene.fractal_3_like = 0.00
    context.scene.fractal_4_like = 0.00


def binaryToDecimal(val):
    return int(val, 2)


def binaryToDecimalStr(val):
    return str(int(val, 2))


def binary_to_modifier(mod, str):
    mod['Input_1'] = binaryToDecimal(str[0:8])
    mod['Input_2'] = binaryToDecimal(str[8:16])
    mod['Input_3'] = binaryToDecimal(str[16:24])
    mod['Input_4'] = binaryToDecimal(str[24:32])

    mod['Input_5'][0] = binaryToDecimal(str[32:41])
    mod['Input_5'][1] = binaryToDecimal(str[41:50])
    mod['Input_5'][2] = binaryToDecimal(str[50:59])

    mod['Input_6'][0] = binaryToDecimal(str[59:68])
    mod['Input_6'][1] = binaryToDecimal(str[68:77])
    mod['Input_6'][2] = binaryToDecimal(str[77:86])

    mod['Input_7'][0] = binaryToDecimal(str[86:95])
    mod['Input_7'][1] = binaryToDecimal(str[95:104])
    mod['Input_7'][2] = binaryToDecimal(str[104:113])

    mod['Input_8'][0] = binaryToDecimal(str[113:122])
    mod['Input_8'][1] = binaryToDecimal(str[122:131])
    mod['Input_8'][2] = binaryToDecimal(str[131:140])

    mod['Input_9'] = float(binaryToDecimalStr(str[140:142]) + "." + binaryToDecimalStr(
        str[142:146])+binaryToDecimalStr(str[146:150]))
    mod['Input_10'] = float(binaryToDecimalStr(str[150:152]) + "." + binaryToDecimalStr(
        str[152:156])+binaryToDecimalStr(str[156:160]))
    mod['Input_11'] = float(binaryToDecimalStr(str[160:162]) + "." + binaryToDecimalStr(
        str[162:166])+binaryToDecimalStr(str[166:170]))
    mod['Input_12'] = float(binaryToDecimalStr(str[170:172]) + "." + binaryToDecimalStr(
        str[172:176])+binaryToDecimalStr(str[176:180]))

    mod['Input_13'][0] = float(binaryToDecimalStr(str[180:182]) + "." + binaryToDecimalStr(
        str[182:186])+binaryToDecimalStr(str[186:190]))
    mod['Input_13'][1] = float(binaryToDecimalStr(str[190:192]) + "." + binaryToDecimalStr(
        str[192:196])+binaryToDecimalStr(str[196:200]))
    mod['Input_13'][2] = float(binaryToDecimalStr(str[200:202]) + "." + binaryToDecimalStr(
        str[202:206])+binaryToDecimalStr(str[206:210]))

    # To update view
    mod.show_render = False
    mod.show_render = True
    mod.show_viewport = False
    mod.show_viewport = True


def modifier_to_binary(mod):
    mod_str_binary = ''
    # print("Input 1 is " + bin(mod['Input_1']))
    # # print("Test with 8 leading 0 " + "{0:b}".format(mod['Input_1']))
    # print("Test with 8 leading 0 " + "{:08b}".format(mod['Input_1']))

    # Object indexes
    mod_str_binary += "{:08b}".format(mod['Input_1'])
    mod_str_binary += "{:08b}".format(mod['Input_2'])
    mod_str_binary += "{:08b}".format(mod['Input_3'])
    mod_str_binary += "{:08b}".format(mod['Input_4'])

    # Rotation 1

    mod_str_binary += "{:09b}".format(int(mod['Input_5'][0]))
    mod_str_binary += "{:09b}".format(int(mod['Input_5'][1]))
    mod_str_binary += "{:09b}".format(int(mod['Input_5'][2]))

    # Rotation 2
    mod_str_binary += "{:09b}".format(int(mod['Input_6'][0]))
    mod_str_binary += "{:09b}".format(int(mod['Input_6'][1]))
    mod_str_binary += "{:09b}".format(int(mod['Input_6'][2]))

    # Rotation 3
    mod_str_binary += "{:09b}".format(int(mod['Input_7'][0]))
    mod_str_binary += "{:09b}".format(int(mod['Input_7'][1]))
    mod_str_binary += "{:09b}".format(int(mod['Input_7'][2]))

    # Rotation 4
    mod_str_binary += "{:09b}".format(int(mod['Input_8'][0]))
    mod_str_binary += "{:09b}".format(int(mod['Input_8'][1]))
    mod_str_binary += "{:09b}".format(int(mod['Input_8'][2]))

    # Scale 1
    scale1 = '{:.2f}'.format(round(mod['Input_9'], 2))

    scale1_destructured = [scale1[0], scale1[2], scale1[3]]
    mod_str_binary += "{:02b}".format(int(scale1_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scale1_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scale1_destructured[2]))

    # Scale 2
    scale2 = '{:.2f}'.format(round(mod['Input_10'], 2))

    scale2_destructured = [scale2[0], scale2[2], scale2[3]]
    mod_str_binary += "{:02b}".format(int(scale2_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scale2_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scale2_destructured[2]))

    # Scale 3
    scale3 = '{:.2f}'.format(round(mod['Input_11'], 2))

    scale3_destructured = [scale3[0], scale3[2], scale3[3]]
    mod_str_binary += "{:02b}".format(int(scale3_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scale3_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scale3_destructured[2]))

    # Scale 4
    scale4 = '{:.2f}'.format(round(mod['Input_12'], 2))
    scale4_destructured = [scale4[0], scale4[2], scale4[3]]
    mod_str_binary += "{:02b}".format(int(scale4_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scale4_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scale4_destructured[2]))

    # Scale Origin
    scaleOriginX = '{:.2f}'.format(round(mod['Input_13'][0], 2))
    scaleOriginY = '{:.2f}'.format(round(mod['Input_13'][1], 2))
    scaleOriginZ = '{:.2f}'.format(round(mod['Input_13'][2], 2))

    scaleOriginX_destructured = [
        scaleOriginX[0], scaleOriginX[2], scaleOriginX[3]]
    mod_str_binary += "{:02b}".format(int(scaleOriginX_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scaleOriginX_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scaleOriginX_destructured[2]))

    scaleOriginY_destructured = [
        scaleOriginY[0], scaleOriginY[2], scaleOriginY[3]]
    mod_str_binary += "{:02b}".format(int(scaleOriginY_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scaleOriginY_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scaleOriginY_destructured[2]))

    scaleOriginZ_destructured = [
        scaleOriginZ[0], scaleOriginZ[2], scaleOriginZ[3]]
    mod_str_binary += "{:02b}".format(int(scaleOriginZ_destructured[0]))
    mod_str_binary += "{:04b}".format(int(scaleOriginZ_destructured[1]))
    mod_str_binary += "{:04b}".format(int(scaleOriginZ_destructured[2]))

    return mod_str_binary


def register():
    pass


def unregister():
    pass
