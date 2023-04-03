import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f:
    dados = json.load(f)


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

    # Coeficiente angular da curva de momento de arfagem gerado pela fuselagem
    coef_ang_curva_momento_arf = (1 / (36.5 * area_da_asa * corda_media_asa)) * dados[modelo]["soma1"]

    # Coeficiente de momento de arfagem gerado pela fuselagem para o ângulo de ataque nulo
    coef_momento_arf_ang_0 = (dados[modelo]["fatores_correcao_fuselagem"]
             / (36.5 * area_da_asa * corda_media_asa)) * dados[modelo]["soma2"]

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


def margem_estatica(modelo_asa, ponto_neutro, hcg):
    # Quanto maior a Margem Estatística, maior será a estabilidade
    # 10% < Margem Estatística < 20%  ->  Boa Estabilidade e Manobrabilidade
    return ponto_neutro - (hcg * 100)


def calcular_estabilidade(modelo_asa, modelo_empenagem_horizontal, modelo_fuselagem, hcg_inicial, hcg_final):
    # Contribuições
    cont_emp_horizontal = contribuicao_empenagem_horizontal(modelo_empenagem_horizontal)
    cont_fuselagem = contribuicao_fuselagem(modelo_fuselagem)

    # Inicialização de variáveis
    hcg = hcg_inicial
    resultados = []

    # Variação do Hcg
    while hcg <= hcg_final+0.001:
        cont_asa = contribuicao_asa(modelo_asa, hcg)
        cont_total = contribuicao_total(cont_asa, cont_emp_horizontal, cont_fuselagem)

        # Teste de estabilidade
        estabilidade = teste_estabilidade(cont_total)
        if estabilidade:
            # Ponto neutro e Margem Estática
            pnt_neutro = ponto_neutro(cont_emp_horizontal, cont_fuselagem, modelo_asa)
            mrgm_estatica = margem_estatica(modelo_asa, pnt_neutro, hcg)

            resultados.append({"hcg": hcg, "contribuicao_asa": cont_asa,
                               "contribuicao_emp_horizontal": cont_emp_horizontal,
                               "contribuicao_fuselagem": cont_fuselagem, "ponto_neutro": pnt_neutro,
                               "margem_estatica": mrgm_estatica, "estabilidade": estabilidade})

        # Aumento do Hcg
        hcg += 0.01

    return resultados


def exibir_resultados(resultados):
    for i in resultados:
        for j in i:
            if j == "hcg":
                print(f"\33[92mHcg - {i[j]} \33[m")
            else:
                print(f"{j} - {i[j]}")
        print()


# -=-=- OUTPUT -=-=-
exibir_resultados(calcular_estabilidade("asa_2022", "empenagem_horizontal_2022", "fuselagem_2022", 0.25, 0.33))
