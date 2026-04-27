import glob
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# KROK 1 – Načtení snímků
# -----------------------------

# seznam souborů
files_a = sorted(glob.glob("skupina_a/*.png"))
files_b = sorted(glob.glob("skupina_b/*.png"))

# načtení obrázků (jen první kanál)
skupina_a = [plt.imread(f)[:, :, 0] for f in files_a]
skupina_b = [plt.imread(f)[:, :, 0] for f in files_b]

print("Načteno snímků skupiny A:", len(skupina_a))
print("Načteno snímků skupiny B:", len(skupina_b))

# zobrazení prvních snímků
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

ax1.imshow(skupina_a[0], cmap="gray", vmin=0, vmax=1)
ax1.set_title("Zdravá tkáň – snímek 0")
ax1.axis("off")

ax2.imshow(skupina_b[0], cmap="gray", vmin=0, vmax=1)
ax2.set_title("Nádorová tkáň – snímek 0")
ax2.axis("off")

plt.tight_layout()
plt.show()


# -----------------------------
# KROK 2 – Prahování
# -----------------------------

PRAH = 0.5
snimek = skupina_a[0]

# binární maska
maska = snimek > PRAH

# vizualizace
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

ax1.imshow(snimek, cmap="gray", vmin=0, vmax=1)
ax1.set_title("Původní snímek")
ax1.axis("off")

ax2.imshow(maska, cmap="gray")
ax2.set_title(f"Maska (práh = {PRAH})")
ax2.axis("off")

plt.tight_layout()
plt.show()


# -----------------------------
# KROK 3 – Výpočty
# -----------------------------

# poměrná plocha (%)
podil = (maska.sum() / maska.size) * 100

# průměrná intenzita uvnitř masky
mean_int = snimek[maska].mean()

print(f"Plocha struktury: {podil:.1f} %")
print(f"Průměrná intenzita: {mean_int:.3f}")


# -----------------------------
# KROK 4 – Srovnání skupin
# -----------------------------

def spocitej_podil(snimek, prah):
    maska = snimek > prah
    return (maska.sum() / maska.size) * 100


PRAH = 0.5

podily_a = [spocitej_podil(img, PRAH) for img in skupina_a]
podily_b = [spocitej_podil(img, PRAH) for img in skupina_b]

# boxplot
fig, ax = plt.subplots()

ax.boxplot([podily_a, podily_b],
           tick_labels=["Zdravá tkáň", "Nádorová tkáň"])

ax.set_title("Porovnání plochy struktury")
ax.set_ylabel("Plocha (%)")
ax.grid(True, axis="y", alpha=0.4)

plt.show()

print("Skupina A:", [f"{p:.1f} %" for p in podily_a])
print("Skupina B:", [f"{p:.1f} %" for p in podily_b])