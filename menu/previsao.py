# previsao.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def carregar_dados():
    df_r = pd.read_csv("data/R_alinhados.csv")
    df_vitals = pd.read_csv("data/vitals_alinhado.csv")

    df_r3 = df_r[['Epoch Time', 'PR_bpm_Value_3', 'Pi_Value_3']].copy()
    df_r3.rename(columns={
        'PR_bpm_Value_3': 'PR_R3',
        'Pi_Value_3': 'Pi_R3'
    }, inplace=True)
    df_r3['datetime'] = pd.to_datetime(df_r3['Epoch Time'], unit='ms')
    df_vitals['MAP'] = pd.to_numeric(df_vitals['MAP (mmHg)'], errors='coerce')

    # Filtrar valores de MAP superiores a 120
    df_vitals = df_vitals[df_vitals['MAP (mmHg)'] <= 130]

    # Selecionar apenas datetime e MAP
    if 'TimeStamp (mS)' in df_vitals.columns:
        df_vitals['datetime'] = pd.to_datetime(df_vitals['TimeStamp (mS)'], unit='ms')
    elif 'Epoch Time' in df_vitals.columns:
        df_vitals['datetime'] = pd.to_datetime(df_vitals['Epoch Time'], unit='ms')

    # Alinhar datasets por tempo
    df_merge = pd.merge_asof(
        df_r3.sort_values('datetime'),
        df_vitals[['datetime', 'MAP']].sort_values('datetime'),
        on='datetime',
        direction='nearest',
        tolerance=pd.Timedelta(milliseconds=1000)
    ).dropna()

    return df_merge

def render():
    st.header("🔮 Previsão de MAP a partir de PR_R3 e Pi_R3")

    df = carregar_dados()
    # st.write("Amostra dos dados utilizados para a previsão:")
    # st.dataframe(df[['datetime', 'PR_R3', 'Pi_R3', 'MAP']].head())

    X = df[['PR_R3', 'Pi_R3']]
    y = df['MAP']

    # Divisão treino/validação/teste (60%/20%/20%)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Modelo Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)

    # Métricas
    def metrics(y_true, y_pred, split):
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        st.write(f"**{split}** — MSE: {mse:.2f} | RMSE: {rmse:.2f} | R²: {r2:.2f}")

    st.subheader("Desempenho do modelo")
    metrics(y_train, y_train_pred, "Treino")
    metrics(y_val, y_val_pred, "Validação")
    metrics(y_test, y_test_pred, "Teste")

    # Gráfico real vs previsto (teste)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(y_test, y_test_pred, color='blue', alpha=0.7)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax.set_xlabel("MAP Real")
    ax.set_ylabel("MAP Previsto")
    ax.set_title("Comparação: MAP real vs MAP previsto (dados de teste)")
    st.pyplot(fig)

if __name__ == "__main__":
    render()
