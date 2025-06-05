# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go

# def carregar_dados():
#     df_r = pd.read_csv("data/R_alinhados.csv")
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
#     st.title("🔍 Correlações sensores R3 e Vitals")

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

#     # Paleta de cores diferenciadas (personalize mais se desejar)
#     color_dict = {
#         'SpO2_R3': 'blue',
#         'PR_R3': 'red',
#         'Pi_R3': 'green',
#         'HeartRate': 'purple',
#         'Systolic': 'orange',
#         'Diastolic': 'cyan',
#         'MAP': 'black',
#         'Respiration': 'magenta'
#     }

#     fig = go.Figure()

#     # R3
#     for col in selected_r3:
#         if col == 'Pi_R3':
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict[col], size=3),
#                 name=col,
#                 yaxis='y2'
#             ))
#         else:
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict[col], size=3),
#                 name=col
#             ))

#     # Vitals
#     for col in selected_vitals:
#         fig.add_trace(go.Scatter(
#             x=df_merge['datetime'], y=df_merge[col],
#             mode='markers',
#             marker=dict(color=color_dict[col], size=3),
#             name=col
#         ))

#     # Layout com segundo eixo para Pi_R3
#     if 'Pi_R3' in selected_r3:
#         fig.update_layout(
#             yaxis2=dict(
#                 title='Pi_R3',
#                 overlaying='y',
#                 side='right',
#                 range=[0, 3],
#                 showgrid=False
#             )
#         )

#     fig.update_layout(
#         title="Visualização das variáveis dos sensores R3 e Vitals (com Zoom)",
#         xaxis_title="Tempo",
#         yaxis_title="Valor",
#         legend_title="Variáveis",
#         hovermode="x unified",
#         height=500
#     )

#     st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     render()








# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go

# def carregar_dados():
#     df_r = pd.read_csv("data/R_alinhados.csv")
#     df_vitals = pd.read_csv("data/vitals_alinhado.csv")

#     # Incluímos todos os sensores R (R1, R2, R3) para seleção dinâmica
#     sensores_r = ['1', '2', '3']
#     dict_vars = {
#         'SpO2': 'SpO2_%_Value_',
#         'PR': 'PR_bpm_Value_',
#         'Pi': 'Pi_Value_',
#         'Events': 'Events_'
#     }

#     dfs_r = {}
#     for s in sensores_r:
#         cols = ['Epoch Time'] + [v + s for v in dict_vars.values()]
#         df_tmp = df_r[cols].copy()
#         df_tmp.rename(columns={
#             f'SpO2_%_Value_{s}': f'SpO2_R{s}',
#             f'PR_bpm_Value_{s}': f'PR_R{s}',
#             f'Pi_Value_{s}': f'Pi_R{s}',
#             f'Events_{s}': f'Events_R{s}'
#         }, inplace=True)
#         df_tmp['datetime'] = pd.to_datetime(df_tmp['Epoch Time'], unit='ms')
#         dfs_r[f'R{s}'] = df_tmp

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
#     return dfs_r, df_vitals

# def render():
#     st.title("🔍 Correlações entre sensores R e Vitals")

#     dfs_r, df_vitals = carregar_dados()
#     sensores = list(dfs_r.keys())

#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Selecione o sensor R para explorar")
#         sensor_sel = st.selectbox("Sensor R disponível", sensores, index=2)  # Padrão R3

#         # st.markdown("Selecione as variáveis para a matriz de correlação:")
#         variaveis_r = [f'SpO2_{sensor_sel}', f'PR_{sensor_sel}', f'Pi_{sensor_sel}']
#         # variaveis_corr = variaveis_r + ['MAP', 'HeartRate', 'Systolic', 'Diastolic', 'Respiration']
#         variaveis_corr = variaveis_r + ['MAP', 'Respiration']

#         # Merge para alinhar temporalmente com Vitals
#         df_merge = pd.merge_asof(
#             dfs_r[sensor_sel].sort_values('datetime'),
#             df_vitals.sort_values('datetime'),
#             on='datetime',
#             direction='nearest',
#             tolerance=pd.Timedelta(milliseconds=1000)
#         ).dropna(subset=variaveis_r)

#         # Matriz de correlação
#         corr_matrix = df_merge[variaveis_corr].corr()

#         st.markdown("### Matriz de correlação (R + Vitals)")
#         st.dataframe(corr_matrix.style.background_gradient(cmap="viridis").format("{:.2f}"), height=260, width=440)

#     with col2:
#         st.subheader("Visualização interativa das variáveis")

#         # variaveis_vitals = ['MAP', 'HeartRate', 'Systolic', 'Diastolic', 'Respiration']
#         variaveis_vitals = ['MAP', 'Respiration']

#         selected_r = st.multiselect(
#             f"Variáveis do {sensor_sel}",
#             variaveis_r,
#             default=[f'PR_{sensor_sel}']
#         )
#         selected_vitals = st.multiselect(
#             "Variáveis do sensor Vitals",
#             variaveis_vitals,
#             default=['MAP']
#         )

#         # Paleta de cores diferenciadas
#         color_dict = {
#             f'SpO2_{sensor_sel}': 'blue',
#             f'PR_{sensor_sel}': 'red',
#             f'Pi_{sensor_sel}': 'green',
#             'HeartRate': 'purple',
#             'Systolic': 'orange',
#             'Diastolic': 'cyan',
#             'MAP': 'black',
#             'Respiration': 'magenta'
#         }

#         fig = go.Figure()

#         # R
#         for col in selected_r:
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict.get(col, 'gray'), size=3),
#                 name=col
#             ))

#         # Vitals
#         for col in selected_vitals:
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict.get(col, 'gray'), size=3),
#                 name=col
#             ))

#         fig.update_layout(
#             title=f"Visualização das variáveis de {sensor_sel} e Vitals (com Zoom)",
#             xaxis_title="Tempo",
#             yaxis_title="Valor",
#             legend_title="Variáveis",
#             hovermode="x unified",
#             height=500
#         )

#         st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     render()





# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np

# def carregar_dados():
#     df_r = pd.read_csv("data/R_alinhados.csv")
#     df_vitals = pd.read_csv("data/vitals_alinhado.csv")

#     sensores_r = ['1', '2', '3']
#     dict_vars = {
#         'SpO2': 'SpO2_%_Value_',
#         'PR': 'PR_bpm_Value_',
#         'Pi': 'Pi_Value_',
#         'Events': 'Events_'
#     }

#     dfs_r = {}
#     for s in sensores_r:
#         cols = ['Epoch Time'] + [v + s for v in dict_vars.values()]
#         df_tmp = df_r[cols].copy()
#         df_tmp.rename(columns={
#             f'SpO2_%_Value_{s}': f'SpO2_R{s}',
#             f'PR_bpm_Value_{s}': f'PR_R{s}',
#             f'Pi_Value_{s}': f'Pi_R{s}',
#             f'Events_{s}': f'Events_R{s}'
#         }, inplace=True)
#         df_tmp['datetime'] = pd.to_datetime(df_tmp['Epoch Time'], unit='ms')
#         dfs_r[f'R{s}'] = df_tmp

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
#     return dfs_r, df_vitals

# def matriz_corr_quadrada(df, variaveis_corr):
#     """
#     Gera uma matriz de correlação quadrada, preenchendo com NaN onde faltar.
#     """
#     corr = df[variaveis_corr].corr()
#     corr = corr.reindex(index=variaveis_corr, columns=variaveis_corr)
#     return corr

# def render():
#     st.title("🔍 Correlações entre sensores R e Vitals")

#     dfs_r, df_vitals = carregar_dados()
#     sensores = list(dfs_r.keys())

#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Selecione o sensor R para explorar")
#         sensor_sel = st.selectbox("Sensor R disponível", sensores, index=2)  # Padrão R3

#         variaveis_r = [f'SpO2_{sensor_sel}', f'PR_{sensor_sel}', f'Pi_{sensor_sel}']
#         variaveis_vitals_corr = ['MAP', 'Respiration']
#         variaveis_corr = variaveis_r + variaveis_vitals_corr

#         # Merge temporal
#         df_merge = pd.merge_asof(
#             dfs_r[sensor_sel].sort_values('datetime'),
#             df_vitals.sort_values('datetime'),
#             on='datetime',
#             direction='nearest',
#             tolerance=pd.Timedelta(milliseconds=1000)
#         )


#         # Limpeza: converte para numérico e remove valores inválidos ('-', '', None)
#         for col in variaveis_corr:
#             df_merge[col] = pd.to_numeric(df_merge[col], errors='coerce')

        
#         # Calcula matriz de correlação
#         corr_matrix = matriz_corr_quadrada(df_merge, variaveis_corr)

#         st.markdown("### Matriz de correlação (R + Vitals)")
#         st.dataframe(corr_matrix.style.background_gradient(cmap="viridis").format("{:.2f}"), height=260, width=440)

#     with col2:
#         st.subheader("Visualização interativa das variáveis")
        
#         variaveis_vitals = ['MAP', 'Respiration', 'HeartRate']
#         # Selectors alinhados lado a lado
#         csel1, csel2 = st.columns(2)
#         with csel1:
#             selected_r = st.multiselect(
#                 f"Variáveis do {sensor_sel}",
#                 variaveis_r,
#                 default=[f'PR_{sensor_sel}']
#             )
#         with csel2:
#             selected_vitals = st.multiselect(
#                 "Variáveis do sensor Vitals",
#                 variaveis_vitals,
#                 default=['MAP']
#             )

#         color_dict = {
#             f'SpO2_{sensor_sel}': 'blue',
#             f'PR_{sensor_sel}': 'red',
#             f'Pi_{sensor_sel}': 'green',
#             'MAP': 'black',
#             'Respiration': 'magenta'
#         }

#         fig = go.Figure()

#         # Añadir datos de Rx
#         for col in selected_r:
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict.get(col, 'gray'), size=3),
#                 name=col
#             ))

#         # Añadir datos de Vitals
#         for col in selected_vitals:
#             fig.add_trace(go.Scatter(
#                 x=df_merge['datetime'], y=df_merge[col],
#                 mode='markers',
#                 marker=dict(color=color_dict.get(col, 'gray'), size=3),
#                 name=col
#             ))

#         fig.update_layout(
#             # title removido
#             xaxis_title="Tempo",
#             yaxis_title="Valor",
#             legend_title="Variáveis",
#             hovermode="x unified",
#             height=500,
#             margin=dict(t=10)
#         )

#         st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     render()








import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def carregar_dados():
    df_r = pd.read_csv("data/R_alinhados.csv")
    df_vitals = pd.read_csv("data/vitals_alinhado.csv")

    sensores_r = ['1', '2', '3']
    dict_vars = {
        'SpO2': 'SpO2_%_Value_',
        'PR': 'PR_bpm_Value_',
        'Pi': 'Pi_Value_',
        'Events': 'Events_'
    }

    dfs_r = {}
    for s in sensores_r:
        cols = ['Epoch Time'] + [v + s for v in dict_vars.values()]
        df_tmp = df_r[cols].copy()
        df_tmp.rename(columns={
            f'SpO2_%_Value_{s}': f'SpO2_R{s}',
            f'PR_bpm_Value_{s}': f'PR_R{s}',
            f'Pi_Value_{s}': f'Pi_R{s}',
            f'Events_{s}': f'Events_R{s}'
        }, inplace=True)
        df_tmp['datetime'] = pd.to_datetime(df_tmp['Epoch Time'], unit='ms')
        dfs_r[f'R{s}'] = df_tmp

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
    return dfs_r, df_vitals

def matriz_corr_quadrada(df, variaveis_corr):
    corr = df[variaveis_corr].corr()
    corr = corr.reindex(index=variaveis_corr, columns=variaveis_corr)
    return corr

def render():
    st.title("🔍 Correlações entre sensores R e Vitals")

    dfs_r, df_vitals = carregar_dados()
    sensores = list(dfs_r.keys())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Selecione o sensor R para explorar")
        sensor_sel = st.selectbox("Sensor R disponível", sensores, index=2)  # Padrão R3

        variaveis_r = [f'SpO2_{sensor_sel}', f'PR_{sensor_sel}', f'Pi_{sensor_sel}']
        variaveis_vitals_corr = ['MAP', 'Respiration']
        variaveis_corr = variaveis_r + variaveis_vitals_corr

        # Merge temporal
        df_merge = pd.merge_asof(
            dfs_r[sensor_sel].sort_values('datetime'),
            df_vitals.sort_values('datetime'),
            on='datetime',
            direction='nearest',
            tolerance=pd.Timedelta(milliseconds=1000)
        )

        # Limpeza: converte para numérico e remove valores inválidos ('-', '', None)
        for col in variaveis_corr:
            df_merge[col] = pd.to_numeric(df_merge[col], errors='coerce')

        corr_matrix = matriz_corr_quadrada(df_merge, variaveis_corr)

        st.markdown("### Matriz de correlação (R + Vitals)")
        st.dataframe(corr_matrix.style.background_gradient(cmap="viridis").format("{:.2f}"), height=260, width=440)

    with col2:
        st.subheader("Visualização interativa das variáveis")
        
        variaveis_vitals = ['MAP', 'Respiration', 'HeartRate']
        # Selectors alinhados lado a lado
        csel1, csel2 = st.columns(2)
        with csel1:
            selected_r = st.multiselect(
                f"Variáveis do {sensor_sel}",
                variaveis_r,
                default=[f'PR_{sensor_sel}', f'Pi_{sensor_sel}']
            )
        with csel2:
            selected_vitals = st.multiselect(
                "Variáveis do sensor Vitals",
                variaveis_vitals,
                default=['MAP']
            )

        color_dict = {
            f'SpO2_{sensor_sel}': 'blue',
            f'PR_{sensor_sel}': 'red',
            f'Pi_{sensor_sel}': 'green',
            'MAP': 'black',
            'Respiration': 'magenta',
            'HeartRate': 'purple'
        }

        fig = go.Figure()

        # Añadir datos de Rx
        for col in selected_r:
            # Si la variable seleccionada es Pi (del sensor actual), graficar en y2
            if col == f'Pi_{sensor_sel}':
                fig.add_trace(go.Scatter(
                    x=df_merge['datetime'], y=df_merge[col],
                    mode='markers',
                    marker=dict(color=color_dict.get(col, 'gray'), size=3),
                    name=col,
                    yaxis='y2'
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=df_merge['datetime'], y=df_merge[col],
                    mode='markers',
                    marker=dict(color=color_dict.get(col, 'gray'), size=3),
                    name=col
                ))

        # Añadir datos de Vitals (siempre en el eje primario)
        for col in selected_vitals:
            fig.add_trace(go.Scatter(
                x=df_merge['datetime'], y=df_merge[col],
                mode='markers',
                marker=dict(color=color_dict.get(col, 'gray'), size=3),
                name=col
            ))

        # Solo mostrar el eje secundario si se seleccionó Pi
        if f'Pi_{sensor_sel}' in selected_r:
            fig.update_layout(
                yaxis2=dict(
                    title=f'Pi_{sensor_sel}',
                    overlaying='y',
                    side='right',
                    range=[0, 3],
                    showgrid=False
                )
            )

        fig.update_layout(
            xaxis_title="Tempo",
            yaxis_title="Valor",
            legend_title="Variáveis",
            hovermode="x unified",
            height=500,
            margin=dict(t=10)
        )

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render()
