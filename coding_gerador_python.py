# -*- coding: utf-8 -*-
  

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------
# 1. Leitura dos 12 valores mensais
# --------------------------------------------------
def ler_consumo_mensal() -> list[float]:
    """
    Pergunta ao usuário os 12 consumos mensais (kWh) e retorna uma lista de floats.
    """
    valores = []
    print("Digite o consumo mensal (kWh) para cada mês (12 valores).")
    for mes in range(1, 13):
        while True:
            try:
                val = float(input(f"  Mês {mes:02d}: "))
                if val < 0:
                    raise ValueError
                valores.append(val)
                break
            except ValueError:
                print("  Valor inválido. Por favor, informe um número positivo.")
    return valores

# --------------------------------------------------
# 2. Cálculos
# --------------------------------------------------
def calcular_metricas(consumos: list[float]) -> dict:
    
    # Conversão para numpy array para operações vetorizadas
    arr = np.array(consumos)

    # Consumo anual
    anual = arr.sum()

    # Média mensal
    media_mensal = anual / 12.0

    # Média diária (30 dias por mês)
    media_diaria = media_mensal / 30.0

    # Dados climáticos
    hsp = 4.3          # kWh/m²·dia
    eta = 0.85         # Performance Ratio

    # Potência pico (kWp)
    p_pico = media_diaria / (hsp * eta)

    # Bateria – 12h de autonomia (metade do consumo diário)
    energia_autonomia = media_diaria / 2.0          # kWh
    energia_real = energia_autonomia / eta          # kWh
    dod = 0.90                                     # Profundidade de descarga
    capacidade_kwh = energia_real / dod             # kWh total
    # Conversão para Ah (tensão 48V)
    capacidade_ah = (capacidade_kwh * 1000) / 48.0

    return {
        "anual": anual,
        "media_mensal": media_mensal,
        "media_diaria": media_diaria,
        "p_pico": p_pico,
        "capacidade_kwh": capacidade_kwh,
        "capacidade_ah": capacidade_ah,
        "hsp": hsp,
        "eta": eta,
        "energia_autonomia": energia_autonomia,
        "energia_real": energia_real
    }

# --------------------------------------------------
# 3. Visualização
# --------------------------------------------------
def plotar_graficos(consumos: list[float], metricas: dict) -> None:
meses = [f"{i:02d}" for i in range(1, 13)]

    fig = plt.figure(constrained_layout=True, figsize=(12, 6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 3, 3])

    # Barra lateral – consumo mensal
    ax_bar = fig.add_subplot(gs[0, 0])
    ax_bar.bar(meses, consumos, color="#4e79a7")
    ax_bar.set_title("Consumo Mensal (kWh)")
    ax_bar.set_xlabel("Mês")
    ax_bar.set_ylabel("kWh")
    ax_bar.tick_params(axis='x', rotation=45)

    # Gráfico de métricas – linha
    ax_line = fig.add_subplot(gs[0, 1:])
    ax_line.plot(meses, consumos, label="Consumo Mensal", marker='o')
    ax_line.axhline( métricas["media_diaria"], color='g', linestyle='--',
                     label=f"Média Diária ({metrics['media_diaria']:.2f} kWh)")
    ax_line.axhline( métricas["p_pico"] * 1000, color='r', linestyle='-',
                     label=f"Pico Necessário ({metrics['p_pico']:.2f} kWp)")
    ax_line.axhline( metrics["capacidade_kwh"], color='m', linestyle='-.',
                     label=f"Capacidade Bateria ({metrics['capacidade_kwh']:.2f} kWh)")
    ax_line.set_title("Métricas de Dimensionamento")
    ax_line.set_xlabel("Mês")
    ax_line.set_ylabel("kWh / kWp")
    ax_line.legend()
    ax_line.tick_params(axis='x', rotation=45)

    plt.suptitle("Dimensionamento Fotovoltaico – Jandira-SP", fontsize=16)
    plt.show()

# --------------------------------------------------
# 4. Programa principal
# --------------------------------------------------
def main() -> None:
    consumos = ler_consumo_mensal()
    metricas = calcular_metricas(consumos)

    # Exibição dos resultados em texto
    print("\n=== Resultados ===")
    for key, val in metricas.items():
        if isinstance(val, float):
            print(f"{key:20s}: {val:8.2f}")
        else:
            print(f"{key:20s}: {val}")

    # Gráficos
    plotar_graficos(consumos, metricas)

if __name__ == "__main__":
    main()
