import json
import matplotlib.pyplot as plt

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

# Forçando a entrada no while
i = 0
j = 0
y = [0]

m = [5]
w = [m[0] * g]

while y[i] < 0.70 or y[i] > 0.75:

    # As condições iniciais devem resetar a cada iteração

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
    CP = w[j] / g

    print("Número de Iteração: ", j)
    w.append(m[j]*g)
    m.append(m[j] + 0.01)

    # Repetição com base no comprimento da pista
    while x[i] < xlim:
        t.append(t[i] + h)
        vx.append(vx[i] + ax[i] * h)
        x.append(x[i] + vx[i + 1] * h)
        T.append((47.782 - (vx[0] ** 2)) * f)
        D.append(0.5 * r * vx[i + 1] ** 2 * dados["S"] * (dados["Cd0"] + dados["K"] * dados["Cl"] ** 2))
        L.append(0.5 * r * vx[i + 1] ** 2 * dados["S"] * (dados["Cl"]) * 1.14)

        if L[i+1] < w[j]:
            Fr.append(mi * abs(L[i + 1] - w[j]))
            ay.append(0)
            vy.append(0)
            y.append(0)
        else:
            Fr.append(0)
            ay.append((L[i + 1] - w[j]) / m[j])
            vy.append(vy[i] + ay[i] * h)
            y.append(y[i] + vy[i + 1] * h)

        ax.append((T[i + 1] - D[i + 1] - Fr[i + 1]) / m[j])
        i += 1

    print("Altura: ", y[i]*100, "cm")
    print("Peso:", w[j]/g, "Kgf")
    print()

    CP = w[j] / g
    j += 1


print('-'*15, "LIMITE DE PISTA: 55m", '-'*15)
print()
print('-'*5, "Sustentação: ", L[i]/g, "Kgf")
print('-'*5, "Tempo: ", t[i], "s")
print('-'*5, "Altura: ", y[i]*100, "cm")
print('-'*5, "MTOW: ", w[j]/g, "Kg")
print('-'*5, "Peso Vazio: ", PVatual/1000, "Kg")
print('-'*5, "Carga Paga: ", CP - (PVatual/1000), "Kg")
print()


# ------------------------- Gráficos -------------------------
# Gráfico arrasto, tração, sustentação, atrito e peso pelo tempo
plt.figure(1)
plt.plot(t, D, label="Arrasto")
plt.plot(t, T, label="Tração")
plt.plot(t, L, label="Sustentação")
plt.plot(t, Fr, label="Atrito")
#plt.plot(t, w, label="Peso")  -> O tamanho do vetor w é diferente do tamanho dos outros vetores
plt.xlabel("Tempo (s)")
plt.ylabel("Força (N)")
plt.title("Cinética da Aeronave")
plt.legend()
plt.grid()

plt.savefig("graficos/Cinética da Aeronave.png")
plt.close()

# Gráfico posição x y, velocidade x y e aceleração x y pelo tempo
plt.figure(2)
plt.subplot(3, 1, 1)
plt.plot(t, x, label="Posição x")
plt.plot(t, y, label="Posição y")
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (m)")
plt.title("Cinemática da Aeronave")
plt.legend()
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(t, vx, label="Velocidade x")
plt.plot(t, vy, label="Velocidade y")
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (m/s)")
plt.legend()
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(t, ax, label="Aceleração x")
plt.plot(t, ay, label="Aceleração y")
plt.xlabel("Tempo (s)")
plt.ylabel("Aceleração (m/s²)")
plt.legend()
plt.grid()

plt.savefig("graficos/Cinemática da Aeronave.png")
plt.close()
