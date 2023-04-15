import json

with open('inputs.json', 'r') as f:
    dados = json.load(f)

# ------------------- ESTIMATIVA PESO VAZIO ----------------------
# Levando em consideração apenas Asa, GAP e Empenagem

Sasabase = 0.984
Pasabase = 1633
Sehbase = 0.16
Pehbase = 258
SGAPbase = 0.12
PGAPbase = 266

Pasaatual = (Pasabase * dados["constantesV"]["S"]) / Sasabase
Pehatual = (Pehbase * dados["constantesV"]["Sht"]) / Sehbase
PGAPatual = (PGAPbase * dados["constantesV"]["SGAP"]) / SGAPbase

Somapatual = Pasaatual + Pehatual + PGAPatual
Somapbase = Pasabase + Pehbase + PGAPbase

PVbase = 3260
PVatual = (PVbase * Somapatual) / Somapbase

# ------------------------- Declaração de Constantes ----------------------
g = 9.81
f = 0.9072
mi = 0.0270
r = 1.1132
xlim = 55
h = 10 ** -2

# ------------------------- CONDIÇÕES INICIAIS -------------------------

m = [5]
w = [m[0] * g]
t = [0]
vx = [0]
vy = [0]
x = [0]
y = [0]
T = [(47.782 - (vx[0] ** 2)) * f]

D = [0.5 * r * vx[0] ** 2 * dados["S"]
     * (dados["Cd0"] + dados["K"] * dados["Cl"] ** 2
        + dados["Cdht"] * (dados["Sht"] / dados["S"]) * dados["Kht"])]

L = [0.5 * r * vx[0] ** 2 * dados["S"] * (dados["Cl"])]
Fr = [mi * abs(L[0] - w[0])]
ax = [(T[0] - D[0] - Fr[0]) / m[0]]
ay = [0]


