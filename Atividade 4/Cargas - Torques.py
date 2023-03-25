import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f: 
    dados = json.load(f)

# -------------------------------------- Torque do Aileron ----------------------------------------------------

# Área do Aileron
area_aileron = dados["aileron"]["base_aileron"] * dados["aileron"]["altura_aileron"]

# Centróide
centroide_base = dados["aileron"]["base_aileron"] / 2
centroide_altura = dados["aileron"]["altura_aileron"] / 2

# Cálculo da Força
forca = (dados["aileron"]["n_maximo"] * dados["aileron"]["w_aileron"] * area_aileron) / dados["aileron"]["area_asa"]

# Corda no ponto do centróide
corda_centroide = dados["aileron"]["altura_aileron"] * 100

# Cálculo da Distância do Braço do retângulo
# TODO: conferir se a divisão é por 2 ou por 3
distancia_retangulo = corda_centroide / 2

# Cálculo do Torque do Aileron (T = F * d) / 2 - Biplano
torqueA = (forca * distancia_retangulo) / 2

# Output:
print("Distância: ", distancia_retangulo, "cm")
print("Força: ", forca, "kgf")
print("Torque: ", torqueA, "kgf.cm")

# -------------------------------------- Torque do Profundor ----------------------------------------------------

# Área do Profundor
print()

# Carregamento de pressão na maior corda da eh em kgf (W)
w_empenagem_horizontal = (2 * dados["profundor"]["maior_carga_eh"]) \
                         / dados["profundor"]["corda_empenagem_horizontal"] / 9.81

# Carregamento de pressão na maior corda do profundor (W')
w_profundor = (w_empenagem_horizontal * dados["profundor"]["corda_profundor"]) \
              / dados["profundor"]["corda_empenagem_horizontal"]

# Força do Profundor
forca_profundor = (dados["profundor"]["corda_profundor"] * w_profundor) / 2

# Distância do Braço
# TODO: conferir se é a altura ou a corda do profundor
distancia_bracoP = dados["profundor"]["altura_profundor"] * 100 / 3

# Torque do Profundor (T = F * d)
torqueP = forca_profundor * distancia_bracoP

print("Distância: ", distancia_bracoP, "cm")
print("Força: ", forca_profundor, "kgf")
print("Torque do Profundor: ", torqueP, "kgf.cm")

# --------------------------------------- Torque do Leme ----------------------------------------------------

print()
# Proporção de Área entre Empenagem Vertical e Leme
area = dados["leme"]["area_leme"] / dados["leme"]["area_empenagem_vertical"]
print(area)

# Cálculo da Força do Leme
# TODO: conferir divisão pela gravidade
forca_leme = area * dados["leme"]["carga_ev_rajada"] / 9.81

# Distância do braço
distancia_bracoL = dados["leme"]["altura_leme"] * 100 / 2

# Torque do Leme
torqueL = forca_leme * distancia_bracoL

print("Distância: ", distancia_bracoL, "cm")
print("Força: ", forca_leme, "kgf")
print("Torque do Leme: ", torqueL, "kgf.cm")
