from math import pi
import json

# Carregamento das informações do JSON na variável dados
with open(r'.\inputs.json', 'r') as f:
    dados = json.load(f)


# -=-=-=-=-=- FUNÇÕES -=-=-=-=-=-

# Função para generalizar os cálculos das integrais
def integral(valores_referencia):  # Recebe uma lista
    resultados_por_grau = [0]

    for i in range(1, len(valores_referencia) + 1):  # Adapta dinamicamente conforme a quantidade de itens
        resultados_por_grau.append(valores_referencia[i - 1] / i)
        resultados_por_grau[0] += -(
                    resultados_por_grau[i] * pow(dados["prop_comuns"]["envergadura"], i))  # Valor máximo

    return resultados_por_grau  # Retorna uma lista


# Função para calcular as longarinas
def calcular_longarina(material, configuracao):
    # Integrais
    valor_por_grau = [112.4, 31.93, -589.8, 2607, -5689, 5779, -2231]  # O índice corresponde ao grau
    esforco_cortante = integral(valor_por_grau)
    momento_fletor = integral(esforco_cortante)

    # Exibição dos valores máximos (sempre no índice 0)
    print(f'Esforço cortante máximo: {esforco_cortante[0]}')
    print(f'Momento fletor máximo: {momento_fletor[0]}')

    # Tensão admissível
    tensao_admissivel_flexao = dados[material]["tensao_esc_flexao"] / dados["prop_comuns"]["fator_seguranca"]
    tensao_admissivel_cisalhamento = dados[material]["tensao_esc_cisalhamento"] \
                                     / dados["prop_comuns"]["fator_seguranca"]

    # Dados iniciais para o 'loop'
    tensao_cisalhamento = tensao_admissivel_cisalhamento + 1
    tensao_flexao = tensao_admissivel_flexao + 1

    # Variáveis usadas no top10
    contador = 1
    top10 = []

    if configuracao == "circular":  # Tipo circular
        raio_externo = 6

        # Procura pelo melhor peso
        while contador <= 10:
            # Calculos das dimensões
            raio_interno = raio_externo - 1

            diametro_externo = 2 * raio_externo
            diametro_interno = 2 * raio_interno

            area_circular = ((pow(raio_externo, 2) * pi) - (pow(raio_interno, 2) * pi))

            massa = dados["prop_comuns"]["envergadura"] * 2000 * area_circular * dados[material]["densidade"]

            # Cálculos das propriedades físicas
            inercia = (pi / 64) * (pow(diametro_externo, 4) - pow(diametro_interno, 4))

            tensao_cisalhamento = \
                ((4 * (-esforco_cortante[0])) / (3 * area_circular)) * \
                ((pow(raio_externo, 2) + raio_externo * raio_interno + pow(raio_interno, 2)) /
                 (pow(raio_externo, 2) + pow(raio_interno, 2)))

            tensao_flexao = momento_fletor[0] * 1000 * raio_externo / inercia

            raio_externo += 0.00001  # Novo raio a ser testado

            if tensao_cisalhamento < tensao_admissivel_cisalhamento and tensao_flexao < tensao_admissivel_flexao:
                contador += 1  # Conta a quantidade de casos registrados para o top10

                top10.append({"tensao flexivel": tensao_flexao, "tensao_cisalhamento": tensao_cisalhamento,
                              "tensao_admissivel_cisalhamento": tensao_admissivel_cisalhamento,
                              "tensao_admissivel_flexao": tensao_admissivel_flexao,
                              "inercia": inercia, "diametro_externo": diametro_externo,
                              "area_circular": area_circular, "massa": massa})

    elif configuracao == "caixao":  # Tipo caixão
        largura = 1
        altura = 40

        while contador <= 10:
            # Calculos das dimensões
            area_retangular = largura * altura - ((largura - (2 * dados[material]["espessura"]))
                                                  * (altura - (2 * dados[material]["espessura"])))

            massa = (dados["prop_comuns"]["envergadura"] * 2000 * area_retangular) * dados[material]["densidade"]

            # Cálculos das propriedades físicas
            inercia = ((largura * pow(altura, 3)) / 12) \
                      - (((largura - (2 * dados[material]["espessura"]))
                          * pow((altura - (2 * dados[material]["espessura"])), 3)) / 12)

            tensao_cisalhamento = (1.5 * dados["prop_comuns"]["envergadura"] * area_retangular) / area_retangular

            tensao_flexao = (momento_fletor[0] * 1000 * (altura / 2)) / inercia

            # Acrescenta largura após a altura atingir o máximo
            if altura < 50:
                altura += 0.5  # Nova altura a ser testada
            else:
                largura += 0.01  # Nova largura a ser testada

            if tensao_cisalhamento < tensao_admissivel_cisalhamento and tensao_flexao < tensao_admissivel_flexao:
                contador += 1  # Conta a quantidade de casos registrados para o top10

                top10.append({"tensao flexivel": tensao_flexao, "tensao_cisalhamento": tensao_cisalhamento,
                              "tensao_admissivel_cisalhamento": tensao_admissivel_cisalhamento,
                              "tensao_admissivel_flexao": tensao_admissivel_flexao,
                              "inercia": inercia, "largura": largura, "altura": altura,
                              "area_retangula": area_retangular, "massa": massa})

    elif configuracao == "retangular":  # Tipo retangular
        largura = 0.5
        altura = 20

        while contador <= 10:
            # Calculos das dimensões
            area_retangular = largura * altura

            massa = (dados["prop_comuns"]["envergadura"] * 2000 * area_retangular) * dados[material]["densidade"]

            # Cálculos das propriedades físicas
            inercia = ((largura * pow(altura, 3)) / 12)

            tensao_cisalhamento = (1.5 * dados["prop_comuns"]["envergadura"] * area_retangular) / area_retangular

            tensao_flexao = (momento_fletor[0] * 1000 * (altura / 2)) / inercia

            # Acrescenta largura após a altura atingir o máximo
            if altura < 50:
                altura += 0.5  # Nova altura a ser testada
            else:
                largura += 0.01  # Nova largura a ser testada

            if tensao_cisalhamento < tensao_admissivel_cisalhamento and tensao_flexao < tensao_admissivel_flexao:
                contador += 1  # Conta a quantidade de casos registrados para o top10

                top10.append({"tensao flexivel": tensao_flexao, "tensao_cisalhamento": tensao_cisalhamento,
                              "tensao_admissivel_cisalhamento": tensao_admissivel_cisalhamento,
                              "tensao_admissivel_flexao": tensao_admissivel_flexao,
                              "inercia": inercia, "largura": largura, "altura": altura,
                              "area_retangula": area_retangular, "massa": massa})

    return top10


# Função para formatar as saídas
def exibir_resultados(lista_de_resultados):
    for i in lista_de_resultados:
        for j in i:
            print(f"{j}: {i[j]}")
        print()


# -=-=-=-=-=- OUTPUTS -=-=-=-=-=-

print("\033[92m-=-=- Alumínio Circular -=-=-\033[0m")
aluminio_circular = calcular_longarina("aluminio", "circular")
exibir_resultados(aluminio_circular)

print("\033[92m-=-=- Alumínio Retangular -=-=-\033[0m")
aluminio_retangular = calcular_longarina("aluminio", "retangular")
exibir_resultados(aluminio_retangular)

print("\033[92m-=-=- Carbono Circular -=-=-\033[0m")
carbono_circular = calcular_longarina("carbono", "circular")
exibir_resultados(carbono_circular)

print("\033[92m-=-=- Balsa Retangular Caixão -=-=-\033[0m")
balsa_caixao = calcular_longarina("balsa", "caixao")
exibir_resultados(balsa_caixao)
