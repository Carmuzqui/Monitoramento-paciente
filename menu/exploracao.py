# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# def carregar_sensor(path, nome_sensor):
#     df = pd.read_csv(path)
#     df = df[df['SpO2 % Value'] != '-'].copy()
#     df['datetime'] = pd.to_datetime(df[' Epoch Time'], unit='ms')
#     df['SpO2'] = pd.to_numeric(df['SpO2 % Value'], errors='coerce')
#     df['Sensor'] = nome_sensor
#     return df[['datetime', 'SpO2', 'Sensor']]

# def carregar_vitals(path, inicio_r1):
#     df = pd.read_csv(path)
#     df['TimeStamp'] = pd.to_numeric(df['TimeStamp (mS)'], errors='coerce')
#     df['datetime'] = inicio_r1 + pd.to_timedelta(df['TimeStamp'], unit='ms')
#     df['HeartRate'] = pd.to_numeric(df['HeartRate (bpm)'], errors='coerce')
#     return df[['datetime', 'HeartRate']]

# def render():
#     st.markdown("# 🔍 Exploração Temporal")
#     st.write("Visualização dos valores de SpO₂ e frequência cardíaca para detectar possíveis defasagens temporais.")

#     try:
#         df_r1 = carregar_sensor("data/R1.csv", "R1")
#         df_r2 = carregar_sensor("data/R2.csv", "R2")
#         df_r3 = carregar_sensor("data/R3.csv", "R3")
#         inicio_r1 = df_r1['datetime'].min()
#         df_vitals = carregar_vitals("data/vitals.csv", inicio_r1)
#     except FileNotFoundError:
#         st.error("Erro ao carregar arquivos. Verifique se todos os CSVs estão na pasta 'data/'.")
#         return

#     df_spo2 = pd.concat([df_r1, df_r2, df_r3])

#     fig, ax = plt.subplots(figsize=(14, 6))

#     # Plot dos sensores de SpO2
#     for sensor in df_spo2['Sensor'].unique():
#         dados = df_spo2[df_spo2['Sensor'] == sensor]
#         ax.plot(dados['datetime'], dados['SpO2'], label=f"SpO₂ - {sensor}", alpha=0.7)

#     # Plot dos batimentos cardíacos (HR)
#     ax.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="Frequência Cardíaca (vitals)", color='black', linestyle='--', alpha=0.6)

#     ax.set_title("Comparação Temporal: SpO₂ dos Sensores e Frequência Cardíaca (vitals)")
#     ax.set_xlabel("Tempo")
#     ax.set_ylabel("Valores Medidos")
#     ax.legend()
#     ax.grid(True)

#     st.pyplot(fig)








# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# def carregar_sensor(path, nome_sensor):
#     df = pd.read_csv(path)
#     df = df[df['SpO2 % Value'] != '-'].copy()
#     df['datetime'] = pd.to_datetime(df[' Epoch Time'], unit='ms')
#     df['SpO2'] = pd.to_numeric(df['SpO2 % Value'], errors='coerce')
#     df['PR'] = pd.to_numeric(df['PR bpm Value'], errors='coerce')
#     df['Pi'] = pd.to_numeric(df['Pi Value'], errors='coerce')
#     df['Sensor'] = nome_sensor
#     return df[['datetime', 'SpO2', 'PR', 'Pi', 'Sensor']]

# def carregar_vitals(path, inicio_r1):
#     df = pd.read_csv(path)
#     df['TimeStamp'] = pd.to_numeric(df['TimeStamp (mS)'], errors='coerce')
#     df['datetime'] = inicio_r1 + pd.to_timedelta(df['TimeStamp'], unit='ms')
#     df['HeartRate'] = pd.to_numeric(df['HeartRate (bpm)'], errors='coerce')
#     return df[['datetime', 'HeartRate']]

# def render():
#     st.markdown("# 🔍 Exploração Temporal")
#     st.write("Visualização dos valores de SpO₂, PR, Pi e frequência cardíaca.")

#     try:
#         df_r1 = carregar_sensor("data/R1.csv", "R1")
#         df_r2 = carregar_sensor("data/R2.csv", "R2")
#         df_r3 = carregar_sensor("data/R3.csv", "R3")
#         inicio_r1 = df_r1['datetime'].min()
#         df_vitals = carregar_vitals("data/vitals.csv", inicio_r1)
#     except FileNotFoundError:
#         st.error("Erro ao carregar arquivos. Verifique se os CSVs estão na pasta `data/`.")
#         return

#     df_all = pd.concat([df_r1, df_r2, df_r3])

#     # --- Gráfico 1: SpO₂, PR bpm e HeartRate ---
#     fig1, ax1 = plt.subplots(figsize=(14, 6))
#     for sensor in df_all['Sensor'].unique():
#         df_sensor = df_all[df_all['Sensor'] == sensor]
#         ax1.plot(df_sensor['datetime'], df_sensor['SpO2'], label=f"SpO₂ - {sensor}", alpha=0.7)
#         ax1.plot(df_sensor['datetime'], df_sensor['PR'], label=f"PR bpm - {sensor}", linestyle='dotted', alpha=0.5)

#     ax1.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="HeartRate (vitals)", color='black', linestyle='--', alpha=0.6)

#     ax1.set_title("SpO₂, Frequência de Pulso (PR) e Frequência Cardíaca")
#     ax1.set_xlabel("Tempo")
#     ax1.set_ylabel("Valor")
#     ax1.legend()
#     ax1.grid(True)
#     st.pyplot(fig1)

#     # --- Gráfico 2: Pi Value ---
#     fig2, ax2 = plt.subplots(figsize=(14, 4))
#     for sensor in df_all['Sensor'].unique():
#         df_sensor = df_all[df_all['Sensor'] == sensor]
#         ax2.plot(df_sensor['datetime'], df_sensor['Pi'], label=f"Pi - {sensor}", alpha=0.6)

#     ax2.set_title("Perfusion Index (Pi) por Sensor")
#     ax2.set_xlabel("Tempo")
#     ax2.set_ylabel("Pi Value")
#     ax2.legend()
#     ax2.grid(True)
#     st.pyplot(fig2)






import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def carregar_sensor(path, nome_sensor):
    df = pd.read_csv(path)
    df = df[df['SpO2 % Value'] != '-'].copy()
    df['datetime'] = pd.to_datetime(df[' Epoch Time'], unit='ms')
    df['SpO2'] = pd.to_numeric(df['SpO2 % Value'], errors='coerce')
    df['PR'] = pd.to_numeric(df['PR bpm Value'], errors='coerce')
    df['Pi'] = pd.to_numeric(df['Pi Value'], errors='coerce')
    df['Sensor'] = nome_sensor
    return df[['datetime', 'SpO2', 'PR', 'Pi', 'Sensor']]

def carregar_vitals(path, inicio_r1):
    df = pd.read_csv(path)
    df['TimeStamp'] = pd.to_numeric(df['TimeStamp (mS)'], errors='coerce')
    df['datetime'] = inicio_r1 + pd.to_timedelta(df['TimeStamp'], unit='ms')
    df['HeartRate'] = pd.to_numeric(df['HeartRate (bpm)'], errors='coerce')
    return df[['datetime', 'HeartRate']]

def render():
    st.markdown("# 🔍 Exploração temporal")
    st.write("Visualização dos valores de SpO₂, PR, Pi e frequência cardíaca.")

    try:
        df_r1 = carregar_sensor("data/R1.csv", "R1")
        df_r2 = carregar_sensor("data/R2.csv", "R2")
        df_r3 = carregar_sensor("data/R3.csv", "R3")
        inicio_r1 = df_r1['datetime'].min()
        df_vitals = carregar_vitals("data/vitals.csv", inicio_r1)
    except FileNotFoundError:
        st.error("Erro ao carregar arquivos. Verifique se os CSVs estão na pasta `data/`.")
        return

    df_all = pd.concat([df_r1, df_r2, df_r3])

    # --- Gráfico 1: SpO₂, PR bpm e HeartRate ---
    fig1, ax1 = plt.subplots(figsize=(14, 6))
    for sensor in df_all['Sensor'].unique():
        df_sensor = df_all[df_all['Sensor'] == sensor]
        ax1.plot(df_sensor['datetime'], df_sensor['SpO2'], label=f"SpO₂ - {sensor}", alpha=0.7)
        ax1.plot(df_sensor['datetime'], df_sensor['PR'], label=f"PR bpm - {sensor}", linestyle='dotted', alpha=0.5)

    ax1.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="HeartRate (vitals)", color='black', linestyle='--', alpha=0.6)

    ax1.set_ylim(60, 150)
    ax1.set_title("SpO₂, Frequência de Pulso (PR) e Frequência Cardíaca")
    ax1.set_xlabel("Tempo")
    ax1.set_ylabel("Valor")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # --- Gráfico 2: Pi Value ---
    fig2, ax2 = plt.subplots(figsize=(14, 4))
    for sensor in df_all['Sensor'].unique():
        df_sensor = df_all[df_all['Sensor'] == sensor]
        ax2.plot(df_sensor['datetime'], df_sensor['Pi'], label=f"Pi - {sensor}", alpha=0.6)

    ax2.set_ylim(0, 2.5)
    ax2.set_title("Perfusion Index (Pi) por Sensor")
    ax2.set_xlabel("Tempo")
    ax2.set_ylabel("Pi Value")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

