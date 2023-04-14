import json
import pandas
import matplotlib.pyplot as plt
import math


def carregar_inputs():
    with open("inputs.json") as f:
        return json.load(f)


def calcular_velocidades(vel_inicial, vel_final):
    inputs = carregar_inputs()

    # Inicialização do Dataframe
    resultados = {"Cl": [], "Cd": [], "Tr": [], "Td": [], "Td-Tr": []}
    resultados = pandas.DataFrame(resultados)

    v = vel_inicial
    while v <= vel_final:
        # Cálculos dos resultados
        cl = (2 * inputs["W"]) / (inputs["p"] * inputs["S"] * pow(v, 2))
        cd = inputs["CD0"] + inputs["K"] * pow(cl, 2)
        cl_dividido_cd = cl / cd
        tr = 0.5 * inputs["p"] * pow(v, 2) * inputs["S"] * cd
        td = 0.0079 * pow(v, 2) - 1.4194 * v + 46.229
        tr_menos_td = abs(tr - td)
        pr = v * tr
        pd = v * td
        d0 = 0.5 * inputs["p"] * inputs["S"] * inputs["CD0"] * pow(v, 2)
        di = 0.5 * inputs["p"] * inputs["S"] * inputs["K"] * pow(cl, 2) * pow(v, 2)

        # Adição dos resultados ao Dataframe
        resultados = resultados.append(
            {"v": v, "Cl": cl, "Cd": cd, "Cl/Cd": cl_dividido_cd, "Tr": tr, "Td": td, "Td-Tr": tr_menos_td, "Pr": pr,
             "Pd": pd, "D0": d0, "Di": di}, ignore_index=True)

        v += 0.01  # Atualização da velocidade

    return resultados


def estimar_velocidades(velocidades):
    inputs = carregar_inputs()

    # Inicialização do Dataframe
    resultados = {"Vmax": [], "Vmin": [], "Vstall": [], "Vcru": [], "Vd": []}
    resultados = pandas.DataFrame(resultados)

    # Cálculos dos resultados
    vmax = velocidades.loc[velocidades.loc[velocidades["v"] >= 15, "Td-Tr"].idxmin(), "v"]
    vmin = velocidades.loc[velocidades.loc[velocidades["v"] < 15, "Td-Tr"].idxmin(), "v"]
    vstall = math.sqrt((2 * inputs["W"]) / (inputs["p"] * inputs["S"] * inputs["Clmax"]))
    vcru = vmax * 0.9
    vd = vmax * 1.25

    # Adição dos resultados ao Dataframe
    resultados = resultados.append({"Vmax": vmax, "Vmin": vmin, "Vstall": vstall,
                                    "Vcru": vcru, "Vd": vd}, ignore_index=True)

    return resultados


def exportar_resultados(tabela, outputs_finais, nome_arquivo):
    # Exportar resultados para Excel
    writer = pandas.ExcelWriter(f"{nome_arquivo}.xlsx", engine="xlsxwriter")
    tabela.to_excel(writer, sheet_name="Velocidades")
    outputs_finais.to_excel(writer, sheet_name="Outputs")
    writer.save()


def gerar_graficos(valores):
    # Gráficos tr, td e v
    titulo = "Tr x Td x v"
    plt.plot(valores["v"], valores["Tr"], label="Tr")
    plt.plot(valores["v"], valores["Td"], label="Td")
    plt.title(titulo)
    plt.xlabel("v (m/s)")
    plt.ylabel("Tr e Td (N)")
    plt.grid()
    plt.legend()
    plt.savefig(f"graficos/{titulo}.png")
    plt.close()

    # Gráficos pr, pd e v
    titulo = "Pr x Pd x v"
    plt.plot(valores["v"], valores["Pr"], label="Pr")
    plt.plot(valores["v"], valores["Pd"], label="Pd")
    plt.title(titulo)
    plt.xlabel("v (m/s)")
    plt.ylabel("Pr e Pd (N)")
    plt.grid()
    plt.legend()
    plt.savefig(f"graficos/{titulo}.png")
    plt.close()

    # Gráficos cl, cd e v
    titulo = "Cl_Cd x v"
    plt.plot(valores["v"], valores["Cl/Cd"], label="Cl")
    plt.title("Cl / Cd x v")
    plt.xlabel("v (m/s)")
    plt.ylabel("Cl/Cd (N)")
    plt.grid()
    plt.legend()
    plt.savefig(f"graficos/{titulo}.png")
    plt.close()

    # Gráfico D0 e Di
    titulo = "D0 x Di x v"
    plt.plot(valores["v"], valores["D0"], label="D0")
    plt.plot(valores["v"], valores["Di"], label="Di")
    plt.title(titulo)
    plt.xlabel("v (m/s)")
    plt.ylabel("D0 e Di (N)")
    plt.grid()
    plt.legend()
    plt.savefig(f"graficos/{titulo}.png")
    plt.close()


# Tabelas para planilha e gráficos
tabela_velocidades = calcular_velocidades(0.01, 30.5)
tabela_resumida = calcular_velocidades(6, 35)

# Formatação do output
outputs = estimar_velocidades(tabela_velocidades)
gerar_graficos(tabela_resumida)
exportar_resultados(tabela_velocidades, outputs, "resultado")
print("\33[92mCódigo executado com sucesso!\33[m")
print("Confira os resultados no arquivo `resultados.xlsx` e na pasta /graficos")
