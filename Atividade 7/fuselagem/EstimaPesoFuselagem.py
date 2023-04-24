# -------------------- Inputs

# Densidades: nucleo = g/mm3 ; fibra = g/mm2
# Espessuras: Fibra = *2 = Usada em cada lado
# Área da Peça: mm2

densidade_nucleo = 0.0006
densidade_fibra = 0.0002
densidade_da_cola = 0
area_da_peca = 90000
espessura_do_nucleo = 10
espessura_da_fibra = 2.7
configuracao_do_aviao = "biplano"


# -------------------- Código Principal para Massa da Fuselagem:
massa_fibra = (espessura_da_fibra * area_da_peca) * densidade_fibra
massa_nucleo = (espessura_do_nucleo * area_da_peca) * densidade_nucleo

massa_total = massa_fibra + massa_nucleo


# -------------------- Conversão de escrita para leitura de String:
minusculo = configuracao_do_aviao.lower()


# -------------------- Adição de Desvio Padrão à massa
if minusculo == "monoplano":
    peso = massa_total * 1.05
    print("Estimativa de Peso da Fuselagem Monoplano: ", peso)

if minusculo == "biplano":
    peso = massa_total * 1.05
    print("Estimativa de Peso da Fuselagem Biplano: ", peso)