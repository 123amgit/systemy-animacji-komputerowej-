import bpy
import math
import os

# ============================================================
# LAB 11 - Animacja geometrii rośliny przez bpy
# ============================================================
# Folder projektu zawiera:
# - lab08_materialy_oswietlenie.blend  -> źródłowy asset rośliny
# - roslina_ozywiona_11.blend          -> pusty plik docelowy
# - roslina_animacja_geometrii.py      -> ten skrypt
#
# Skrypt:
# 1. Importuje kolekcję Roslina_Hero z lab08_materialy_oswietlenie.blend.
# 2. Wyszukuje liście po prefiksie Roslina_Lisc.
# 3. Animuje liście sinusoidalnie przez rotation_euler.
# 4. Wyszukuje pąki po prefiksie Roslina_Pak.
# 5. Animuje pąki przez skalowanie.
# 6. Delikatnie animuje łodygę.
# 7. Ustawia scenę, kamerę, światło, ścieżkę renderu i zapisuje plik .blend.
# ============================================================


# ============================================================
# KONFIGURACJA
# ============================================================

FOLDER_PROJEKTU = os.path.dirname(bpy.data.filepath)

# Źródłowy plik z rośliną z Lab 8
SCIEZKA_ASSETU = os.path.join(FOLDER_PROJEKTU, "lab08_materialy_oswietlenie.blend")

# Kolekcja z rośliną w pliku Lab 8
NAZWA_KOLEKCJI = "Roslina_Hero"

# Nazwy obiektów w kolekcji
PREFIX_LISCIA = "Roslina_Lisc"
PREFIX_PAKA = "Roslina_Pak"
NAZWA_LODYGI = "Roslina_Lodyga"

# Animacja
KLATKA_START = 1
KLATKA_KONIEC = 125
FPS = 25

# Ruch liści
CZESTOSC_LISCI = 0.08
AMPLITUDA_LISCI = 0.25

# Ruch pąków
PAK_START = 30
PAK_KONIEC = 90
PAK_SKALA_MIN = 0.15
PAK_SKALA_MAX = 1.0

# Pliki wynikowe
PLIK_WYNIKOWY_BLEND = os.path.join(FOLDER_PROJEKTU, "roslina_ozywiona_11.blend")
PLIK_WYNIKOWY_MP4 = os.path.join(FOLDER_PROJEKTU, "roslina_ozywiona_11.mp4")


# ============================================================
# FUNKCJE POMOCNICZE
# ============================================================

def wyczysc_animacje(obj):
    """
    Usuwa istniejącą animację obiektu.
    Dzięki temu skrypt można uruchamiać wiele razy bez dokładania starych F-Curves.
    """
    if obj.animation_data and obj.animation_data.action:
        obj.animation_data.action = None


def ustaw_scene():
    """
    Ustawia długość animacji i FPS.
    """
    scena = bpy.context.scene
    scena.frame_start = KLATKA_START
    scena.frame_end = KLATKA_KONIEC
    scena.render.fps = FPS
    scena.frame_set(KLATKA_START)


def usun_domyslny_cube():
    """
    Usuwa domyślny Cube, jeśli istnieje.
    """
    for obj in list(bpy.data.objects):
        if obj.name.startswith("Cube"):
            bpy.data.objects.remove(obj, do_unlink=True)


def pokaz_liste_obiektow():
    """
    Wypisuje obiekty w konsoli Blendera.
    Pomaga znaleźć błędne nazwy liści/pąków.
    """
    print("\nDostępne obiekty w scenie:")
    for obj in bpy.data.objects:
        print(" -", obj.name)


def usun_stara_kolekcje_docelowa(nazwa_kolekcji):
    """
    Jeśli skrypt był już uruchamiany, usuwa starą zaimportowaną kolekcję.
    Dzięki temu ponowne uruchomienie daje czystą scenę, bez duplikatów.
    """
    kolekcja = bpy.data.collections.get(nazwa_kolekcji)

    if kolekcja is None:
        return

    print(f"Usuwam starą kolekcję: {nazwa_kolekcji}")

    for obj in list(kolekcja.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(kolekcja)


# ============================================================
# IMPORT KOLEKCJI Z PLIKU .BLEND
# ============================================================

def importuj_kolekcje_z_blend(sciezka_blend, nazwa_kolekcji):
    """
    Importuje kolekcję z innego pliku .blend przez bpy.ops.wm.append().
    """
    if not os.path.exists(sciezka_blend):
        print("\nBŁĄD: Nie znaleziono pliku źródłowego:")
        print(sciezka_blend)
        print("Sprawdź, czy lab08_materialy_oswietlenie.blend jest w tym samym folderze co roslina_ozywiona_11.blend.")
        return False

    directory = os.path.join(sciezka_blend, "Collection")
    filepath = os.path.join(directory, nazwa_kolekcji)

    try:
        bpy.ops.wm.append(
            filepath=filepath,
            directory=directory,
            filename=nazwa_kolekcji
        )

        print(f"\nZaimportowano kolekcję: {nazwa_kolekcji}")
        return True

    except Exception as e:
        print("\nBŁĄD podczas importowania kolekcji.")
        print("Sprawdź, czy w lab08_materialy_oswietlenie.blend istnieje kolekcja:", nazwa_kolekcji)
        print("Szczegóły błędu:", e)
        return False


# ============================================================
# ANIMACJA LIŚCI
# ============================================================

def animuj_lisc(obj, faza, czestosc=CZESTOSC_LISCI, amplituda=AMPLITUDA_LISCI,
                klatka_start=KLATKA_START, klatka_koniec=KLATKA_KONIEC):
    """
    Animuje jeden liść przez sinusoidalną rotację.
    Keyframe jest wstawiany tylko na osi Y: rotation_euler index=1.
    """
    wyczysc_animacje(obj)

    rotacja_bazowa_y = obj.rotation_euler[1]

    for klatka in range(klatka_start, klatka_koniec + 1, 3):
        kat = rotacja_bazowa_y + amplituda * math.sin(klatka * czestosc + faza)
        obj.rotation_euler[1] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)

    print(f"Zaanimowano liść: {obj.name}")


def animuj_wszystkie_liscie(prefix_nazwy=PREFIX_LISCIA):
    """
    Szuka wszystkich liści po nazwie i animuje je w jednej pętli.
    Każdy liść ma inną fazę, więc ruch nie jest identyczny.
    """
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]

    if not liscie:
        print("\nUWAGA: Nie znaleziono liści.")
        print(f"Skrypt szuka obiektów zaczynających się od: {prefix_nazwy}")
        print("Przykłady poprawnych nazw:")
        print("Roslina_Lisc_01")
        print("Roslina_Lisc_02")
        print("Roslina_Lisc_03")
        pokaz_liste_obiektow()
        return 0

    liczba_lisci = len(liscie)

    for i, lisc in enumerate(liscie):
        faza = i * (2 * math.pi / max(liczba_lisci, 1))
        animuj_lisc(lisc, faza=faza)

    print(f"\nŁącznie zaanimowano liście: {liczba_lisci}")
    return liczba_lisci


# ============================================================
# ANIMACJA PĄKÓW
# ============================================================

def animuj_pak(obj, klatka_start=PAK_START, klatka_koniec=PAK_KONIEC,
               skala_min=PAK_SKALA_MIN, skala_max=PAK_SKALA_MAX):
    """
    Animuje pąk przez skalowanie.
    Pąk jest mały na początku, potem rośnie/otwiera się między klatkami start-koniec.
    """
    wyczysc_animacje(obj)

    obj.scale = (skala_min, skala_min, skala_min)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    obj.keyframe_insert(data_path="scale", frame=klatka_start)

    obj.scale = (skala_max, skala_max, skala_max)
    obj.keyframe_insert(data_path="scale", frame=klatka_koniec)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)

    print(f"Zaanimowano pąk: {obj.name}")


def animuj_wszystkie_paki(prefix_nazwy=PREFIX_PAKA):
    """
    Szuka wszystkich pąków i animuje ich otwieranie.
    Każdy kolejny pąk startuje trochę później.
    """
    paki = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]

    if not paki:
        print("\nUWAGA: Nie znaleziono pąków.")
        print(f"Skrypt szuka obiektów zaczynających się od: {prefix_nazwy}")
        print("Przykłady poprawnych nazw:")
        print("Roslina_Pak_01")
        print("Roslina_Pak_02")
        print("Roslina_Pak_03")
        pokaz_liste_obiektow()
        return 0

    for i, pak in enumerate(paki):
        opoznienie = i * 10
        start = PAK_START + opoznienie
        koniec = min(PAK_KONIEC + opoznienie, KLATKA_KONIEC)

        animuj_pak(
            pak,
            klatka_start=start,
            klatka_koniec=koniec,
            skala_min=PAK_SKALA_MIN,
            skala_max=PAK_SKALA_MAX
        )

    print(f"\nŁącznie zaanimowano pąki: {len(paki)}")
    return len(paki)


# ============================================================
# DODATKOWA ANIMACJA ŁODYGI
# ============================================================

def animuj_lodyge(nazwa=NAZWA_LODYGI):
    """
    Delikatnie kołysze łodygę.
    To dodatkowy efekt, żeby animacja wyglądała bardziej żywo.
    """
    obj = bpy.data.objects.get(nazwa)

    if obj is None:
        print(f"\nNie znaleziono łodygi o nazwie {nazwa}. Pomijam animację łodygi.")
        return False

    wyczysc_animacje(obj)

    rotacja_bazowa_x = obj.rotation_euler[0]

    for klatka in range(KLATKA_START, KLATKA_KONIEC + 1, 5):
        kat = rotacja_bazowa_x + 0.05 * math.sin(klatka * 0.04)
        obj.rotation_euler[0] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=0)

    print(f"Zaanimowano łodygę: {obj.name}")
    return True


# ============================================================
# KAMERA I ŚWIATŁO
# ============================================================

def ustaw_kamere_na_rosline():
    """
    Ustawia kamerę tak, żeby widziała pionową roślinę z Lab 8.
    Jeśli kamera została zaimportowana z assetu, zostanie użyta.
    """
    kamera = bpy.context.scene.camera

    if kamera is None:
        bpy.ops.object.camera_add()
        kamera = bpy.context.object
        kamera.name = "Kamera_Lab11"
        bpy.context.scene.camera = kamera

    kamera.location = (0, -7, 3.2)
    kamera.rotation_euler = (math.radians(65), 0, 0)
    kamera.data.lens = 35

    print("Ustawiono kamerę.")


def dodaj_swiatlo():
    """
    Dodaje światła tylko wtedy, gdy w scenie nie ma żadnego światła.
    Jeśli Lab 8 ma własne oświetlenie, zostaje zachowane.
    """
    swiatla = [obj for obj in bpy.data.objects if obj.type == "LIGHT"]

    if swiatla:
        print("Światła już istnieją w scenie. Pomijam dodawanie nowych.")
        return

    bpy.ops.object.light_add(type="SUN", location=(0, -4, 6))
    sun = bpy.context.object
    sun.name = "Sun_Lab11"
    sun.data.energy = 2.0

    bpy.ops.object.light_add(type="AREA", location=(3, -4, 4))
    area = bpy.context.object
    area.name = "Area_Lab11"
    area.data.energy = 400
    area.data.size = 5

    print("Dodano światła.")


# ============================================================
# RENDER
# ============================================================

def ustaw_enum_bezpiecznie(obiekt, nazwa_wlasciwosci, wartosc):
    """
    Próbuje ustawić właściwość enum tylko wtedy, gdy dana wartość istnieje.
    Przydatne dla różnych wersji Blendera.
    """
    try:
        prop = obiekt.bl_rna.properties[nazwa_wlasciwosci]
        dozwolone = [item.identifier for item in prop.enum_items]

        if wartosc in dozwolone:
            setattr(obiekt, nazwa_wlasciwosci, wartosc)
            return True

    except Exception:
        pass

    return False


def ustaw_render():
    """
    Ustawia ścieżkę renderu i próbuje ustawić format video.
    W Blenderze 5.1 część ustawień video bywa inaczej nazwana,
    dlatego skrypt robi to bezpiecznie i nie przerywa działania.
    """
    scena = bpy.context.scene

    # Silnik renderu
    ustaw_enum_bezpiecznie(scena.render, "engine", "BLENDER_EEVEE_NEXT")
    ustaw_enum_bezpiecznie(scena.render, "engine", "BLENDER_EEVEE")

    scena.render.filepath = PLIK_WYNIKOWY_MP4

    scena.render.resolution_x = 1280
    scena.render.resolution_y = 720
    scena.render.resolution_percentage = 100

    # Blender 5.1 ma w UI Media Type: Image / Video.
    # Jeżeli ta właściwość istnieje w danej wersji, ustawiamy VIDEO.
    ustaw_enum_bezpiecznie(scena.render.image_settings, "media_type", "VIDEO")

    # Starsze wersje miały file_format = FFMPEG.
    # W 5.1 ta wartość może nie istnieć, więc próbujemy, ale nie wymagamy.
    ustaw_enum_bezpiecznie(scena.render.image_settings, "file_format", "FFMPEG")

    # Ustawienia ffmpeg, jeśli są dostępne.
    if hasattr(scena.render, "ffmpeg"):
        ustaw_enum_bezpiecznie(scena.render.ffmpeg, "format", "MPEG4")
        ustaw_enum_bezpiecznie(scena.render.ffmpeg, "codec", "H264")

    print("Ustawiono ścieżkę renderu:")
    print(PLIK_WYNIKOWY_MP4)
    print("Sprawdź w Output Properties: Media Type = Video, Container = MPEG-4, Codec = H.264.")


# ============================================================
# ZAPIS
# ============================================================

def zapisz_plik_blend():
    """
    Zapisuje końcowy plik .blend.
    """
    bpy.ops.wm.save_as_mainfile(filepath=PLIK_WYNIKOWY_BLEND)
    print("Zapisano plik:")
    print(PLIK_WYNIKOWY_BLEND)


# ============================================================
# GŁÓWNY PROGRAM
# ============================================================

def main():
    print("\n==============================")
    print("LAB 11 - START SKRYPTU")
    print("==============================")

    if not bpy.data.filepath:
        print("\nBŁĄD: Najpierw zapisz pusty plik jako roslina_ozywiona_11.blend.")
        print("Dopiero potem uruchom skrypt, żeby znał folder projektu.")
        return

    print("\nFolder projektu:")
    print(FOLDER_PROJEKTU)

    print("\nPlik źródłowy:")
    print(SCIEZKA_ASSETU)

    ustaw_scene()
    usun_domyslny_cube()

    # Przy ponownym uruchomieniu skryptu usuwamy wcześniejszy import.
    usun_stara_kolekcje_docelowa(NAZWA_KOLEKCJI)

    sukces = importuj_kolekcje_z_blend(SCIEZKA_ASSETU, NAZWA_KOLEKCJI)
    if not sukces:
        print("\nNie udało się zaimportować rośliny. Skrypt zatrzymany.")
        return

    liczba_lisci = animuj_wszystkie_liscie()
    liczba_pakow = animuj_wszystkie_paki()
    animuj_lodyge()

    ustaw_kamere_na_rosline()
    dodaj_swiatlo()
    ustaw_render()
    zapisz_plik_blend()

    print("\n==============================")
    print("LAB 11 - KONIEC SKRYPTU")
    print("==============================")
    print(f"Liście: {liczba_lisci}")
    print(f"Pąki: {liczba_pakow}")
    print("Odtwórz timeline 1-125, żeby sprawdzić animację.")
    print("Potem wyrenderuj przez Ctrl + F12.")
    print("==============================\n")


main()