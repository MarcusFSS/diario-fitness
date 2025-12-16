import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(
    page_title="DailyFit",
    page_icon="logo.png",
    layout="centered"
)

st.image("logo.png", width=200)
st.title("DailyFit")
st.caption("Diário simples de calorias, musculação, cardio e água")

ARQUIVO = "dados.csv"

# Carregar dados existentes
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO, parse_dates=["Data"])
else:
    df = pd.DataFrame(columns=[
        "Data", "Calorias", "Musculação", "Cardio (min)", "Água (ml)"
    ])

st.subheader("➕ Registrar o dia")

dia = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
calorias = st.number_input("Calorias consumidas", min_value=0, step=50)
musculacao = st.checkbox("Fez musculação hoje?")
cardio = st.number_input("Cardio (minutos)", min_value=0, step=5)
agua = st.number_input("Água ingerida (ml)", min_value=0, step=250)

if st.button("Salvar"):
    # remove registro do mesmo dia (para substituir)
    df = df[df["Data"] != pd.to_datetime(dia)]

    novo = pd.DataFrame([{
        "Data": dia,
        "Calorias": calorias,
        "Musculação": "Fez" if musculacao else "Não fez",
        "Cardio (min)": cardio,
        "Água (ml)": agua
    }])

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)
    st.success("Registro salvo com sucesso!")

st.divider()
st.subheader("📈 Histórico e gráficos")

if not df.empty:
    df = df.sort_values("Data")

    # Mostrar Data como DD/MM/AAAA na tabela
    df_vis = df.copy()
    df_vis["Data"] = df_vis["Data"].dt.strftime("%d/%m/%Y")
    st.dataframe(df_vis, use_container_width=True)

    st.line_chart(df.set_index("Data")[["Calorias"]])
    st.line_chart(df.set_index("Data")[["Água (ml)"]])
else:
    st.info("Nenhum registro ainda.")
