import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.cameras:
        if block.users == 0:
            bpy.data.cameras.remove(block)
    for block in bpy.data.lights:
        if block.users == 0:
            bpy.data.lights.remove(block)

def make_material(name, base_color=(1, 1, 1, 1), metallic=0.0, roughness=0.5,
                  emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

    if emission_color is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission_color

    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emission_strength

    return mat


def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def add_bevel(obj, width=0.03, segments=2):
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = width
    bevel.segments = segments


def smooth_object(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except:
        pass
    obj.select_set(False)

def create_ground():
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Podloze"

    mat_ground = make_material(
        "Mat_Podloze",
        base_color=(0.14, 0.14, 0.16, 1.0),
        metallic=0.15,
        roughness=0.90
    )
    assign_material(ground, mat_ground)
    return ground


def setup_world():
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.42, 0.44, 0.50, 1.0)
    bg.inputs[1].default_value = 0.9


def setup_light():
    bpy.ops.object.light_add(type='SUN', location=(6, -6, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.rotation_euler = (math.radians(48), math.radians(0), math.radians(32))
    sun.data.energy = 4.5

    bpy.ops.object.light_add(type='POINT', location=(1.5, -4.5, 4.0))
    point = bpy.context.active_object
    point.name = "PointLight"
    point.data.energy = 900
    point.data.shadow_soft_size = 1.5

    return sun, point


def setup_camera():
    bpy.ops.object.camera_add(location=(8.7, -11.2, 5.8))
    cam = bpy.context.active_object
    cam.name = "Camera"
    cam.rotation_euler = (math.radians(75), 0, math.radians(30))
    bpy.context.scene.camera = cam
    return cam


def setup_render(output_name="lab04_rosliny.png"):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    scene.render.image_settings.file_format = 'PNG'

    scene.render.filepath = "//" + output_name

    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 64
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = True

def stworz_lodyge(x_offset, y_offset, wysokosc, mat_lodyga):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.22,
        depth=wysokosc,
        location=(x_offset, y_offset, wysokosc / 2.0)
    )
    stem = bpy.context.active_object
    stem.name = f"Lodyga_{x_offset:.1f}"

    assign_material(stem, mat_lodyga)
    smooth_object(stem)

    return stem


def stworz_liscie(x_offset, y_offset, wysokosc, liczba_lisci, promien_lisci, mat_lisc):
    leaves = []

    if liczba_lisci < 1:
        return leaves

    for i in range(liczba_lisci):
        angle = (2 * math.pi * i) / liczba_lisci

        radius_from_center = 0.38 + promien_lisci * 0.38
        x = x_offset + math.cos(angle) * radius_from_center
        y = y_offset + math.sin(angle) * radius_from_center

        z = wysokosc * (0.50 + 0.09 * i)

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        leaf = bpy.context.active_object
        leaf.name = f"Lisc_{x_offset:.1f}_{i+1}"

        leaf.scale = (
            promien_lisci * 1.45,
            promien_lisci * 0.20,
            promien_lisci * 0.55
        )

        leaf.rotation_euler = (
            math.radians(14 + i * 4),
            math.radians(42 + i * 3),
            angle + math.radians(10)
        )

        add_bevel(leaf, width=0.025, segments=2)
        assign_material(leaf, mat_lisc)

        leaves.append(leaf)

    return leaves


def stworz_korzenie(x_offset, y_offset, liczba_korzeni, mat_korzen):
    roots = []

    if liczba_korzeni < 1:
        return roots

    for i in range(liczba_korzeni):
        angle = (2 * math.pi * i) / liczba_korzeni

        root_radius = 0.52
        x = x_offset + math.cos(angle) * root_radius
        y = y_offset + math.sin(angle) * root_radius
        z = 0.10

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        root = bpy.context.active_object
        root.name = f"Korzen_{x_offset:.1f}_{i+1}"

        root.scale = (0.36, 0.07, 0.06)
        root.rotation_euler = (
            math.radians(0),
            math.radians(12),
            angle + math.radians(8)
        )

        add_bevel(root, width=0.015, segments=2)
        assign_material(root, mat_korzen)

        roots.append(root)

    return roots

def stworz_rosline(
    x_offset=0.0,
    y_offset=0.0,
    wysokosc=2.0,
    liczba_lisci=3,
    promien_lisci=0.3,
    liczba_korzeni=4,
    mat_lodyga=None,
    mat_lisc=None,
    mat_korzen=None
):
    if mat_lodyga is None or mat_lisc is None or mat_korzen is None:
        raise ValueError("Przekaż materiały do stworz_rosline().")

    stem = stworz_lodyge(x_offset, y_offset, wysokosc, mat_lodyga)
    leaves = stworz_liscie(
        x_offset, y_offset, wysokosc,
        liczba_lisci, promien_lisci, mat_lisc
    )
    roots = stworz_korzenie(x_offset, y_offset, liczba_korzeni, mat_korzen)

    return {
        "lodyga": stem,
        "liscie": leaves,
        "korzenie": roots
    }

def main():
    clear_scene()
    setup_world()

    mat_lodyga = make_material(
        "Lodyga_Metaliczna",
        base_color=(0.42, 0.24, 0.10, 1.0),
        metallic=0.82,
        roughness=0.28
    )

    mat_lisc = make_material(
        "Lisc_Syntetyczny",
        base_color=(0.08, 0.88, 0.82, 1.0),
        metallic=0.12,
        roughness=0.18,
        emission_color=(0.12, 0.95, 0.90, 1.0),
        emission_strength=0.55
    )

    mat_korzen = make_material(
        "Korzen_Grafit",
        base_color=(0.12, 0.13, 0.16, 1.0),
        metallic=0.65,
        roughness=0.42
    )

    create_ground()
    setup_light()
    setup_camera()
    setup_render("lab04_rosliny.png")

    stworz_rosline(
        x_offset=-3.0,
        y_offset=0.0,
        wysokosc=1.6,
        liczba_lisci=3,
        promien_lisci=0.24,
        liczba_korzeni=3,
        mat_lodyga=mat_lodyga,
        mat_lisc=mat_lisc,
        mat_korzen=mat_korzen
    )

    stworz_rosline(
        x_offset=0.0,
        y_offset=0.0,
        wysokosc=2.2,
        liczba_lisci=4,
        promien_lisci=0.32,
        liczba_korzeni=4,
        mat_lodyga=mat_lodyga,
        mat_lisc=mat_lisc,
        mat_korzen=mat_korzen
    )

    stworz_rosline(
        x_offset=3.0,
        y_offset=0.0,
        wysokosc=3.0,
        liczba_lisci=5,
        promien_lisci=0.42,
        liczba_korzeni=5,
        mat_lodyga=mat_lodyga,
        mat_lisc=mat_lisc,
        mat_korzen=mat_korzen
    )

    bpy.ops.render.render(write_still=True)
    print("Gotowe. Render zapisany do:", bpy.context.scene.render.filepath)


if __name__ == "__main__":
    main()