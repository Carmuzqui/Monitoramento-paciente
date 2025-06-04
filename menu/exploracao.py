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
#     st.markdown("# 🔍 Exploração temporal")
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

#     # ax1.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="HeartRate (vitals)", color='black', linestyle='--', alpha=0.6)
#     ax1.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="HeartRate (vitals)", color='black', linestyle='dotted', alpha=0.6)

#     ax1.set_ylim(60, 150)
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

#     ax2.set_ylim(0, 2.5)
#     ax2.set_title("Perfusion Index (Pi) por Sensor")
#     ax2.set_xlabel("Tempo")
#     ax2.set_ylabel("Pi Value")
#     ax2.legend()
#     ax2.grid(True)
#     st.pyplot(fig2)





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
#     # Conversão para valores numéricos
#     df['HeartRate'] = pd.to_numeric(df['HeartRate (bpm)'], errors='coerce')
#     df['Systolic'] = pd.to_numeric(df['Systolic (mmHg)'], errors='coerce')
#     df['Diastolic'] = pd.to_numeric(df['Diastolic (mmHg)'], errors='coerce')
#     df['MAP'] = pd.to_numeric(df['MAP (mmHg)'], errors='coerce')
#     df['Respiration'] = pd.to_numeric(df['Respiration (Bpm)'], errors='coerce')
#     df['AS'] = pd.to_numeric(df['AS'], errors='coerce')
#     df['SQE'] = pd.to_numeric(df['SQE'], errors='coerce')
#     return df[['datetime', 'HeartRate', 'Systolic', 'Diastolic', 'MAP', 'Respiration', 'AS', 'SQE']]

# def render():
#     st.markdown("# 🔍 Exploração temporal")
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

#     ax1.plot(df_vitals['datetime'], df_vitals['HeartRate'], label="HeartRate (vitals)", color='black', linestyle='dotted', alpha=0.6)
#     ax1.set_ylim(60, 150)
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

#     ax2.set_ylim(0, 2.5)
#     ax2.set_title("Perfusion Index (Pi) por Sensor")
#     ax2.set_xlabel("Tempo")
#     ax2.set_ylabel("Pi Value")
#     ax2.legend()
#     ax2.grid(True)
#     st.pyplot(fig2)

#     # --- NOVO: Seleção dinâmica e visualização entre HeartRate e outras variáveis ---
#     st.markdown("## 📈 Relação entre HeartRate e outras variáveis do Vitals")
#     variaveis = ['Systolic', 'Diastolic', 'MAP', 'Respiration', 'AS', 'SQE']
#     var_selecionada = st.selectbox(
#         "Selecione a variável para comparar com a frequência cardíaca (HeartRate):",
#         variaveis
#     )

#     fig3, ax3 = plt.subplots(figsize=(8, 5))
#     ax3.scatter(df_vitals['HeartRate'], df_vitals[var_selecionada], alpha=0.6)
#     ax3.set_xlabel("HeartRate (bpm)")
#     ax3.set_ylabel(f"{var_selecionada}")
#     ax3.set_title(f"HeartRate vs {var_selecionada}")
#     ax3.grid(True)
#     st.pyplot(fig3)

#     # --- Dica clínica/técnica ---
#     if var_selecionada == "MAP":
#         st.info("MAP (Pressão Arterial Média) é uma variável clínica essencial, pois representa a pressão de perfusão dos órgãos vitais. Prever o MAP a partir da frequência cardíaca pode ser extremamente útil para monitoramento hemodinâmico.")
#     elif var_selecionada in ["Systolic", "Diastolic"]:
#         st.info("Systolic e Diastolic são componentes fundamentais da pressão arterial e têm importância clínica direta na avaliação cardiovascular.")
#     elif var_selecionada == "Respiration":
#         st.info("Respiration indica a taxa respiratória, também relevante em contextos críticos, mas com relação fisiológica distinta.")
#     elif var_selecionada in ["AS", "SQE"]:
#         st.info("AS e SQE são variáveis técnicas relacionadas à qualidade ou características do sinal, úteis em contexto de validação ou robustez do sensor.")

# # Para rodar em Streamlit:
# # if __name__ == "__main__":
# #     render()











# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# def carregar_dados():
#     # Carga o consolidado dos sensores R (usando apenas R3) e o vitals alinhado
#     df_r = pd.read_csv("data/R_consolidado.csv")
#     df_vitals = pd.read_csv("data/vitals_alinhado.csv")
    
#     # Renomeia as colunas de R3 para nomes amigáveis
#     df_r3 = df_r[['Epoch Time', 'SpO2_%_Value_3', 'PR_bpm_Value_3', 'Pi_Value_3', 'Events_3']].copy()
#     df_r3.rename(columns={
#         'SpO2_%_Value_3': 'SpO2_R3',
#         'PR_bpm_Value_3': 'PR_R3',
#         'Pi_Value_3': 'Pi_R3',
#         'Events_3': 'Events_R3'
#     }, inplace=True)
    
#     # Converte Epoch Time para datetime se necessário
#     if not pd.api.types.is_datetime64_any_dtype(df_r3['Epoch Time']):
#         df_r3['datetime'] = pd.to_datetime(df_r3['Epoch Time'], unit='ms')
#     else:
#         df_r3['datetime'] = df_r3['Epoch Time']

#     # Variables do sensor vitals
#     df_vitals.rename(columns={
#         'HeartRate (bpm)': 'HeartRate',
#         'Systolic (mmHg)': 'Systolic',
#         'Diastolic (mmHg)': 'Diastolic',
#         'MAP (mmHg)': 'MAP',
#         'Respiration (Bpm)': 'Respiration',
#     }, inplace=True)
#     if 'TimeStamp (mS)' in df_vitals.columns:
#         df_vitals['datetime'] = pd.to_datetime(df_vitals['TimeStamp (mS)'], unit='ms')
#     elif 'Epoch Time' in df_vitals.columns:
#         df_vitals['datetime'] = pd.to_datetime(df_vitals['Epoch Time'], unit='ms')

#     return df_r3, df_vitals

# def render():
#     st.title("🔍 Visualização Interativa dos Sensores R3 e Vitals")

#     df_r3, df_vitals = carregar_dados()

#     st.subheader("Selecione as variáveis para visualizar")

#     # Listas de variáveis disponíveis para seleção
#     variaveis_r3 = ['SpO2_R3', 'PR_R3', 'Pi_R3']
#     variaveis_vitals = ['HeartRate', 'Systolic', 'Diastolic', 'MAP', 'Respiration']

#     selected_r3 = st.multiselect("Variáveis do sensor R3", variaveis_r3, default=['PR_R3'])
#     selected_vitals = st.multiselect("Variáveis do sensor Vitals", variaveis_vitals, default=['MAP'])

#     # Merge dos dois dataframes pelo tempo mais próximo
#     df_merge = pd.merge_asof(
#         df_r3.sort_values('datetime'),
#         df_vitals.sort_values('datetime'),
#         on='datetime',
#         direction='nearest',  # ou 'backward'/'forward' se preferir
#         tolerance=pd.Timedelta(milliseconds=1000)  # Ajuste a tolerância conforme o intervalo dos dados
#     )

#     # Plotagem dinâmica
#     fig, ax = plt.subplots(figsize=(15, 6))
#     for col in selected_r3:
#         ax.plot(df_merge['datetime'], df_merge[col], label=col)
#     for col in selected_vitals:
#         ax.plot(df_merge['datetime'], df_merge[col], label=col, linestyle='dashed')

#     ax.set_xlabel("Tempo")
#     ax.set_ylabel("Valor")
#     ax.set_title("Visualização das variáveis dos sensores R3 e Vitals")
#     ax.legend()
#     ax.grid(True)
#     st.pyplot(fig)

#     # st.info(
#     #     "Dica: Experimente selecionar 'PR_R3' e 'MAP' juntos para analisar a relação entre frequência de pulso e pressão arterial média."
#     # )

# if __name__ == "__main__":
#     render()







# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# def carregar_dados():
#     df_r = pd.read_csv("data/R_consolidado.csv")
#     df_vitals = pd.read_csv("data/vitals_alinhado.csv")

#     df_r3 = df_r[['Epoch Time', 'SpO2_%_Value_3', 'PR_bpm_Value_3', 'Pi_Value_3', 'Events_3']].copy()
#     df_r3.rename(columns={
#         'SpO2_%_Value_3': 'SpO2_R3',
#         'PR_bpm_Value_3': 'PR_R3',
#         'Pi_Value_3': 'Pi_R3',
#         'Events_3': 'Events_R3'
#     }, inplace=True)

#     df_r3['datetime'] = pd.to_datetime(df_r3['Epoch Time'], unit='ms')
#     df_vitals.rename(columns={
#         'HeartRate (bpm)': 'HeartRate',
#         'Systolic (mmHg)': 'Systolic',
#         'Diastolic (mmHg)': 'Diastolic',
#         'MAP (mmHg)': 'MAP',
#         'Respiration (Bpm)': 'Respiration',
#     }, inplace=True)
#     if 'TimeStamp (mS)' in df_vitals.columns:
#         df_vitals['datetime'] = pd.to_datetime(df_vitals['TimeStamp (mS)'], unit='ms')
#     elif 'Epoch Time' in df_vitals.columns:
#         df_vitals['datetime'] = pd.to_datetime(df_vitals['Epoch Time'], unit='ms')
#     return df_r3, df_vitals

# def render():
#     st.title("🔍 Visualização Interativa dos Sensores R3 e Vitals")

#     df_r3, df_vitals = carregar_dados()

#     st.subheader("Selecione as variáveis para visualizar")

#     variaveis_r3 = ['SpO2_R3', 'PR_R3', 'Pi_R3']
#     variaveis_vitals = ['HeartRate', 'Systolic', 'Diastolic', 'MAP', 'Respiration']

#     selected_r3 = st.multiselect("Variáveis do sensor R3", variaveis_r3, default=['PR_R3'])
#     selected_vitals = st.multiselect("Variáveis do sensor Vitals", variaveis_vitals, default=['MAP'])

#     df_merge = pd.merge_asof(
#         df_r3.sort_values('datetime'),
#         df_vitals.sort_values('datetime'),
#         on='datetime',
#         direction='nearest',
#         tolerance=pd.Timedelta(milliseconds=1000)
#     )

#     fig, ax1 = plt.subplots(figsize=(15, 6))
#     color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

#     # Eixo secundário só se Pi_R3 for selecionado
#     ax2 = None
#     if 'Pi_R3' in selected_r3:
#         ax2 = ax1.twinx()
#         ax2.set_ylim(0, 3)
#         ax2.set_ylabel('Pi_R3', color=color_cycle[2])
#         ax2.tick_params(axis='y', labelcolor=color_cycle[2])

#     for i, col in enumerate(selected_r3):
#         if col == 'Pi_R3' and ax2 is not None:
#             ax2.plot(df_merge['datetime'], df_merge[col], label=col, color=color_cycle[2])
#         else:
#             ax1.plot(df_merge['datetime'], df_merge[col], label=col, color=color_cycle[i % len(color_cycle)])

#     for i, col in enumerate(selected_vitals):
#         ax1.plot(df_merge['datetime'], df_merge[col], label=col, linestyle='dashed')

#     ax1.set_xlabel("Tempo")
#     ax1.set_ylabel("Valor")
#     ax1.set_title("Visualização das variáveis dos sensores R3 e Vitals")
#     ax1.grid(True)

#     # Juntar as legendas de ambos os eixos se ax2 existir
#     lines, labels = ax1.get_legend_handles_labels()
#     if ax2 is not None:
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         lines += lines2
#         labels += labels2
#     ax1.legend(lines, labels)

#     st.pyplot(fig)

    

# if __name__ == "__main__":
#     render()










import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def carregar_dados():
    df_r = pd.read_csv("data/R_consolidado.csv")
    df_vitals = pd.read_csv("data/vitals_alinhado.csv")

    df_r3 = df_r[['Epoch Time', 'SpO2_%_Value_3', 'PR_bpm_Value_3', 'Pi_Value_3', 'Events_3']].copy()
    df_r3.rename(columns={
        'SpO2_%_Value_3': 'SpO2_R3',
        'PR_bpm_Value_3': 'PR_R3',
        'Pi_Value_3': 'Pi_R3',
        'Events_3': 'Events_R3'
    }, inplace=True)
    df_r3['datetime'] = pd.to_datetime(df_r3['Epoch Time'], unit='ms')

    df_vitals.rename(columns={
        'HeartRate (bpm)': 'HeartRate',
        'Systolic (mmHg)': 'Systolic',
        'Diastolic (mmHg)': 'Diastolic',
        'MAP (mmHg)': 'MAP',
        'Respiration (Bpm)': 'Respiration',
    }, inplace=True)
    if 'TimeStamp (mS)' in df_vitals.columns:
        df_vitals['datetime'] = pd.to_datetime(df_vitals['TimeStamp (mS)'], unit='ms')
    elif 'Epoch Time' in df_vitals.columns:
        df_vitals['datetime'] = pd.to_datetime(df_vitals['Epoch Time'], unit='ms')
    return df_r3, df_vitals

def render():
    st.title("🔍 Visualização Interativa dos Sensores R3 e Vitals (Plotly)")

    df_r3, df_vitals = carregar_dados()

    st.subheader("Selecione as variáveis para visualizar")
    variaveis_r3 = ['SpO2_R3', 'PR_R3', 'Pi_R3']
    variaveis_vitals = ['HeartRate', 'Systolic', 'Diastolic', 'MAP', 'Respiration']

    selected_r3 = st.multiselect("Variáveis do sensor R3", variaveis_r3, default=['PR_R3'])
    selected_vitals = st.multiselect("Variáveis do sensor Vitals", variaveis_vitals, default=['MAP'])

    df_merge = pd.merge_asof(
        df_r3.sort_values('datetime'),
        df_vitals.sort_values('datetime'),
        on='datetime',
        direction='nearest',
        tolerance=pd.Timedelta(milliseconds=1000)
    )

    # Paleta de cores diferenciadas (personalize mais se desejar)
    color_dict = {
        'SpO2_R3': 'blue',
        'PR_R3': 'red',
        'Pi_R3': 'green',
        'HeartRate': 'purple',
        'Systolic': 'orange',
        'Diastolic': 'cyan',
        'MAP': 'black',
        'Respiration': 'magenta'
    }

    fig = go.Figure()

    # R3
    for col in selected_r3:
        if col == 'Pi_R3':
            fig.add_trace(go.Scatter(
                x=df_merge['datetime'], y=df_merge[col],
                mode='markers',
                marker=dict(color=color_dict[col], size=3),
                name=col,
                yaxis='y2'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df_merge['datetime'], y=df_merge[col],
                mode='markers',
                marker=dict(color=color_dict[col], size=3),
                name=col
            ))

    # Vitals
    for col in selected_vitals:
        fig.add_trace(go.Scatter(
            x=df_merge['datetime'], y=df_merge[col],
            mode='markers',
            marker=dict(color=color_dict[col], size=3),
            name=col
        ))

    # Layout com segundo eixo para Pi_R3
    if 'Pi_R3' in selected_r3:
        fig.update_layout(
            yaxis2=dict(
                title='Pi_R3',
                overlaying='y',
                side='right',
                range=[0, 3],
                showgrid=False
            )
        )

    fig.update_layout(
        title="Visualização das variáveis dos sensores R3 e Vitals (com Zoom)",
        xaxis_title="Tempo",
        yaxis_title="Valor",
        legend_title="Variáveis",
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render()
