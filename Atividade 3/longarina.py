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


def calcular_longarina(configuracao):
    # Integrais
    valor_por_grau = [112.4, 31.93, -589.8, 2607, -5689, 5779, -2231]  # O índice corresponde ao grau
    esforco_cortante = integral(valor_por_grau)
    momento_fletor = integral(esforco_cortante)

    # Exibição dos valores máximos (sempre no índice 0)
    print(f'Esforço cortante máximo: {esforco_cortante[0]}')
    print(f'Momento fletor máximo: {momento_fletor[0]}')

    # Tensão admissível
    tensao_admissivel_flexao = dados[configuracao]["tensao_esc_flexao"] / dados["prop_comuns"]["fator_seguranca"]
    tensao_admissivel_cisalhamento = dados[configuracao]["tensao_esc_cisalhamento"] \
                                     / dados["prop_comuns"]["fator_seguranca"]

    # Dados iniciais para o 'loop'
    tensao_cisalhamento = tensao_admissivel_cisalhamento + 1
    tensao_flexao = tensao_admissivel_flexao + 1

    if "circular" in configuracao:
        raio_externo = 6

        # Procura pelo melhor peso
        while tensao_cisalhamento > tensao_admissivel_cisalhamento or tensao_flexao > tensao_admissivel_flexao:
            # Calculos das dimensões
            raio_interno = raio_externo - 1

            diametro_externo = 2 * raio_externo
            diametro_interno = 2 * raio_interno

            area_circular = ((pow(raio_externo, 2) * pi) - (pow(raio_interno, 2) * pi))

            massa = dados["prop_comuns"]["base"] * 2000 * area_circular * dados[configuracao]["densidade"]

            # Cálculos das propriedades físicas
            inercia = (pi / 64) * (pow(diametro_externo, 4) - pow(diametro_interno, 4))

            tensao_cisalhamento = \
                ((4 * (-esforco_cortante[0])) / (3 * area_circular)) * \
                ((pow(raio_externo, 2) + raio_externo * raio_interno + pow(raio_interno, 2)) /
                 (pow(raio_externo, 2) + pow(raio_interno, 2)))

            tensao_flexao = momento_fletor[0] * 1000 * raio_externo / inercia

            raio_externo += 0.00001  # Novo raio a ser testado

        return {"tensao flexivel": tensao_flexao, "tensao_cisalhamento": tensao_cisalhamento,
                "tensao_admissivel_cislhamento": tensao_admissivel_cisalhamento,
                "tensao_admissivel_flexao": tensao_admissivel_flexao,
                "inercia": inercia, "diametro_externo": diametro_externo,
                "area_circular": area_circular, "massa": massa}

    elif "retangular" in configuracao:
        # TODO: descobrir os limites e proporções
        largura = 1
        altura = 40

        while tensao_cisalhamento > tensao_admissivel_cisalhamento or tensao_flexao > tensao_admissivel_flexao:
            # Calculos das dimensões
            area_retangular = largura * altura

            massa = (dados["prop_comuns"]["base"] * 2000 * area_retangular) * dados[configuracao]["densidade"]

            # Cálculos das propriedades físicas
            inercia = (largura * pow(altura, 3)) / 12

            tensao_cisalhamento = (1.5 * dados["prop_comuns"]["base"] * area_retangular) / area_retangular

            tensao_flexao = (momento_fletor[0] * 1000 * (altura / 2)) / inercia

            altura += 0.01  # Nova altura a ser testada
            largura += 0.01  # Nova largura a ser testada

        return {"tensao flexivel": tensao_flexao, "tensao_cisalhamento": tensao_cisalhamento,
                "tensao_admissivel_cislhamento": tensao_admissivel_cisalhamento,
                "tensao_admissivel_flexao": tensao_admissivel_flexao,
                "inercia": inercia, "largura": largura, "altura": altura,
                "area_retangula": area_retangular, "massa": massa}


print("-=-=- Alumínio Circular -=-=-")
aluminio = calcular_longarina("aluminio_circular")
for i in aluminio:
    print(f"{i}: {aluminio[i]}")

print()

print("-=-=- Balsa Retangular -=-=-")
balsa = calcular_longarina("balsa_retangular")
for i in balsa:
    print(f"{i}: {balsa[i]}")
