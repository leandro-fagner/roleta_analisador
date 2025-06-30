import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Analisador de Roleta", layout="centered")

st.title("🎯 Analisador de Roleta - Estratégia Pelayo")
st.markdown("""
Insira os últimos números que saíram na roleta (0 a 36). O sistema vai analisar quais números estão se repetindo mais e sugerir onde apostar.
""")

entrada = st.text_area("🎰 Números (separados por vírgula):", placeholder="Ex: 7, 22, 17, 7, 36, 31, 7")

if st.button("🔍 Analisar"):
    try:
        numeros = [int(n.strip()) for n in entrada.split(",") if n.strip().isdigit()]
        
        if not numeros:
            st.warning("Por favor, insira ao menos alguns números entre 0 e 36.")
        elif any(n < 0 or n > 36 for n in numeros):
            st.error("Os números devem estar entre 0 e 36 (roleta europeia).")
        else:
            frequencias = np.bincount(numeros, minlength=37)
            top5_indices = np.argsort(frequencias)[-5:][::-1]
            top5_numeros = list(top5_indices)
            top5_freq = frequencias[top5_indices]

            st.success("🎯 Números recomendados para apostar:")
            st.write(f"**{top5_numeros}** (os mais frequentes)")
            
            df = pd.DataFrame({
                "Número": np.arange(37),
                "Frequência": frequencias
            }).sort_values("Frequência", ascending=False)

            st.subheader("📊 Frequência dos Números")
            st.bar_chart(df.set_index("Número"))

            aposta_por_numero = 1
            saldo = 0
            for resultado in numeros:
                aposta_total = aposta_por_numero * len(top5_numeros)
                if resultado in top5_numeros:
                    saldo += 35 * aposta_por_numero - aposta_total
                else:
                    saldo -= aposta_total
            st.subheader("💰 Simulação de Lucro")
            st.write(f"Saldo hipotético: **{saldo:.2f} unidades** com {len(numeros)} giros.")

    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
