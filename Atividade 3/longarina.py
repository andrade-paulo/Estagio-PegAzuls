from math import pi
import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f:
    dados = json.load(f)


# Função para generalizar os cálculos das integrais
def integral(valores_referencia):  # Recebe uma lista
    resultados_por_grau = [0]

    for i in range(1, len(valores_referencia) + 1):  # Adapta dinamicamente conforme a quantidade de itens
        resultados_por_grau.append(valores_referencia[i - 1] / i)
        resultados_por_grau[0] += -(resultados_por_grau[i] * pow(dados["prop_comuns"]["base"], i))  # Valor máximo

    return resultados_por_grau  # Retorna uma lista


# Integrais
valor_por_grau = [112.4, 31.93, -589.8, 2607, -5689, 5779, -2231]  # O índice corresponde ao grau
esforco_cortante = integral(valor_por_grau)
momento_fletor = integral(esforco_cortante)

# Exibição dos valores máximos (sempre no índice 0)
print('O vetor cortante máximo é', esforco_cortante[0])
print('O momento fletor máximo é', momento_fletor[0])


# -=-=-=- Aluminio Retangular -=-=-=-

if dados["aluminio_circular"]["tensao_esc_flexao"] < dados["aluminio_circular"]["tensao_esc_cisalhamento"]:
    tensao_admissivel = dados["aluminio_circular"]["tensao_esc_flexao"] / dados["prop_comuns"]["fator_seguranca"]
else:
    tensao_admissivel = dados["aluminio_circular"]["tensao_esc_cisalhamento"] / dados["prop_comuns"]["fator_seguranca"]

raio_externo = 12.495
tensao_cisalhamento = tensao_flexao = tensao_admissivel + 1  # Valor inicial do loop

while tensao_cisalhamento > tensao_admissivel or tensao_flexao > tensao_admissivel:  # Força bruta
    # Calculos das dimensões
    raio_interno = raio_externo - 1

    diametro_externo = 2 * raio_externo
    diametro_interno = 2 * raio_interno

    area_circular = ((pow(raio_externo, 2) * pi) - (pow(raio_interno, 2) * pi))

    # Cálculos das propriedades físicas
    inercia = (pi / 64) * (pow(diametro_externo, 4) - pow(diametro_interno, 4))

    tensao_cisalhamento = \
        ((4 * (-esforco_cortante[0])) / (3 * area_circular)) * \
        ((pow(raio_externo, 2) + raio_externo * raio_interno + pow(raio_interno, 2)) /
         (pow(raio_externo, 2) + pow(raio_interno, 2)))

    tensao_flexao = momento_fletor[0] * 1000 * raio_externo / inercia

    raio_externo = raio_externo + 0.00001

    massa = dados["prop_comuns"]["base"] * area_circular * 0.00238

# Output
print()
print(f"""-=-=- Melhor resultado -=-=-
Tensão flexível: {tensao_flexao}
A tensão de cisalhamento: {tensao_cisalhamento}
A tensão admissível: {tensao_admissivel}
Inércia: {inercia}
Diâmetro externo: {diametro_externo}
Área Circular: {area_circular}
Massa: {massa}""")

# -=-=-=-=-=-=-=--=-=-=--=-=-=--=-=-
