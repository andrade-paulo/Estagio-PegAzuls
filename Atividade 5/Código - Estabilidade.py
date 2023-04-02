import json


# Carregamento das informações do JSON na variável dados
with open(r'C:\Users\Acer\OneDrive\Documentos\Pegazuls\Estagio-Pegazuls\Atividade 5\inputs.json', 'r') as f:
    dados = json.load(f)



#----------------- CONTRIBUIÇÃO DA ASA -----------------
# ---------- Cálculo do Coeficiente Angular da Curva de momento de Arfagem gerado pela Asa --------
c_mAlfaAsa = dados["contribuicao_asa"]["C_angular_curva_CLxAlfa"] * (dados["contribuicao_asa"]["posicao_CG_corda_media"] - dados["contribuicao_asa"]["posicao_centro_aerod_corda_media"])

# ------ Cálculo do Coeficiente de momento de Arfagem gerado pela Asa para o Ângulo de Ataque Nulo -----
c_m0Asa = dados["contribuicao_asa"]["C_momento_redor_centro"] + dados["contribuicao_asa"]["C_sustentacao_angulo_ataque_nulo"] * (dados["contribuicao_asa"]["posicao_CG_corda_media"] - dados["contribuicao_asa"]["posicao_centro_aerod_corda_media"])




#----------------- CONTRIBUIÇÃO DA EMPENAGEM HORIZONTAL -----------------
volume_cauda_horizontal = dados["contribuicao_empenagem_horizontal"]["volume_cauda"]
eficiencia_cauda_horizontal = dados["contribuicao_empenagem_horizontal"]["eficiencia_cauda"]
coenfiente_angular_EH = dados["contribuicao_empenagem_horizontal"]["C_angular_curva_CLxAlfa_EH"]
derivada = dados["contribuicao_empenagem_horizontal"]["derivada_angulo_ataque_induzido / angulo_ataque"]
angulo_incidencia_asa = dados["contribuicao_empenagem_horizontal"]["i_w"]
angulo_incidencia_EH = dados["contribuicao_empenagem_horizontal"]["i_t"]
angulo_ataque_induzido_0 = dados["contribuicao_empenagem_horizontal"]["E0"]
C_sustentacao_EH_0 = dados["contribuicao_empenagem_horizontal"]["C_L0t"]
Ct = dados["contribuicao_empenagem_horizontal"]["corda_media_aerod_empenag_horiz"]
Lt = dados["contribuicao_empenagem_horizontal"]["L_t"]
C_mact = dados["contribuicao_empenagem_horizontal"]["C_momento_redor_centro_aerod_empenag_horiz"]

# -------- Coeficiente Angular da Curva de Momento de Arfagem gerado pela Empenagem H ------------
c_mAlfaEh = - volume_cauda_horizontal * eficiencia_cauda_horizontal * coenfiente_angular_EH * (1 - derivada)

# -------- Coeficiente de Momento de Arfagem gerado pela EH para o Ângulo de Ataque Nulo ------------
c_m0Eh = (volume_cauda_horizontal * eficiencia_cauda_horizontal * coenfiente_angular_EH * (angulo_incidencia_asa - angulo_incidencia_EH + angulo_ataque_induzido_0)) - (volume_cauda_horizontal * eficiencia_cauda_horizontal * C_sustentacao_EH_0) + ((Ct / Lt) * volume_cauda_horizontal * eficiencia_cauda_horizontal * C_mact)




#----------------- CONTRIBUIÇÃO DA FUSELAGEM -----------------
area_da_asa = dados["contribuicao_fuselagem"]["area_asa"]
corda_media_asa = dados["contribuicao_fuselagem"]["corda_media_aerod_asa"]

# ---------- Coeficiente Angular da Curva de Momento de Arfagem gerado pela Fuselagem -------
c_mAlfaF = (1 / (36.5 * area_da_asa * corda_media_asa)) * dados["contribuicao_fuselagem"]["soma1"] 

# ---------- Coeficiente de momento de Arfagem gerado pela Fuselagem para o ângulo de Ataque Nulo -------
c_m0F = (dados["contribuicao_fuselagem"]["fatores_correcao_fuselagem"]/(36.5 * area_da_asa * corda_media_asa)) * dados["contribuicao_fuselagem"]["soma2"]




#----------------- CONTRIBUIÇÃO TOTAL -----------------
# ----------- Coeficiente Angular da Curva de Momento de Arfagem Total -------
c_mAlfa = c_mAlfaAsa + c_mAlfaEh + c_mAlfaF

#------------ Coeficiente de momento de Arfagem para o ângulo de Ataque Nulo Total ------
c_m0 = c_m0Asa + c_m0Eh + c_m0F



# -------------------------- TESTE DE ESTABILIDADE ----------------------------
if  c_mAlfa < 0 and c_m0 > 0 :
    estabilidade = "Avião Estável"

else: 
    estabilidade = "Avião Instável"

  

# ---------------- Ponto Neutro e Margem Estática -------------------
ponto_neutro_corda_media = dados["contribuicao_asa"]["posicao_centro_aerod_corda_media"] - (c_mAlfaF / dados["contribuicao_asa"]["C_angular_curva_CLxAlfa"]) - (c_mAlfaEh / dados["contribuicao_asa"]["C_angular_curva_CLxAlfa"])
porcentagem = ponto_neutro_corda_media * 100

margem_estatistica = ponto_neutro_corda_media - dados["contribuicao_asa"]["posicao_CG_corda_media"]
porcentagem2 = margem_estatistica * 100

# -=-=- OUTPUT -=-=-

print ()

print ("\33[92m---------- Contribuição da Asa \33[m") 
print ("Coeficiente Angular da Curva de momento de Arfagem : ", c_mAlfaAsa)
print ("Coeficiente de momento de Arfagem para o Ângulo de Ataque Nulo : ", c_m0Asa)

print ()

print ("\33[92m---------- Contribuição da Empenagem Horizontal \33[m") 
print ("Coeficiente Angular da Curva de Momento de Arfagem : ", c_mAlfaEh)
print ("Coeficiente de Momento de Arfagem para o Ângulo de Ataque Nulo : ", c_m0Eh)

print ()

print ("\33[92m---------- Contribuição da Fuselagem \33[m") 
print ("Coeficiente Angular da Curva de Momento de Arfagem  : ", c_mAlfaF)
print ("Coeficiente de momento de Arfagem para o ângulo de Ataque Nulo : ", c_m0F)

print ()

print ("\33[92m---------- Contribuição Total \33[m") 
print ("Coeficiente Angular da Curva de Momento de Arfagem Total : ", c_mAlfa)
print ("Coeficiente de momento de Arfagem para o ângulo de Ataque Nulo Total: ", c_m0)

print ()

# Quanto maior a Margem Estatística, maior será a estabilidade
# 10% < Margem Estatística < 20%  ----  Boa Estabilidade e Manobrabilidade
print ("\033[34m---------- Ponto Neutro e Margem Estática \033[0m") 
print ("Ponto Neutro da Corda Média: %.2f%% " % porcentagem)
print ("Margem Estatística: %.2f%% " % porcentagem2)

print ()

print ("\033[35m---------- Teste de Estabilidade : \033[0m", estabilidade) 
print ()