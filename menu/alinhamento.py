# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# def carregar_e_limpar_r3(path):
#     """
#     Carrega e limpa os dados do sensor R3.
    
#     Parâmetros:
#     - path: Caminho para o arquivo R3.csv
    
#     Retorna:
#     - DataFrame limpo com apenas os dados confiáveis
#     """
#     # Carregando os dados do R3
#     df_r3 = pd.read_csv(path)
    
#     # Convertendo colunas para formato numérico
#     df_r3['SpO2'] = pd.to_numeric(df_r3['SpO2 % Value'], errors='coerce')
#     df_r3['PR'] = pd.to_numeric(df_r3['PR bpm Value'], errors='coerce')
#     df_r3['Pi'] = pd.to_numeric(df_r3['Pi Value'], errors='coerce')
#     df_r3['Epoch'] = pd.to_numeric(df_r3[' Epoch Time'], errors='coerce')
    
#     # Aplicando critérios de limpeza:
#     # - SpO2 > 90
#     # - Pi > 0.3
#     df_r3_limpo = df_r3[(df_r3['SpO2'] > 90) & (df_r3['Pi'] > 0.3)].copy()
    
#     # Resetando o índice após a filtragem
#     df_r3_limpo.reset_index(drop=True, inplace=True)
    
#     return df_r3_limpo

# def carregar_vitals(path):
#     """
#     Carrega os dados do arquivo vitals.csv
    
#     Parâmetros:
#     - path: Caminho para o arquivo vitals.csv
    
#     Retorna:
#     - DataFrame com os dados de vitals
#     """
#     df_vitals = pd.read_csv(path)
    
#     # Convertendo a coluna de timestamp para numérico
#     df_vitals['TimeStamp'] = pd.to_numeric(df_vitals['TimeStamp (mS)'], errors='coerce')
#     df_vitals['HeartRate'] = pd.to_numeric(df_vitals['HeartRate (bpm)'], errors='coerce')
    
#     return df_vitals

# def ajuste_tempo_zero(df_r3, df_vitals):
#     """
#     Ajusta o tempo zero dos sensores para que ambos comecem do zero.
    
#     Parâmetros:
#     - df_r3: DataFrame do sensor R3 limpo
#     - df_vitals: DataFrame do sensor vitals
    
#     Retorna:
#     - Tupla com os DataFrames ajustados
#     """
#     # Obtendo o tempo inicial de cada sensor
#     tempo_inicial_r3 = df_r3['Epoch'].min()
#     tempo_inicial_vitals = df_vitals['TimeStamp'].min()
    
#     # Calculando o delta de tempo desde o início para cada sensor
#     df_r3['tempo_relativo'] = df_r3['Epoch'] - tempo_inicial_r3
#     df_vitals['tempo_relativo'] = df_vitals['TimeStamp'] - tempo_inicial_vitals
    
#     return df_r3, df_vitals

# def visualizar_ajuste_tempo_zero(df_r3, df_vitals):
#     """
#     Cria um gráfico para visualizar os dados após o ajuste de tempo zero.
    
#     Parâmetros:
#     - df_r3: DataFrame do sensor R3 com tempo relativo
#     - df_vitals: DataFrame do sensor vitals com tempo relativo
#     """
#     fig, ax = plt.subplots(figsize=(14, 6))
    
#     # Plotando PR do R3
#     ax.plot(df_r3['tempo_relativo']/1000, df_r3['PR'], 
#             label="PR bpm - R3", alpha=0.7, color='blue')
    
#     # Plotando HeartRate do vitals
#     ax.plot(df_vitals['tempo_relativo']/1000, df_vitals['HeartRate'], 
#             label="HeartRate - vitals", color='red', linestyle='--', alpha=0.7)
    
#     ax.set_title("Comparação entre PR (R3) e HeartRate (vitals) - Ajuste de Tempo Zero")
#     ax.set_xlabel("Tempo (segundos desde o início)")
#     ax.set_ylabel("Batimentos por minuto (bpm)")
#     ax.legend()
#     ax.grid(True)
    
#     return fig

# def render():
#     """
#     Função principal para renderizar a interface do Streamlit.
#     """
#     st.markdown("# 🔍 Ajuste Inicial de Tempo Zero")
#     st.write("Preparação para o alinhamento posterior dos dados de frequência cardíaca.")
    
#     # Carregando e limpando os dados
#     try:
#         df_r3 = carregar_e_limpar_r3("data/R3.csv")
#         df_vitals = carregar_vitals("data/vitals.csv")
        
#         # Exibindo informações sobre os dados originais
#         st.subheader("Informações dos Dados")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.write("Sensor R3 (após limpeza):")
#             st.write(f"- Registros: {len(df_r3)}")
#             st.write(f"- Período: {df_r3['Epoch'].min()} a {df_r3['Epoch'].max()} ms")
        
#         with col2:
#             st.write("Sensor Vitals:")
#             st.write(f"- Registros: {len(df_vitals)}")
#             st.write(f"- Período: {df_vitals['TimeStamp'].min()} a {df_vitals['TimeStamp'].max()} ms")
        
#         # Ajustando o tempo zero
#         df_r3_ajustado, df_vitals_ajustado = ajuste_tempo_zero(df_r3, df_vitals)
        
#         # Visualizando os dados após ajuste de tempo zero
#         st.subheader("Visualização após Ajuste de Tempo Zero")
#         fig = visualizar_ajuste_tempo_zero(df_r3_ajustado, df_vitals_ajustado)
#         st.pyplot(fig)
        
#         # Exibindo amostras dos dados ajustados
#         st.subheader("Amostra dos Dados com Tempo Zero Ajustado")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.write("R3 (primeiros 5 registros):")
#             st.dataframe(df_r3_ajustado[['tempo_relativo', 'PR', 'SpO2', 'Pi']].head())
        
#         with col2:
#             st.write("Vitals (primeiros 5 registros):")
#             st.dataframe(df_vitals_ajustado[['tempo_relativo', 'HeartRate']].head())
        
#         st.info("Este é apenas o ajuste inicial de tempo zero. O alinhamento completo será implementado posteriormente conforme a estratégia a ser compartilhada.")
        
#     except FileNotFoundError:
#         st.error("Erro ao carregar arquivos. Verifique se os CSVs estão na pasta `data/`.")
#     except Exception as e:
#         st.error(f"Ocorreu um erro: {str(e)}")

# # Para execução direta do script
# if __name__ == "__main__":
#     render()






import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def carregar_e_limpar_r3(path):
    """
    Carrega e limpa os dados do sensor R3.
    
    Parâmetros:
    - path: Caminho para o arquivo R3.csv
    
    Retorna:
    - DataFrame limpo com apenas os dados confiáveis
    """
    # Carregando os dados do R3
    df_r3 = pd.read_csv(path)
    
    # Convertendo colunas para formato numérico
    df_r3['SpO2'] = pd.to_numeric(df_r3['SpO2 % Value'], errors='coerce')
    df_r3['PR'] = pd.to_numeric(df_r3['PR bpm Value'], errors='coerce')
    df_r3['Pi'] = pd.to_numeric(df_r3['Pi Value'], errors='coerce')
    df_r3['Epoch'] = pd.to_numeric(df_r3[' Epoch Time'], errors='coerce')
    
    # Aplicando critérios de limpeza:
    # - SpO2 > 90
    # - Pi > 0.3
    df_r3_limpo = df_r3[(df_r3['SpO2'] > 90) & (df_r3['Pi'] > 0.3)].copy()
    
    # Resetando o índice após a filtragem
    df_r3_limpo.reset_index(drop=True, inplace=True)
    
    return df_r3_limpo

def carregar_vitals(path):
    """
    Carrega os dados do arquivo vitals.csv
    
    Parâmetros:
    - path: Caminho para o arquivo vitals.csv
    
    Retorna:
    - DataFrame com os dados de vitals
    """
    df_vitals = pd.read_csv(path)
    
    # Convertendo a coluna de timestamp para numérico
    df_vitals['TimeStamp'] = pd.to_numeric(df_vitals['TimeStamp (mS)'], errors='coerce')
    df_vitals['HeartRate'] = pd.to_numeric(df_vitals['HeartRate (bpm)'], errors='coerce')
    
    return df_vitals

def ajuste_tempo_zero(df_r3, df_vitals):
    """
    Ajusta o tempo zero dos sensores para que ambos comecem do zero.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3 limpo
    - df_vitals: DataFrame do sensor vitals
    
    Retorna:
    - Tupla com os DataFrames ajustados
    """
    # Obtendo o tempo inicial de cada sensor
    tempo_inicial_r3 = df_r3['Epoch'].min()
    tempo_inicial_vitals = df_vitals['TimeStamp'].min()
    
    # Calculando o delta de tempo desde o início para cada sensor
    df_r3['tempo_relativo'] = df_r3['Epoch'] - tempo_inicial_r3
    df_vitals['tempo_relativo'] = df_vitals['TimeStamp'] - tempo_inicial_vitals
    
    return df_r3, df_vitals

def visualizar_ajuste_tempo_zero_interativo(df_r3, df_vitals):
    """
    Cria um gráfico interativo com Plotly para visualizar os dados após o ajuste de tempo zero.
    Mostra apenas pontos (sem linhas) e permite zoom.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3 com tempo relativo
    - df_vitals: DataFrame do sensor vitals com tempo relativo
    """
    # Criando o gráfico interativo com Plotly
    fig = go.Figure()
    
    # Adicionando pontos do R3 (PR)
    fig.add_trace(go.Scatter(
        x=df_r3['tempo_relativo']/1000,  # Convertendo para segundos
        y=df_r3['PR'],
        mode='markers',  # Apenas pontos, sem linhas
        marker=dict(
            size=2,  # Tamanho pequeno dos pontos
            color='blue',
            opacity=0.7
        ),
        name='PR bpm - R3'
    ))
    
    # Adicionando pontos do Vitals (HeartRate)
    fig.add_trace(go.Scatter(
        x=df_vitals['tempo_relativo']/1000,  # Convertendo para segundos
        y=df_vitals['HeartRate'],
        mode='markers',  # Apenas pontos, sem linhas
        marker=dict(
            size=2,  # Tamanho pequeno dos pontos
            color='red',
            opacity=0.7
        ),
        name='HeartRate - vitals'
    ))
    
    # Configurando o layout do gráfico
    fig.update_layout(
        title='Comparação entre PR (R3) e HeartRate (vitals) - Ajuste de Tempo Zero',
        xaxis_title='Tempo (segundos desde o início)',
        yaxis_title='Batimentos por minuto (bpm)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        hovermode='closest'
    )
    
    # Configurando as ferramentas de interação
    fig.update_layout(
        dragmode='zoom',  # Modo padrão de zoom
        showlegend=True
    )
    
    return fig

def render():
    """
    Função principal para renderizar a interface do Streamlit.
    """
    st.markdown("# 🔍 Ajuste Inicial de Tempo Zero")
    st.write("Preparação para o alinhamento posterior dos dados de frequência cardíaca.")
    
    # Carregando e limpando os dados
    try:
        df_r3 = carregar_e_limpar_r3("data/R3.csv")
        df_vitals = carregar_vitals("data/vitals.csv")
        
        # Exibindo informações sobre os dados originais
        st.subheader("Informações dos Dados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Sensor R3 (após limpeza):")
            st.write(f"- Registros: {len(df_r3)}")
            st.write(f"- Período: {df_r3['Epoch'].min()} a {df_r3['Epoch'].max()} ms")
        
        with col2:
            st.write("Sensor Vitals:")
            st.write(f"- Registros: {len(df_vitals)}")
            st.write(f"- Período: {df_vitals['TimeStamp'].min()} a {df_vitals['TimeStamp'].max()} ms")
        
        # Ajustando o tempo zero
        df_r3_ajustado, df_vitals_ajustado = ajuste_tempo_zero(df_r3, df_vitals)
        
        # Visualizando os dados após ajuste de tempo zero com gráfico interativo
        st.subheader("Visualização após Ajuste de Tempo Zero")
        
        fig = visualizar_ajuste_tempo_zero_interativo(df_r3_ajustado, df_vitals_ajustado)
        st.plotly_chart(fig, use_container_width=True)
        
        # Exibindo amostras dos dados ajustados
        st.subheader("Amostra dos Dados com Tempo Zero Ajustado")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("R3 (primeiros 5 registros):")
            st.dataframe(df_r3_ajustado[['tempo_relativo', 'PR', 'SpO2', 'Pi']].head())
        
        with col2:
            st.write("Vitals (primeiros 5 registros):")
            st.dataframe(df_vitals_ajustado[['tempo_relativo', 'HeartRate']].head())
        
        st.info("Este é apenas o ajuste inicial de tempo zero. O alinhamento completo será implementado posteriormente conforme a estratégia.")
        
        # Adicionando opção para download dos dados ajustados
        st.subheader("Download dos Dados Ajustados")
        
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_r3 = convert_df_to_csv(df_r3_ajustado[['tempo_relativo', 'PR', 'SpO2', 'Pi']])
            st.download_button(
                "Download dados R3 ajustados",
                csv_r3,
                "r3_ajustado.csv",
                "text/csv",
                key='download-r3'
            )
        
        with col2:
            csv_vitals = convert_df_to_csv(df_vitals_ajustado[['tempo_relativo', 'HeartRate']])
            st.download_button(
                "Download dados Vitals ajustados",
                csv_vitals,
                "vitals_ajustado.csv",
                "text/csv",
                key='download-vitals'
            )
        
    except FileNotFoundError:
        st.error("Erro ao carregar arquivos. Verifique se os CSVs estão na pasta `data/`.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

# Para execução direta do script
if __name__ == "__main__":
    render()