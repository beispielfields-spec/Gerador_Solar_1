# -*- coding: utf-8 -*-
  
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="CALCULO DE GERADOR SOLAR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖 DADOS DE CONSUMO")
# Campo para inserir o consumo mensal
    CONSUMO_MENSAL = st.float(input(f"  Mês {mes:02d}: "),
        "Insira consumo menal", 
        type="float",
        help="Obtenha os dados do projeto"
   )
# Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )
# ------------------------------------------------------------------
# 1. Leitura dos 12 valores mensais – usando widgets Streamlit
# ------------------------------------------------------------------
def ler_consumo_mensal() -> list[float]:
    """
    Mostra 12 campos numéricos onde o usuário insere o consumo mensal (kWh).
    Retorna uma lista de floats.
    """
    st.subheader("?? Inserir Consumo Mensal (kWh)")

    consumos = []
    for mes in range(1, 13):
        # `key` garante que cada campo seja único
        valor = st.number_input(
            label=f"Mês {mes:02d}",
            min_value=0.0,
            value=0.0,
            step=0.1,
            key=f"mes_{mes}"
        )
        consumos.append(float(valor))
    return consumos

# ------------------------------------------------------------------
# 2. Cálculos
# ------------------------------------------------------------------
def calcular_metricas(consumos: list[float]) -> dict:
    arr = np.array(consumos)

    anual = arr.sum()
    media_mensal = anual / 12.0
    media_diaria = media_mensal / 30.0

    # Dados climáticos
    hsp = 4.3          # kWh/m²·dia
    eta = 0.85         # Performance Ratio

    p_pico = media_diaria / (hsp * eta)

    energia_autonomia = media_diaria / 2.0          # kWh
    energia_real = energia_autonomia / eta          # kWh
    dod = 0.90                                     # Profundidade de descarga
    capacidade_kwh = energia_real / dod             # kWh total
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


# ------------------------------------------------------------------
# 3. Visualização – usando Matplotlib + Streamlit
# ------------------------------------------------------------------
def plotar_graficos(consumos: list[float], metricas: dict) -> None:
    meses = [f"{i:02d}" for i in range(1, 13)]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle("Dimensionamento Fotovoltaico – JandiraSP", fontsize=16)

    # Barra de consumo mensal
    ax.bar(meses, consumos, color="#4e79a7")
    ax.set_title("Consumo Mensal (kWh)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("kWh")
    ax.tick_params(axis='x', rotation=45)

    # Linhas de métricas
    ax.plot(meses, consumos, label="Consumo Mensal", marker='o')
    ax.axhline(metricas["media_diaria"], color='g', linestyle='--',
               label=f"Média Diária ({metricas['media_diaria']:.2f} kWh)")
    ax.axhline(metricas["p_pico"] * 1000, color='r', linestyle='-',
               label=f"Pico Necessário ({metricas['p_pico']:.2f} kWp)")
    ax.axhline(metricas["capacidade_kwh"], color='m', linestyle='-.',
               label=f"Capacidade Bateria ({metricas['capacidade_kwh']:.2f} kWh)")
    ax.legend()
    ax.set_ylabel("kWh / kWp")

    st.pyplot(fig)


# ------------------------------------------------------------------
# 4. Programa principal – página Streamlit
# ------------------------------------------------------------------
def main() -> None:
    st.title("?? Dimensionamento Fotovoltaico – Jandira-SP")

    # 1. Entrada
    consumos = ler_consumo_mensal()

    # Botão para executar os cálculos
    if st.button("Calcular"):
        # 2. Cálculo
        metricas = calcular_metricas(consumos)

        # 3. Exibir resultados em texto
        st.subheader("?? Resultados")
        for key, val in metricas.items():
            if isinstance(val, float):
                st.write(f"**{key.replace('_', ' ').title()}:** {val:8.2f}")
            else:
                st.write(f"**{key.replace('_', ' ').title()}:** {val}")

        # 4. Gráficos
        plotar_graficos(consumos, metricas)


# ------------------------------------------------------------------
# Execução
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()

