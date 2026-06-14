import bpy
import random
import math

# =========================
# PARAMETRY PROJEKTU
# =========================

LICZBA_KLATEK = 150
FPS = 25

INTENSYWNOSC_DESZCZU = 90
PREDKOSC_SAMOCHODOW = 1.0
CZESTOTLIWOSC_MIGOTANIA = 12

SEED = 42


def ustaw_timeline():
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = LICZBA_KLATEK
    bpy.context.scene.render.fps = FPS


def wyczysc_kolekcje(nazwa):
    kolekcja = bpy.data.collections.get(nazwa)
    if kolekcja:
        for obj in list(kolekcja.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        kolekcja = bpy.data.collections.new(nazwa)
        bpy.context.scene.collection.children.link(kolekcja)
    return kolekcja


def material_emission(nazwa, kolor, sila):
    mat = bpy.data.materials.get(nazwa) or bpy.data.materials.new(nazwa)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = kolor
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = sila
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = kolor

    return mat


def generuj_deszcz():
    random.seed(SEED)
    kolekcja = wyczysc_kolekcje("Rain_Generated")
    mat = material_emission("Rain_Material", (0.55, 0.75, 1.0, 1.0), 0.8)

    for i in range(INTENSYWNOSC_DESZCZU):
        x = random.uniform(-5.0, 5.0)
        y = random.uniform(-16.0, 12.0)
        z = random.uniform(2.0, 7.0)

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6,
            radius=0.012,
            depth=0.45,
            location=(x, y, z),
            rotation=(math.radians(8), 0, 0)
        )

        drop = bpy.context.object
        drop.name = f"Rain_Drop_{i:03d}"
        drop.data.materials.append(mat)

        for c in drop.users_collection:
            c.objects.unlink(drop)
        kolekcja.objects.link(drop)

        start = random.randint(1, 30)
        end = min(start + random.randint(35, 70), LICZBA_KLATEK)

        drop.location.z = z
        drop.keyframe_insert(data_path="location", frame=start)

        drop.location.z = -0.1
        drop.location.y += random.uniform(-0.5, 0.5)
        drop.keyframe_insert(data_path="location", frame=end)


def animuj_neony():
    random.seed(SEED + 10)

    for obj in bpy.data.objects:
        if obj.name.lower().startswith("neon"):
            mat = obj.active_material
            if not mat or not mat.use_nodes:
                continue

            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if not bsdf or "Emission Strength" not in bsdf.inputs:
                continue

            strength = bsdf.inputs["Emission Strength"]

            for frame in range(1, LICZBA_KLATEK + 1, CZESTOTLIWOSC_MIGOTANIA):
                value = random.choice([1.2, 2.5, 4.0, 6.0])
                strength.default_value = value
                strength.keyframe_insert(data_path="default_value", frame=frame)


def main():
    ustaw_timeline()
    animuj_neony()
    generuj_deszcz()


if __name__ == "__main__":
    main()