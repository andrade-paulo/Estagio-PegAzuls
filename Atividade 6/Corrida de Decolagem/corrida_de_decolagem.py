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

Pasaatual = (Pasabase * dados["S"]) / Sasabase
Pehatual = (Pehbase * dados["Sht"]) / Sehbase
PGAPatual = (PGAPbase * dados["SGAP"]) / SGAPbase

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


i = 0
j = 0
CP = w[j] / g
while y[i] < 0.70 and y[i] > 0.75:
    print("Número de Iteração: ", j)
    w[j] = m[j] * g
    m[j + 1] = m[j] + 0.01

    while x[i] < xlim:
        t[i + 1] = t[i] + h
        vx[i + 1] = vx[i] + ax[i] * h
        x[i + 1] = x[i] + vx[i + 1] * h
        T[i + 1] = (47.782 - (vx[0] ** 2)) * f
        D[i + 1] = 0.5 * r * vx[i + 1] ** 2 * dados["S"] * (dados["Cd0"] + dados["K"] * dados["Cl"] ** 2)
        L[i + 1] = 0.5 * r * vx(i + 1) ** 2 * dados["S"] * (dados["Cl"]) * 1.14

        if L[i+1] < w[j]:
            Fr[i + 1] = mi * abs(L[i + 1] - w[j])
            ay[i + 1] = 0
            vy[i + 1] = 0
            y[i + 1] = 0
        else:
            Fr[i + 1] = 0
            ay[i + 1] = (L[i + 1] - w[j]) / m[j]
            vy[i + 1] = vy[i] + ay[i] * h
            y[i + 1] = y[i] + vy[i + 1] * h

    ax[i + 1] = (T[i + 1] - D[i + 1] - Fr[i + 1]) / m[j]
    i = i + 1

    print("Altura: ", y[i]*100, "cm")
    print("Peso:", w[j]/g, "Kgf")


print('-'*15, "LIMITE DE PISTA: 55m", '-'*15)
print()
print('-'*5, "Sustentação: ", L[i]/g, "Kgf")
print('-'*5, "Tempo: ", t[i], "s")
print('-'*5, "Altura: ", y[i]*100, "cm")
print ('-'*5, "MTOW: ", w[j]/g, "Kg")
print('-'*5, "Peso Vazio: ", PVatual/1000, "Kg")
print('-'*5, "Carga Paga: ", CP - (PVatual/1000), "Kg")
