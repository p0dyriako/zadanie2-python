# Zadanie 2 – Python (Programovacie techniky)

**Autor:** Arsenii Podyriako, Smart technológie vo výrobe, FVT TUKE

Aplikácia simuluje **tepelnú rozťažnosť oceľovej tyče** vo výrobnej hale.

## Čo program robí
1. Vygeneruje pole **60 náhodných teplôt** (15–35 °C).
2. Operácie s poľom: **zoradenie, min, max, priemer, medián**.
3. Výpočet: `ΔL = α · L0 · (T − T0)`, kde α = 12·10⁻⁶ 1/°C, L0 = 1000 mm, T0 = 20 °C.
4. **Jeden graf** s pôvodnými (teplota) aj vypočítanými (ΔL) hodnotami (dve osi Y).
5. **GUI (Tkinter):** vstupné pole, tlačidlo „Vypočítať", popis s výsledkom pre ľubovoľné číslo.
6. Tlačidlo „Nové náhodné dáta" vygeneruje nové pole.

## Spustenie
```
pip install numpy matplotlib
python app.py
```

## Vytvorenie .exe
```
pip install pyinstaller
pyinstaller --onefile --windowed --name TepelnaRoztaznost app.py
```
Výsledok: `dist/TepelnaRoztaznost.exe` (spustí sa aj bez Pythonu).
