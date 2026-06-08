"""
Laboratorium 05 - Generator lasu z typami roslin i biomami
Systemy Animacji Komputerowej - Blender Python API (bpy)

Jak uruchomic:
1. Blender -> Scripting -> Open -> las_05.py
2. Run Script
3. W scenie powstanie kolekcja "Las" z podkolekcjami.
4. Render zapisze sie jako las_05.png obok pliku .blend albo w katalogu tymczasowym Blendera.

Poprawiona wersja:
- uzywa normalnego ukladu Blendera: X/Y = ziemia, Z = wysokosc,
- rosliny nie sa juz dziwnymi pionowymi kulkami,
- drzewa maja pien i korone,
- krzewy sa niskimi kepami,
- paprocie maja promieniste plaskie liscie,
- zachowana jest logika labu: TYPY_ROSLIN, biom, seed, kolekcja Las i podkolekcje.
"""

import math
import os
import random
from typing import Dict, List, Tuple

import bpy
from mathutils import Vector


Kolor = Tuple[float, float, float, float]


# -----------------------------
# 1. Slownik typow roslin
# -----------------------------
TYPY_ROSLIN: Dict[str, dict] = {
    "drzewo": {
        "wysokosc": (3.0, 4.8),
        "liczba_lisci": (5, 7),
        "promien_lisci": (0.55, 0.85),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.16, 0.09, 0.035, 1.0),
        "kolor_lisci": (0.04, 0.32, 0.09, 1.0),
        "promien_lodygi": (0.10, 0.17),
    },
    "krzew": {
        "wysokosc": (0.75, 1.35),
        "liczba_lisci": (6, 9),
        "promien_lisci": (0.35, 0.60),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.24, 0.14, 0.05, 1.0),
        "kolor_lisci": (0.08, 0.45, 0.06, 1.0),
        "promien_lodygi": (0.035, 0.065),
    },
    "paproc": {
        "wysokosc": (0.35, 0.75),
        "liczba_lisci": (7, 11),
        "promien_lisci": (0.55, 0.90),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.18, 0.25, 0.08, 1.0),
        "kolor_lisci": (0.02, 0.55, 0.16, 1.0),
        "promien_lodygi": (0.025, 0.045),
    },
}

PODKOLEKCJE = {
    "drzewo": "Drzewa",
    "krzew": "Krzewy",
    "paproc": "Paprocie",
}

MATERIALY: Dict[str, bpy.types.Material] = {}


# -----------------------------
# 2. Narzedzia sceny/materialow
# -----------------------------
def material(nazwa: str, kolor: Kolor) -> bpy.types.Material:
    if nazwa in MATERIALY:
        return MATERIALY[nazwa]

    mat = bpy.data.materials.new(nazwa)
    mat.diffuse_color = kolor
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = kolor
        bsdf.inputs["Roughness"].default_value = 0.80
    MATERIALY[nazwa] = mat
    return mat


def linkuj_tylko_do(obj: bpy.types.Object, kol: bpy.types.Collection) -> None:
    if obj.name not in kol.objects:
        kol.objects.link(obj)
    for stara in list(obj.users_collection):
        if stara != kol:
            stara.objects.unlink(obj)


def usun_kolekcje(nazwa: str) -> None:
    kol = bpy.data.collections.get(nazwa)
    if not kol:
        return

    def wszystkie_obiekty(k: bpy.types.Collection):
        wynik = list(k.objects)
        for dziecko in k.children:
            wynik.extend(wszystkie_obiekty(dziecko))
        return wynik

    for obj in set(wszystkie_obiekty(kol)):
        bpy.data.objects.remove(obj, do_unlink=True)

    def usun_dzieci(k: bpy.types.Collection):
        for dziecko in list(k.children):
            usun_dzieci(dziecko)
            bpy.data.collections.remove(dziecko)

    usun_dzieci(kol)
    bpy.data.collections.remove(kol)


def przygotuj_kolekcje() -> Tuple[bpy.types.Collection, Dict[str, bpy.types.Collection]]:
    usun_kolekcje("Las")

    las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(las)

    podkolekcje = {}
    for typ, nazwa in PODKOLEKCJE.items():
        pod = bpy.data.collections.new(nazwa)
        las.children.link(pod)
        podkolekcje[typ] = pod
    return las, podkolekcje


# -----------------------------
# 3. Prymitywy geometryczne
# -----------------------------
def cylinder(nazwa: str, radius: float, depth: float, loc, mat, vertices: int = 18) -> bpy.types.Object:
    # W Blenderze cylinder stoi pionowo wzdluz osi Z.
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = nazwa
    obj.data.materials.append(mat)
    return obj


def kula(nazwa: str, radius: float, loc, mat, scale=(1.0, 1.0, 1.0), segments: int = 24) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=12, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = nazwa
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj


def lisc_paprotki(nazwa: str, loc, dlugosc: float, szerokosc: float, kat: float, mat) -> bpy.types.Object:
    # Plaski, zielony lisc jako cienka elipsoida lezaca poziomo i skierowana na zewnatrz.
    obj = kula(nazwa, 1.0, loc, mat, scale=(dlugosc, szerokosc, 0.055), segments=16)
    obj.rotation_euler[2] = kat
    obj.rotation_euler[0] = random.uniform(-0.12, 0.12)
    return obj


def korzen(nazwa: str, x: float, y: float, kat: float, dlugosc: float, mat) -> bpy.types.Object:
    # Cienki cylinder polozony na ziemi. Domyslnie jest pionowy, wiec kladziemy go poziomo.
    sx = x + math.cos(kat) * dlugosc / 2.0
    sy = y + math.sin(kat) * dlugosc / 2.0
    obj = cylinder(nazwa, 0.025, dlugosc, (sx, sy, 0.035), mat, vertices=8)
    obj.rotation_euler[1] = math.radians(90)
    obj.rotation_euler[2] = kat
    return obj


# -----------------------------
# 4. Funkcje tworzenia roslin
# -----------------------------
def stworz_rosline(
    pozycja: Tuple[float, float, float],
    wysokosc: float,
    liczba_lisci: int,
    promien_lisci: float,
    liczba_korzeni: int,
    material_lodygi: bpy.types.Material,
    material_lisci: bpy.types.Material,
    promien_lodygi: float,
    typ: str,
) -> List[bpy.types.Object]:
    """
    Zmodyfikowana funkcja z Lab 04.
    Argument pozycja jest w stylu labu: (x, 0, z), ale wewnatrz mapujemy to na Blender:
    x -> X, z -> Y, wysokosc -> Z.
    """
    x = pozycja[0]
    y = pozycja[2]
    obiekty: List[bpy.types.Object] = []

    if typ == "drzewo":
        pien = cylinder("drzewo_pien", promien_lodygi, wysokosc, (x, y, wysokosc / 2.0), material_lodygi, vertices=20)
        obiekty.append(pien)

        for i in range(liczba_korzeni):
            kat = 2 * math.pi * i / liczba_korzeni + random.uniform(-0.18, 0.18)
            obiekty.append(korzen(f"drzewo_korzen_{i+1}", x, y, kat, random.uniform(0.35, 0.70), material_lodygi))

        # Korona: jedna wieksza kula plus kilka mniejszych. Daje normalne drzewo, nie slup kulek.
        obiekty.append(kula("drzewo_korona_glowna", promien_lisci * 1.25, (x, y, wysokosc + promien_lisci * 0.35), material_lisci, scale=(1.08, 1.08, 0.92)))
        for i in range(liczba_lisci - 1):
            kat = 2 * math.pi * i / max(1, liczba_lisci - 1)
            r = promien_lisci * random.uniform(0.55, 0.95)
            loc = (
                x + math.cos(kat) * r,
                y + math.sin(kat) * r,
                wysokosc + random.uniform(-0.05, 0.45) * promien_lisci,
            )
            obiekty.append(kula(f"drzewo_korona_{i+1}", promien_lisci * random.uniform(0.65, 0.90), loc, material_lisci, scale=(1.0, 1.0, 0.88)))

    elif typ == "krzew":
        # Krzew: niski srodek + kepa lisci przy ziemi.
        pien = cylinder("krzew_lodyga", promien_lodygi, wysokosc * 0.55, (x, y, wysokosc * 0.275), material_lodygi, vertices=12)
        obiekty.append(pien)

        for i in range(liczba_lisci):
            kat = 2 * math.pi * i / liczba_lisci + random.uniform(-0.20, 0.20)
            r = promien_lisci * random.uniform(0.25, 0.80)
            loc = (
                x + math.cos(kat) * r,
                y + math.sin(kat) * r,
                random.uniform(0.35, wysokosc),
            )
            obiekty.append(kula(f"krzew_lisc_{i+1}", promien_lisci * random.uniform(0.62, 0.92), loc, material_lisci, scale=(1.0, 1.0, 0.75), segments=18))

        for i in range(liczba_korzeni):
            kat = 2 * math.pi * i / liczba_korzeni
            obiekty.append(korzen(f"krzew_korzen_{i+1}", x, y, kat, random.uniform(0.18, 0.35), material_lodygi))

    elif typ == "paproc":
        # Paproc: bardzo niska lodyga i promieniste plaskie liscie.
        srodek = cylinder("paproc_srodek", promien_lodygi, wysokosc * 0.35, (x, y, wysokosc * 0.175), material_lodygi, vertices=10)
        obiekty.append(srodek)

        for i in range(liczba_lisci):
            kat = 2 * math.pi * i / liczba_lisci + random.uniform(-0.10, 0.10)
            dl = promien_lisci * random.uniform(0.65, 1.05)
            szer = promien_lisci * random.uniform(0.11, 0.18)
            loc = (
                x + math.cos(kat) * dl * 0.50,
                y + math.sin(kat) * dl * 0.50,
                wysokosc * random.uniform(0.35, 0.70),
            )
            obiekty.append(lisc_paprotki(f"paproc_lisc_{i+1}", loc, dl, szer, kat, material_lisci))

    return obiekty


def stworz_rosline_typ(x: float, z: float, typ: str) -> List[bpy.types.Object]:
    cfg = TYPY_ROSLIN[typ]

    wysokosc = random.uniform(*cfg["wysokosc"])
    liczba_lisci = random.randint(*cfg["liczba_lisci"])
    promien_lisci = random.uniform(*cfg["promien_lisci"])
    liczba_korzeni = random.randint(*cfg["liczba_korzeni"])
    promien_lodygi = random.uniform(*cfg["promien_lodygi"])

    mat_lodyga = material(f"mat_{typ}_lodyga", cfg["kolor_lodygi"])
    mat_liscie = material(f"mat_{typ}_liscie", cfg["kolor_lisci"])

    return stworz_rosline(
        pozycja=(x, 0.0, z),
        wysokosc=wysokosc,
        liczba_lisci=liczba_lisci,
        promien_lisci=promien_lisci,
        liczba_korzeni=liczba_korzeni,
        material_lodygi=mat_lodyga,
        material_lisci=mat_liscie,
        promien_lodygi=promien_lodygi,
        typ=typ,
    )


# -----------------------------
# 5. Biom
# -----------------------------
def wybierz_typ_biomu(x: float, z: float, rozmiar_pola: float) -> str:
    polowa = rozmiar_pola / 2.0
    odleglosc = max(abs(x), abs(z)) / polowa

    if odleglosc < 0.30:
        return "drzewo"
    elif odleglosc < 0.70:
        return "krzew" if random.random() < 0.70 else "drzewo"
    else:
        return "paproc" if random.random() < 0.70 else "krzew"


# -----------------------------
# 6. Teren, kamera, render
# -----------------------------
def dodaj_teren(rozmiar_pola: float, kolekcja: bpy.types.Collection) -> None:
    mat = material("mat_teren", (0.12, 0.28, 0.08, 1.0))
    bpy.ops.mesh.primitive_plane_add(size=rozmiar_pola * 1.15, location=(0, 0, 0))
    teren = bpy.context.object
    teren.name = "teren_lasu"
    teren.data.materials.append(mat)
    linkuj_tylko_do(teren, kolekcja)


def ustaw_kamere_i_swiatlo(rozmiar_pola: float) -> None:
    for nazwa in ["Kamera_Las_05", "Slonce_Las_05"]:
        obj = bpy.data.objects.get(nazwa)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.object.light_add(type="SUN", location=(0, 0, 8))
    sun = bpy.context.object
    sun.name = "Slonce_Las_05"
    sun.data.energy = 2.7
    sun.rotation_euler = (math.radians(45), 0, math.radians(35))

    # Kamera patrzy pod katem, zeby bylo widac wysokosc drzew i strefy biomu.
    bpy.ops.object.camera_add(location=(7.5, -9.0, 6.2), rotation=(math.radians(61), 0, math.radians(42)))
    cam = bpy.context.object
    cam.name = "Kamera_Las_05"
    cam.data.lens = 28
    bpy.context.scene.camera = cam

    # Dodatkowe ustawienie: kamera patrzy dokladnie w centrum sceny.
    kierunek = Vector((0, 0, 1.0)) - cam.location
    cam.rotation_euler = kierunek.to_track_quat("-Z", "Y").to_euler()

    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 800

    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        try:
            bpy.context.scene.render.engine = "BLENDER_EEVEE"
        except TypeError:
            bpy.context.scene.render.engine = "BLENDER_WORKBENCH"

    try:
        bpy.context.scene.eevee.taa_render_samples = 32
    except Exception:
        pass

    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"


def sciezka_renderu() -> str:
    if bpy.data.filepath:
        katalog = os.path.dirname(bpy.data.filepath)
    else:
        katalog = bpy.app.tempdir or os.getcwd()
    return os.path.join(katalog, "las_05.png")


# -----------------------------
# 7. Generator glowny
# -----------------------------
def generuj_las(liczba_roslin: int = 18, rozmiar_pola: float = 10.0, seed: int = 42, renderuj: bool = True) -> None:
    random.seed(seed)

    las, podkolekcje = przygotuj_kolekcje()
    dodaj_teren(rozmiar_pola, las)

    licznik = {"drzewo": 0, "krzew": 0, "paproc": 0}

    for _ in range(liczba_roslin):
        x = random.uniform(-rozmiar_pola / 2.0, rozmiar_pola / 2.0)
        z = random.uniform(-rozmiar_pola / 2.0, rozmiar_pola / 2.0)
        typ = wybierz_typ_biomu(x, z, rozmiar_pola)
        licznik[typ] += 1

        obiekty = stworz_rosline_typ(x, z, typ)
        for obj in obiekty:
            linkuj_tylko_do(obj, podkolekcje[typ])

    ustaw_kamere_i_swiatlo(rozmiar_pola)

    print("Wygenerowano las 05:")
    print(f"drzewa:   {licznik['drzewo']}")
    print(f"krzewy:   {licznik['krzew']}")
    print(f"paprocie: {licznik['paproc']}")
    print("Kolekcja: Las -> Drzewa, Krzewy, Paprocie")

    if renderuj:
        wynik = sciezka_renderu()
        bpy.context.scene.render.filepath = wynik
        bpy.ops.render.render(write_still=True)
        print(f"Render zapisany: {wynik}")


# Wymagane w labie: wywolanie funkcji na koncu skryptu.
generuj_las(liczba_roslin=18, rozmiar_pola=10.0, seed=42, renderuj=True)
