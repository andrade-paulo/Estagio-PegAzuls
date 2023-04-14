import json

with open('./inputs2.json', 'r') as f:
    dados = json.load(f)


# ------------------- ESTIMATIVA PESO VAZIO ----------------------
# Levando em consideração apenas Asa, GAP e Empenagem

Sasabase = 0.984
Pasabase = 1633
Sehbase = 0.16
Pehbase = 258
SGAPbase = 0.12
PGAPbase = 266


Pasaatual = (Pasabase* dados["constantesV"]["S"]) / Sasabase
Pehatual = (Pehbase* dados["constantesV"]["Sht"]) / Sehbase
PGAPatual = (PGAPbase* dados["constantesV"]["SGAP"]) / SGAPbase

Somapatual = Pasaatual + Pehatual + PGAPatual
Somapbase = Pasabase + Pehbase + PGAPbase

PVbase = 3260
PVatual = (PVbase * Somapatual) / Somapbase

print (PVatual)

# ------------------------- Declaração de Constantes ----------------------
g = 9.81
f = 0.9072
mi = 0.0270
r = 1.1132
xlim=55
h=10**-2


nomes_vetores = ["m", "w", "t", "vx", "vy", "x", "y", "T", "D", "L", "Fr", "ax", "ay"]
vetores = {nome: [] for nome in nomes_vetores}
vetores["m"][0] = 5
print(vetores["m"])


w[0] = m[1] * g
t[0] = 0
vx[0] = 0
vy[0] = 0
x[0] = 0
y[0] = 0
T[0] = (47.782-(vx[1]**2)) * f

D[0] = 0.5 * r * vx[1]**2 * S *(Cd0 + K * Cl**2 + Cdht * (Sht/S) * Kht)

L[1] = 0.5 * r * vx[1]**2 * S * (Cl)
Fr[1] = mi * abs (L[1] - w[1])
ax[1] = (T[1]-D[1]-Fr[1]) / m[1]
ay[1] = 0