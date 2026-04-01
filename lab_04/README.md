# Laboratorium 04 - Proceduralna roślina biomechaniczna w Blender Python API

## Temat ćwiczenia
Implementacja proceduralnej sceny 3D w Blenderze z wykorzystaniem Python API (`bpy`). Celem projektu było stworzenie biomechanicznych roślin generowanych programowo z użyciem prymitywów geometrycznych, materiałów oraz renderu sceny.

## Cel ćwiczenia
Celem laboratorium było:
- zapoznanie się z podstawami Blender Python API,
- tworzenie obiektów 3D przy użyciu kodu,
- manipulacja pozycją, skalą i rotacją obiektów,
- parametryzacja funkcji generujących modele,
- przypisywanie materiałów przez kod,
- przygotowanie sceny, kamery, świateł i renderu.

## Opis programu
Program automatycznie czyści scenę, tworzy podłoże, ustawia świat, oświetlenie i kamerę, a następnie generuje trzy biomechaniczne rośliny o różnych rozmiarach. Każda roślina składa się z:
- łodygi utworzonej z walca,
- liści utworzonych z sześcianów,
- korzeni utworzonych z sześcianów. :contentReference[oaicite:0]{index=0}

W skrypcie zastosowano strukturę modułową. Najważniejsze funkcje to:
- `clear_scene()` - usuwa obiekty i czyści nieużywane dane,
- `make_material()` - tworzy materiał o zadanych parametrach,
- `assign_material()` - przypisuje materiał do obiektu,
- `create_ground()` - tworzy podłoże sceny,
- `setup_world()` - ustawia kolor i jasność tła,
- `setup_light()` - dodaje światła,
- `setup_camera()` - ustawia kamerę,
- `setup_render()` - konfiguruje render,
- `stworz_lodyge()` - tworzy łodygę,
- `stworz_liscie()` - tworzy liście,
- `stworz_korzenie()` - tworzy korzenie,
- `stworz_rosline()` - tworzy pełną roślinę z podanych parametrów,
- `main()` - uruchamia całość programu. :contentReference[oaicite:1]{index=1}

## Struktura projektu
- `lab_04blender.py` - główny skrypt Pythona dla Blendera
- `lab04_rosliny.png` - render końcowy sceny
- `README.md` - opis projektu

## Zastosowane elementy
W projekcie wykorzystano:
- Python
- Blender Python API (`bpy`)
- Blender Eevee
- materiały proceduralne
- render sceny 3D

## Najważniejsze funkcjonalności
- automatyczne czyszczenie sceny przed rozpoczęciem pracy,
- generowanie podłoża, kamery i świateł,
- tworzenie materiałów dla łodygi, liści i korzeni,
- generowanie roślin na podstawie parametrów,
- tworzenie trzech różnych roślin w jednej scenie,
- zapis renderu do pliku PNG,
- zastosowanie efektów materiałowych, w tym metaliczności, roughness i emisji.

## Parametry roślin
Funkcja `stworz_rosline()` przyjmuje między innymi następujące argumenty:
- `x_offset`
- `y_offset`
- `wysokosc`
- `liczba_lisci`
- `promien_lisci`
- `liczba_korzeni`
- materiały dla łodygi, liści i korzeni

Dzięki temu możliwe jest wygodne generowanie wielu wariantów roślin bez powielania kodu. :contentReference[oaicite:2]{index=2}

## Uruchomienie
Aby uruchomić projekt w Blenderze:
1. otworzyć Blender,
2. przejść do zakładki **Scripting**,
3. otworzyć plik `lab_04blender.py`,
4. uruchomić skrypt przyciskiem **Run Script**.
