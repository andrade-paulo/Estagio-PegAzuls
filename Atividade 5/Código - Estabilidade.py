import json

# Carregamento das informações do JSON na variável dados
with open('./inputs.json', 'r') as f:
    dados = json.load(f)


def contribuicao_asa(modelo):
    # Coeficiente angular da curva de momento de arfagem gerado pela asa
    coef_ang_curva_momento_arf = dados[modelo]["C_angular_curva_CLxAlfa"] \
                                 * (dados[modelo]["posicao_CG_corda_media"]
                                    - dados[modelo]["posicao_centro_aerod_corda_media"])

    # Coeficiente de momento de arfagem gerado pela asa para o ângulo de ataque nulo
    coef_momento_arf_ang_0 = dados[modelo]["C_momento_redor_centro"] \
                             + dados[modelo]["C_sustentacao_angulo_ataque_nulo"] \
                             * (dados[modelo]["posicao_CG_corda_media"]
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


def contribuicao_total(asa, empenagem_horizontal, fuselagem):
    # Coeficiente angular da curva de momento de arfagem total
    coef_ang_curva_momento_arf = asa["coef_ang_curva_momento_arf"] \
                                 + empenagem_horizontal["coef_ang_curva_momento_arf"] \
                                 + fuselagem["coef_ang_curva_momento_arf"]

    # Coeficiente de momento de arfagem para o ângulo de ataque nulo total
    coef_momento_arf_ang_0 = asa["coef_momento_arf_ang_0"] \
                                 + empenagem_horizontal["coef_momento_arf_ang_0"] \
                                 + fuselagem["coef_momento_arf_ang_0"]

    return {"coef_ang_curva_momento_arf": coef_ang_curva_momento_arf, "coef_momento_arf_ang_0": coef_momento_arf_ang_0}


def teste_estabilidade(total):
    if total["coef_ang_curva_momento_arf"] < 0 and total["coef_momento_arf_ang_0"] > 0:
        estabilidade = True
    else:
        estabilidade = False

    return estabilidade


def ponto_neutro(empenagem_horizontal, fuselagem, modelo_asa):
    return (dados[modelo_asa]["posicao_centro_aerod_corda_media"]
           - (fuselagem["coef_ang_curva_momento_arf"] / dados[modelo_asa]["C_angular_curva_CLxAlfa"])
           - (empenagem_horizontal["coef_ang_curva_momento_arf"] / dados[modelo_asa]["C_angular_curva_CLxAlfa"])) * 100


def margem_estatica(modelo_asa, ponto_neutro):
    return ((ponto_neutro / 100) - dados[modelo_asa]["posicao_CG_corda_media"]) * 100

# -=-=- OUTPUT -=-=-

print()

print("\33[92m---------- Contribuição da Asa \33[m")
asa = contribuicao_asa("asa_2022")
print("Coeficiente Angular da Curva de momento de Arfagem : ", asa["coef_ang_curva_momento_arf"])
print("Coeficiente de momento de Arfagem para o Ângulo de Ataque Nulo : ", asa["coef_momento_arf_ang_0"])

print()

emp_horizontal = contribuicao_empenagem_horizontal("empenagem_horizontal_2022")
print("\33[92m---------- Contribuição da Empenagem Horizontal \33[m")
print("Coeficiente Angular da Curva de Momento de Arfagem : ", emp_horizontal["coef_ang_curva_momento_arf"])
print("Coeficiente de Momento de Arfagem para o Ângulo de Ataque Nulo : ", emp_horizontal["coef_momento_arf_ang_0"])

print()

fuselagem = contribuicao_fuselagem("fuselagem_2022")
print("\33[92m---------- Contribuição da Fuselagem \33[m")
print("Coeficiente Angular da Curva de Momento de Arfagem  : ", fuselagem["coef_ang_curva_momento_arf"])
print("Coeficiente de momento de Arfagem para o ângulo de Ataque Nulo : ", fuselagem["coef_momento_arf_ang_0"])

print()

total = contribuicao_total(asa, emp_horizontal, fuselagem)
print("\33[92m---------- Contribuição Total \33[m")
print("Coeficiente Angular da Curva de Momento de Arfagem Total : ", total["coef_ang_curva_momento_arf"])
print("Coeficiente de momento de Arfagem para o ângulo de Ataque Nulo Total: ", total["coef_momento_arf_ang_0"])

print()

# Quanto maior a Margem Estatística, maior será a estabilidade
# 10% < Margem Estatística < 20%  ----  Boa Estabilidade e Manobrabilidade
ponto_neutro = ponto_neutro(emp_horizontal, fuselagem, "asa_2022")
margem_estatica = margem_estatica("asa_2022", ponto_neutro)
print("\033[34m---------- Ponto Neutro e Margem Estática \033[0m")
print("Ponto Neutro da Corda Média: %.2f%% " % ponto_neutro)
print("Margem Estatística: %.2f%% " % margem_estatica)

print()

estabilidade = teste_estabilidade(total)
print("\033[35m---------- Teste de Estabilidade:\033[0m", estabilidade)
print()
