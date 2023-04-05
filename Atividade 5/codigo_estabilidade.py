import json
import pandas as pd
import matplotlib.pyplot as plt

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f:
    dados = json.load(f)

# Carregamento do Excel com os dados de entrada
dados_somatorio = pd.read_excel('./inputs_somatorio.xlsx', sheet_name='Planilha1')


def somatorio(valores):
    valores["equacao_1"] = pow(valores["w_f"], 2) * valores["a0w + if"] * valores["delta_x"]
    valores["equacao_2"] = pow(valores["w_f2"], 2) * valores["escoamento por ataque"] * valores["delta_x2"]
    soma1 = valores["equacao_1"].sum()
    soma2 = valores["equacao_2"].sum()

    return {"soma1": soma1, "soma2": soma2}


def contribuicao_asa(modelo, posicao_cg_corda_media):
    # Coeficiente angular da curva de momento de arfagem gerado pela asa
    coef_ang_curva_momento_arf = dados[modelo]["C_angular_curva_CLxAlfa"] \
                                 * (posicao_cg_corda_media
                                    - dados[modelo]["posicao_centro_aerod_corda_media"])

    # Coeficiente de momento de arfagem gerado pela asa para o ângulo de ataque nulo
    coef_momento_arf_ang_0 = dados[modelo]["C_momento_redor_centro"] \
                             + dados[modelo]["C_sustentacao_angulo_ataque_nulo"] \
                             * (posicao_cg_corda_media
                                - dados[modelo]["posicao_centro_aerod_corda_media"])

    return {"coef_ang_curva_momento_arf": coef_ang_curva_momento_arf,
            "coef_momento_arf_ang_0": coef_momento_arf_ang_0}


def contribuicao_empenagem_horizontal(modelo):
    # Atribuição de variáveis
    volume_cauda_horizontal = dados[modelo]["volume_cauda"]
    eficiencia_cauda_horizontal = dados[modelo]["eficiencia_cauda"]
    coenfiente_angular_EH = dados[modelo]["C_angular_curva_CLxAlfa_EH"]
    derivada = dados[modelo]["derivada_angulo_ataque_induzido / angulo_ataque"]
    angulo_incidencia_asa = dados[modelo]["i_w"]
    angulo_incidencia_EH = dados[modelo]["i_t"]
    angulo_ataque_induzido_0 = dados[modelo]["E0"]
    C_sustentacao_EH_0 = dados[modelo]["C_L0t"]
    Ct = dados[modelo]["corda_media_aerod_empenag_horiz"]
    Lt = dados[modelo]["L_t"]
    C_mact = dados[modelo]["C_momento_redor_centro_aerod_empenag_horiz"]

    # Coeficiente angular da curva de momento de arfagem gerado pela empenagem horizontal
    coef_ang_curva_momento_arf = - volume_cauda_horizontal * eficiencia_cauda_horizontal \
                                 * coenfiente_angular_EH * (1 - derivada)

    # Coeficiente de momento de arfagem gerado pela EH para o ângulo de ataque nulo
    coef_momento_arf_ang_0 = (volume_cauda_horizontal * eficiencia_cauda_horizontal * coenfiente_angular_EH
                              * (angulo_incidencia_asa - angulo_incidencia_EH + angulo_ataque_induzido_0)) \
                             - (volume_cauda_horizontal * eficiencia_cauda_horizontal * C_sustentacao_EH_0) \
                             + ((Ct / Lt) * volume_cauda_horizontal * eficiencia_cauda_horizontal * C_mact)

    return {"coef_ang_curva_momento_arf": coef_ang_curva_momento_arf,
            "coef_momento_arf_ang_0": coef_momento_arf_ang_0}


def contribuicao_fuselagem(modelo):
    area_da_asa = dados[modelo]["area_asa"]
    corda_media_asa = dados[modelo]["corda_media_aerod_asa"]

    # Somatório da tabela Excel
    somas = somatorio(dados_somatorio)

    # Coeficiente angular da curva de momento de arfagem gerado pela fuselagem
    coef_ang_curva_momento_arf = (1 / (36.5 * area_da_asa * corda_media_asa)) * somas["soma1"]

    # Coeficiente de momento de arfagem gerado pela fuselagem para o ângulo de ataque nulo
    coef_momento_arf_ang_0 = (dados[modelo]["fatores_correcao_fuselagem"]
                              / (36.5 * area_da_asa * corda_media_asa)) * somas["soma2"]

    return {"coef_ang_curva_momento_arf": coef_ang_curva_momento_arf,
            "coef_momento_arf_ang_0": coef_momento_arf_ang_0}


def contribuicao_total(cont_asa, cont_empenagem_horizontal, cont_fuselagem):
    # Coeficiente angular da curva de momento de arfagem total
    coef_ang_curva_momento_arf = cont_asa["coef_ang_curva_momento_arf"] \
                                 + cont_empenagem_horizontal["coef_ang_curva_momento_arf"] \
                                 + cont_fuselagem["coef_ang_curva_momento_arf"]

    # Coeficiente de momento de arfagem para o ângulo de ataque nulo total
    coef_momento_arf_ang_0 = cont_asa["coef_momento_arf_ang_0"] \
                             + cont_empenagem_horizontal["coef_momento_arf_ang_0"] \
                             + cont_fuselagem["coef_momento_arf_ang_0"]

    return {"coef_ang_curva_momento_arf": coef_ang_curva_momento_arf, "coef_momento_arf_ang_0": coef_momento_arf_ang_0}


def teste_estabilidade(total):
    return total["coef_ang_curva_momento_arf"] < 0 and total["coef_momento_arf_ang_0"] > 0


def ponto_neutro(cont_empenagem_horizontal, cont_fuselagem, modelo_asa):
    return (dados[modelo_asa]["posicao_centro_aerod_corda_media"]
            - (cont_fuselagem["coef_ang_curva_momento_arf"] / dados[modelo_asa]["C_angular_curva_CLxAlfa"])
            - (cont_empenagem_horizontal["coef_ang_curva_momento_arf"]
               / dados[modelo_asa]["C_angular_curva_CLxAlfa"])) * 100


def margem_estatica(ponto_neutro, hcg):
    # Quanto maior a Margem Estatística, maior será a estabilidade
    # 10% < Margem Estatística < 20%  ->  Boa Estabilidade e Manobrabilidade
    return ponto_neutro - (hcg * 100)


def calcular_estabilidade(modelo_asa, modelo_empenagem_horizontal, modelo_fuselagem, hcg_inicial, hcg_final):
    # Contribuições
    cont_emp_horizontal = contribuicao_empenagem_horizontal(modelo_empenagem_horizontal)
    cont_fuselagem = contribuicao_fuselagem(modelo_fuselagem)

    # Inicialização de variáveis
    hcg = hcg_inicial
    resultados = {}

    # Variação do Hcg
    while hcg <= hcg_final:
        cont_asa = contribuicao_asa(modelo_asa, hcg)
        cont_total = contribuicao_total(cont_asa, cont_emp_horizontal, cont_fuselagem)

        # Teste de estabilidade
        estabilidade = teste_estabilidade(cont_total)
        if estabilidade:
            # Ponto neutro e Margem Estática
            pnt_neutro = ponto_neutro(cont_emp_horizontal, cont_fuselagem, modelo_asa)
            mrgm_estatica = margem_estatica(pnt_neutro, hcg)

            resultados[f"Hcg_{hcg}"] = {"Cmaw": cont_asa["coef_ang_curva_momento_arf"],
                                        "Cm0w": cont_asa["coef_momento_arf_ang_0"],
                                        "Cmat": cont_emp_horizontal["coef_ang_curva_momento_arf"],
                                        "Cm0t": cont_emp_horizontal["coef_momento_arf_ang_0"],
                                        "Cmaf": cont_fuselagem["coef_ang_curva_momento_arf"],
                                        "Cm0f": cont_fuselagem["coef_momento_arf_ang_0"],
                                        "Cm": cont_total["coef_ang_curva_momento_arf"],
                                        "Cm0": cont_total["coef_momento_arf_ang_0"],
                                        "Ponto_Neutro": pnt_neutro,
                                        "Margem_Estatica": mrgm_estatica,
                                        "Estabilidade": estabilidade}

        # Aumento do Hcg
        hcg += 0.01
        hcg = float("{:.4f}".format(hcg))  # Correção da imprecisão do Python para 4 número decimais

    return pd.DataFrame.from_dict(resultados)


def grafico_cm_por_alfa(coef_ang_curva_momento_arf, coef_momento_arf_ang_0, modelo):
    # Definição dos valores para o gráfico
    alfa = range(-5, 20)
    cm = [coef_momento_arf_ang_0 + coef_ang_curva_momento_arf * a for a in alfa]

    plt.plot(alfa, cm)
    plt.title(f"Contribuição {modelo}")
    plt.xlabel("Ângulo de Ataque")
    plt.ylabel("Momento de Arfagem")
    plt.grid()

    # Salvar gráfico na pasta graficos
    plt.savefig(f"graficos/{modelo}.png")

    plt.close()  # Deve-se fechar o gráfico para não consumir memória


def exportar_resultados(resultados, nome_arquivo):
    # Exportar resultados para Excel
    writer = pd.ExcelWriter(f"{nome_arquivo}.xlsx", engine="xlsxwriter")
    resultados.to_excel(writer, sheet_name="Resultados")
    writer.save()


# -=-=- OUTPUT -=-=-
casos_estaveis = calcular_estabilidade("asa_2022", "empenagem_horizontal_2022", "fuselagem_2022", 0.25, 0.33, )
exportar_resultados(casos_estaveis, "casos_estaveis")

# Gráficos
for caso in casos_estaveis.columns:  # Vários gráficos da asa devido à variação do Hcg
    grafico_cm_por_alfa(casos_estaveis.loc["Cmaw"][caso], casos_estaveis.loc["Cm0w"][caso], f"Asa {caso}")

grafico_cm_por_alfa(casos_estaveis.loc["Cmat"][0], casos_estaveis.loc["Cm0t"][0], "Empenagem Horizontal")
grafico_cm_por_alfa(casos_estaveis.loc["Cmaf"][0], casos_estaveis.loc["Cm0f"][0], "Fuselagem")
grafico_cm_por_alfa(casos_estaveis.loc["Cm"][0], casos_estaveis.loc["Cm0"][0], "Total")
