"""
Programovacie techniky - Zadanie 2 (Python)
Autor: Arsenii Podyriako, Smart technológie vo výrobe, FVT TUKE

Téma: Tepelná rozťažnosť oceľového dielca vo výrobnej hale.
Simulujeme 60 meraní teploty (°C) a pre každú vypočítame zmenu dĺžky
oceľovej tyče podľa vzorca:   dL = alpha * L0 * (T - T0)   [mm]
"""

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Konštanty vzorca ----------------
ALPHA = 12e-6   # koeficient tepelnej rozťažnosti ocele [1/°C]
L0 = 1000.0     # pôvodná dĺžka tyče [mm]
T0 = 20.0       # referenčná teplota [°C]
POCET = 60      # počet meraní (min. 50)


# ---------------- Logika ----------------
def generuj_teploty(n=POCET):
    """1. Pole vstupných hodnôt: n náhodných teplôt 15-35 °C."""
    return np.round(np.random.uniform(15, 35, n), 2)


def vypocet(teplota):
    """3. Výpočet: zmena dĺžky tyče v mm (funguje pre číslo aj pole)."""
    return ALPHA * L0 * (np.asarray(teplota, dtype=float) - T0)


def statistika(teploty):
    """2. Práca s poľom: zoradenie, min, max, priemer, medián."""
    return {
        "zoradene": np.sort(teploty),
        "min": float(np.min(teploty)),
        "max": float(np.max(teploty)),
        "priemer": float(np.mean(teploty)),
        "median": float(np.median(teploty)),
    }


# ---------------- GUI ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tepelná rozťažnosť ocele - Zadanie 2")
        self.geometry("980x720")

        self.teploty = generuj_teploty()

        # --- Horný panel: vstup + tlačidlá ---
        panel = ttk.Frame(self, padding=10)
        panel.pack(fill="x")

        ttk.Label(
            panel,
            text=f"Zadaj teplotu (°C) a vypočítaj zmenu dĺžky tyče (L0 = {L0:.0f} mm):",
        ).grid(row=0, column=0, columnspan=4, sticky="w")

        self.vstup = ttk.Entry(panel, width=12)
        self.vstup.grid(row=1, column=0, pady=6, padx=(0, 8))
        self.vstup.insert(0, "30")
        self.vstup.bind("<Return>", lambda e: self.vypocitaj())

        ttk.Button(panel, text="Vypočítať", command=self.vypocitaj).grid(
            row=1, column=1, padx=4
        )
        ttk.Button(panel, text="Nové náhodné dáta", command=self.nove_data).grid(
            row=1, column=2, padx=4
        )

        self.vysledok = ttk.Label(
            panel, text="Výsledok: -", font=("Arial", 12, "bold")
        )
        self.vysledok.grid(row=2, column=0, columnspan=4, sticky="w", pady=(4, 0))

        self.stat_label = ttk.Label(panel, text="", justify="left")
        self.stat_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # --- Graf ---
        self.fig = Figure(figsize=(9, 4.6), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.obnov()

    def vypocitaj(self):
        text = self.vstup.get().strip().replace(",", ".")
        try:
            t = float(text)
        except ValueError:
            messagebox.showerror("Chyba", "Zadaj platné číslo, napr. 27.5")
            return
        dl = float(vypocet(t))
        self.vysledok.config(
            text=f"Pri {t:.2f} °C sa tyč zmení o {dl:+.4f} mm "
            f"(nová dĺžka {L0 + dl:.4f} mm)"
        )

    def nove_data(self):
        self.teploty = generuj_teploty()
        self.obnov()

    def obnov(self):
        s = statistika(self.teploty)
        self.stat_label.config(
            text=(
                f"Počet meraní: {len(self.teploty)}   |   "
                f"Min: {s['min']:.2f} °C   Max: {s['max']:.2f} °C   "
                f"Priemer: {s['priemer']:.2f} °C   Medián: {s['median']:.2f} °C\n"
                f"Najchladnejších 5: {', '.join(f'{x:.1f}' for x in s['zoradene'][:5])}   |   "
                f"Najteplejších 5: {', '.join(f'{x:.1f}' for x in s['zoradene'][-5:])}"
            )
        )

        dl = vypocet(self.teploty)
        cislo = np.arange(1, len(self.teploty) + 1)

        self.ax1.clear()
        self.ax2.clear()
        l1 = self.ax1.plot(cislo, self.teploty, "o-", color="tab:blue",
                           markersize=3, label="Pôvodné: teplota (°C)")
        l2 = self.ax2.plot(cislo, dl, "s--", color="tab:red",
                           markersize=3, label="Vypočítané: zmena dĺžky (mm)")
        self.ax1.set_xlabel("Číslo merania")
        self.ax1.set_ylabel("Teplota (°C)", color="tab:blue")
        self.ax2.set_ylabel("Zmena dĺžky ΔL (mm)", color="tab:red")
        self.ax1.set_title("Teplota a tepelná rozťažnosť oceľovej tyče")
        self.ax1.grid(True, alpha=0.3)
        čiary = l1 + l2
        self.ax1.legend(čiary, [c.get_label() for c in čiary], loc="upper right")
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    App().mainloop()
