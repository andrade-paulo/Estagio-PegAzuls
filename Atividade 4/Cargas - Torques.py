import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f: 
    dados = json.load(f)


# -------------------------------------- Torque do Aileron ----------------------------------------------------

# Área do Aileron
baseA = dados["aileron"]["base_aileron"]
alturaA = dados["aileron"]["altura_aileron"]
area_aileron =  baseA * alturaA

# Centróide
centroide_base = baseA / 2
centroide_altura = alturaA / 2

# Cálculo da Força ()
forca = (dados["aileron"]["n_maximo"] * dados["aileron"]["w_aileron"] * area_aileron) / dados["aileron"]["area_asa"]

# Cálculo da Distância do Braço do retângulo
distancia_retangulo = centroide_altura

# Cálculo do Torque do Aileron (T = F * d) / 2 - Biplano

torqueA = (forca * distancia_retangulo) / 2

# Opcional:
print ("Área do Aileron: ", area_aileron, "Centímetros ao Quadrado")
print ("Valores do Centróide - Base e Altura: ", centroide_base, " e ", centroide_altura )
print ("Torque do Aileron Biplano: ", torqueA, "KgFCm")



# -------------------------------------- Torque do Profundor ----------------------------------------------------

corda_eh = dados["profundor"]["corda_empenagem_horizontal"]
p_total = dados["profundor"]["maior_carga_eh"]
ce_profundor = dados ["profundor"]["corda_profundor"]
baseP = dados ["profundor"]["base_profundor"]
alturaP = dados ["profundor"]["altura_profundor"]

# Área do Profundor
area_profundor = baseP * alturaP

# Carregamento de pressão na maior corda da eh em kgf (W)
w_empenagem_horizontal = (2 * p_total) / corda_eh

# Carregamento de pressão na maior corda do profundor (W')
w_profundor = (w_empenagem_horizontal * ce_profundor) / corda_eh

# Força do Profundor
forca_profundor = (ce_profundor * w_profundor) / 2

# Distância do Braço
distancia_bracoP = alturaP / 3

# Torque do Profundor (T = F * d) 
torqueP = forca_profundor * distancia_bracoP

print ()
print ("Área do Profundor: ", area_profundor, "Centímetros ao Quadrado")
print ("Força e Distância do Braço do Profundor: ", forca_profundor, "e", distancia_bracoP)
print ("Torque do Profundor: ", torqueP, "KgFCm")




# --------------------------------------- Torque do Leme ----------------------------------------------------

baseL = dados ["leme"]["base_leme"]
alturaL = dados ["leme"]["altura_leme"]

# Área 
# Proporção de Área entre Empenagem Vertical e Leme
area = dados["leme"]["area_leme"] / dados["leme"]["area_empenagem_vertical"]

# Cálculo da Força do Leme
forca_leme = area * dados["leme"]["carga_ev_rajada"]

# Torque do Leme
torqueL = forca_leme * (alturaL / 2)


print ()
print ("Torque do Leme: ", torqueL, "KgFCm")