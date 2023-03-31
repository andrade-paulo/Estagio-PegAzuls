import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f:
    dados = json.load(f)


def torque_aileron(modelo):
    area = dados[modelo]["base"] * dados[modelo]["altura"]

    centroide_base = dados[modelo]["base"] / 2
    centroide_altura = dados[modelo]["altura"] / 2

    forca = (dados[modelo]["massa"] * dados[modelo]["fator_carga_maxima"] * area) \
            / dados[modelo]["area_asa"]

    corda_centroide = dados[modelo]["altura"] * 100

    distancia_braco = corda_centroide / 3

    # Cálculo do Torque do Aileron (T = F * d) / 2 - Biplano
    torque = (forca * distancia_braco) / 2

    # Resultados
    return {"area": area, "centroide_base": centroide_base, "centroide_altura": centroide_altura, "forca": forca,
            "corda_centroide": corda_centroide, "distancia_braco": distancia_braco, "torque": torque}


def torque_profundor(modelo):
    carregamento_de_pressao_emp_hor = (2 * dados[modelo]["maior_carga_emp_hor"]) \
                                      / dados[modelo]["corda_emp_hor"] / 9.81

    carregamento_de_pressao_profundor = (carregamento_de_pressao_emp_hor * dados[modelo]["corda"]) \
                  / dados[modelo]["corda_emp_hor"]

    forca = (dados[modelo]["corda"] * carregamento_de_pressao_profundor) / 2

    distancia_braco = dados[modelo]["altura"] * 100 / 3

    torque = forca * distancia_braco

    # Resultados
    return {"carregamento_de_pressao_emp_hor": carregamento_de_pressao_emp_hor,
            "carregamento_de_pressao_profundor": carregamento_de_pressao_profundor,
            "forca": forca, "distancia_braco": distancia_braco, "torque": torque}


def torque_leme(modelo):
    area = dados[modelo]["area"] / dados[modelo]["area_emp_vert"]

    forca = area * dados[modelo]["carga_rajada_emp_vert"] / 9.81

    distancia_braco = dados[modelo]["altura"] * 100 / 2

    torque = forca * distancia_braco

    # Resultados
    return {"area": area, "forca": forca, "distancia_braco": distancia_braco, "torque": torque}


def exibir(conteudo):
    for i in conteudo:
        print(f"{i}: {conteudo[i]}")
    print()


# -=-=- OUTPUT -=-=-
print("\33[92m-=-=- Modelo 2022 -=-=-\33[m")
print("-> Aileron")
exibir(torque_aileron("aileron2022"))

print("-> Profundor")
exibir(torque_profundor("profundor2022"))

print("-> Leme")
exibir(torque_leme("leme2022"))

print("\33[92m-=-=- Modelo 2021 -=-=-\33[m")
print("-> Aileron")
exibir(torque_aileron("aileron2021"))

print("-> Profundor")
exibir(torque_profundor("profundor2021"))

print("-> Leme")
exibir(torque_leme("leme2021"))
