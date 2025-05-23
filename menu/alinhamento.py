import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import random

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

def encontrar_registros_similares(df_r3, valor_vitals, max_desvio=2):
    """
    Encontra registros no sensor R3 com valores similares ao valor do vitals.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3
    - valor_vitals: Valor do HeartRate do vitals
    - max_desvio: Desvio máximo permitido
    
    Retorna:
    - DataFrame com os registros similares
    """
    return df_r3[(df_r3['PR'] >= valor_vitals - max_desvio) & 
                 (df_r3['PR'] <= valor_vitals + max_desvio)]




def calcular_metricas_alinhamento(df_r3, df_vitals, desfase, max_diff_tempo=500, limiar_penalizacao=3, penalizacoes_minimas=50):
    """
    Calcula métricas para avaliar a qualidade do alinhamento com um determinado desfase.
    Interrompe a verificação se o número de penalizações ultrapassar um valor mínimo global.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3
    - df_vitals: DataFrame do sensor vitals
    - desfase: Valor de desfase em milissegundos a ser testado
    - max_diff_tempo: Diferença máxima de tempo (em ms) para considerar uma comparação válida
    - limiar_penalizacao: Valor de erro absoluto acima do qual se aplica uma penalização
    - penalizacoes_minimas: Número mínimo global de penalizações para interromper a verificação
    
    Retorna:
    - Dicionário com as métricas calculadas
    """
    # Aplicando o desfase aos tempos do R3
    df_r3_temp = df_r3.copy()
    df_r3_temp['tempo_ajustado'] = df_r3_temp['tempo_relativo'] + desfase
    
    # # Ordenar os DataFrames por tempo para otimizar a busca
    # df_r3_temp = df_r3_temp.sort_values('tempo_ajustado').reset_index(drop=False)
    # df_vitals_temp = df_vitals.sort_values('tempo_relativo').reset_index(drop=False)

    df_vitals_temp = df_vitals

        
    erros_absolutos = []
    num_penalizacoes = 0
    num_comparacoes = 0
    
    # Índice para percorrer o DataFrame do R3
    idx_r3 = 0
    
    # Para cada registro do vitals
    for idx_vitals, row_vitals in df_vitals_temp.iterrows():
        tempo_vitals = row_vitals['tempo_relativo']
        valor_vitals = row_vitals['HeartRate']
        
        # Continuar a busca a partir do último índice de R3
        while idx_r3 < len(df_r3_temp):
            tempo_r3 = df_r3_temp.iloc[idx_r3]['tempo_ajustado']
            
            # Se o tempo do R3 for maior que tempo_vitals + max_diff_tempo, não há mais pares possíveis
            if tempo_r3 > tempo_vitals + max_diff_tempo:
                break
            
            # Verificar se o ponto atual do R3 está dentro da janela de tempo
            if abs(tempo_r3 - tempo_vitals) <= max_diff_tempo:
                # Calcular o erro absoluto
                valor_r3 = df_r3_temp.iloc[idx_r3]['PR']
                erro = abs(valor_r3 - valor_vitals)
                erros_absolutos.append(erro)
                
                # Verificar se é uma penalização
                if erro > limiar_penalizacao:
                    num_penalizacoes += 1
                                        
                    # Interromper se o número de penalizações ultrapassar o mínimo global
                    if num_penalizacoes >= penalizacoes_minimas:
                        return {
                            'desfase': desfase,
                            'media_erros': float('inf'),
                            'num_penalizacoes': num_penalizacoes,
                            'num_comparacoes': num_comparacoes,
                            'metrica': float('inf')
                        }
                
                num_comparacoes += 1
                # Encontrou um par, então sair do loop para o próximo valor de vitals
                break
            
            idx_r3 += 1
    
    # Calcular a média dos erros absolutos
    media_erros = np.mean(erros_absolutos) if erros_absolutos else float('inf')
    
    # Calcular a métrica final
    if num_comparacoes > 0:
        metrica = media_erros / num_comparacoes
    else:
        metrica = float('inf')
    
    return {
        'desfase': desfase,
        'media_erros': media_erros,
        'num_penalizacoes': num_penalizacoes,
        'num_comparacoes': num_comparacoes,
        'metrica': metrica
    }







def alinhar_sensores_heuristico(df_r3, df_vitals, num_pontos_aleatorios=20, max_desvio=2, 
                               max_diff_tempo=500, limiar_penalizacao=3, min_comparacoes_percentual=0.1):
    """
    Implementa a estratégia heurística para alinhar os sensores.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3
    - df_vitals: DataFrame do sensor vitals
    - num_pontos_aleatorios: Número de pontos aleatórios do vitals a considerar
    - max_desvio: Desvio máximo permitido para considerar valores similares
    - max_diff_tempo: Diferença máxima de tempo (em ms) para considerar uma comparação válida
    - limiar_penalizacao: Valor de erro absoluto acima do qual se aplica uma penalização
    - min_comparacoes_percentual: Percentual mínimo de comparações necessárias
    
    Retorna:
    - Melhor desfase encontrado e métricas associadas
    """
    # Selecionar pontos aleatórios do vitals
    indices_aleatorios = random.sample(range(len(df_vitals)), min(num_pontos_aleatorios, len(df_vitals)))
    pontos_aleatorios = df_vitals.iloc[indices_aleatorios]
    
    # Calcular o número mínimo de comparações necessárias
    min_comparacoes = min(int(len(df_r3) * min_comparacoes_percentual), int(len(df_vitals) * min_comparacoes_percentual))
    
    resultados = []

    num_penalizacoes=50
    
    # Para cada ponto aleatório do vitals
    for _, ponto_vitals in pontos_aleatorios.iterrows():
        valor_vitals = ponto_vitals['HeartRate']
        tempo_vitals = ponto_vitals['tempo_relativo']
        
        # Encontrar registros similares no R3
        registros_similares = encontrar_registros_similares(df_r3, valor_vitals, max_desvio)
        
        # Para cada registro similar, simular um alinhamento
        for _, registro_r3 in registros_similares.iterrows():
            tempo_r3 = registro_r3['tempo_relativo']
            
            # Calcular o desfase necessário para alinhar este par de pontos
            desfase = tempo_vitals - tempo_r3
            
            # Calcular métricas para este desfase
            metricas = calcular_metricas_alinhamento(
                df_r3, df_vitals, desfase, max_diff_tempo, limiar_penalizacao, num_penalizacoes
            )

            num_penalizacoes = metricas['num_penalizacoes']
            
            # Adicionar aos resultados se tiver número suficiente de comparações
            if metricas['num_comparacoes'] >= min_comparacoes:
                resultados.append(metricas)
    
    # Se não houver resultados válidos, retornar None
    if not resultados:
        return None
    
    # Ordenar resultados primeiro por número de penalizações, depois pela métrica
    resultados_ordenados = sorted(resultados, key=lambda x: (x['num_penalizacoes'], x['metrica']))
    
    # Retornar o melhor resultado
    return resultados_ordenados[0]




def aplicar_desfase(df, desfase, coluna_tempo='tempo_relativo'):
    """
    Aplica um desfase ao tempo de um DataFrame.
    
    Parâmetros:
    - df: DataFrame a ser ajustado
    - desfase: Valor de desfase em milissegundos
    - coluna_tempo: Nome da coluna de tempo
    
    Retorna:
    - DataFrame com o tempo ajustado
    """
    df_ajustado = df.copy()
    df_ajustado[f'{coluna_tempo}_ajustado'] = df_ajustado[coluna_tempo] + desfase
    return df_ajustado

def visualizar_alinhamento(df_r3, df_vitals, desfase=0):
    """
    Cria um gráfico interativo para visualizar o alinhamento dos sensores.
    
    Parâmetros:
    - df_r3: DataFrame do sensor R3
    - df_vitals: DataFrame do sensor vitals
    - desfase: Desfase a ser aplicado ao tempo do R3
    
    Retorna:
    - Figura do Plotly
    """
    # Aplicar o desfase ao R3
    df_r3_ajustado = aplicar_desfase(df_r3, desfase)
    
    # Criando o gráfico interativo com Plotly
    fig = go.Figure()
    
    # Adicionando pontos do R3 (PR)
    fig.add_trace(go.Scatter(
        x=df_r3_ajustado['tempo_relativo_ajustado']/1000,  # Convertendo para segundos
        y=df_r3_ajustado['PR'],
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
        title=f'Alinhamento entre PR (R3) e HeartRate (vitals) - Desfase: {desfase/1000:.2f} segundos',
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
    st.markdown("# 🔍 Alinhamento de Sensores")
    
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
        
        # Parâmetros para o alinhamento heurístico
        st.subheader("Parâmetros para o Alinhamento Heurístico")
        
        col1, col2 = st.columns(2)
        with col1:
            num_pontos_aleatorios = st.slider("Número de pontos aleatórios", 2, 50, 2)
            max_desvio = st.slider("Desvio máximo para valores similares (bpm)", 0, 5, 0)
        
        with col2:
            max_diff_tempo = st.slider("Diferença máxima de tempo (ms)", 100, 1000, 500, 50)
            limiar_penalizacao = st.slider("Limiar de penalização (bpm)", 1, 10, 3)
        
        min_comparacoes_percentual = st.slider("Percentual mínimo de comparações", 0.05, 0.3, 0.05, 0.01)



        # Selecionar aleatoriamente 25% dos dados do df_vitals, mantendo a ordem
        df_vitals_ajustado_subconjunto = df_vitals_ajustado.sample(frac=min_comparacoes_percentual*3).sort_index().reset_index(drop=False)


        
        # Botão para executar o alinhamento
        if st.button("Executar Alinhamento Heurístico"):
            with st.spinner("Calculando o melhor alinhamento..."):
                # Executar o alinhamento heurístico
                resultado = alinhar_sensores_heuristico(
                    df_r3_ajustado, 
                    df_vitals_ajustado_subconjunto,  #df_vitals_ajustado
                    num_pontos_aleatorios=num_pontos_aleatorios,
                    max_desvio=max_desvio,
                    max_diff_tempo=max_diff_tempo,
                    limiar_penalizacao=limiar_penalizacao,
                    min_comparacoes_percentual=min_comparacoes_percentual
                )
                
                if resultado:
                    # Exibir resultados
                    st.subheader("Resultados do Alinhamento")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Desfase (segundos)", f"{resultado['desfase']/1000:.3f}")
                    with col2:
                        st.metric("Média de Erros (bpm)", f"{resultado['media_erros']:.2f}")
                    with col3:
                        st.metric("Número de Penalizações", resultado['num_penalizacoes'])
                    
                    st.metric("Número de Comparações", resultado['num_comparacoes'])
                    st.metric("Métrica Final", f"{resultado['metrica']:.4f}")
                    
                    # Visualizar o alinhamento
                    st.subheader("Visualização do Alinhamento aprimorado")
                    fig_alinhado = visualizar_alinhamento(df_r3_ajustado, df_vitals_ajustado, resultado['desfase'])
                    st.plotly_chart(fig_alinhado, use_container_width=True)
                    
                    # Aplicar o desfase aos dados
                    df_r3_alinhado = aplicar_desfase(df_r3_ajustado, resultado['desfase'])
                    
                    # Opção para download dos dados alinhados
                    st.subheader("Download dos Dados Alinhados")
                    
                    @st.cache_data
                    def convert_df_to_csv(df):
                        return df.to_csv(index=False).encode('utf-8')
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_r3 = convert_df_to_csv(df_r3_alinhado[['tempo_relativo', 'tempo_relativo_ajustado', 'PR', 'SpO2', 'Pi']])
                        st.download_button(
                            "Download dados R3 alinhados",
                            csv_r3,
                            "r3_alinhado.csv",
                            "text/csv",
                            key='download-r3-alinhado'
                        )
                    
                    with col2:
                        csv_vitals = convert_df_to_csv(df_vitals_ajustado[['tempo_relativo', 'HeartRate']])
                        st.download_button(
                            "Download dados Vitals",
                            csv_vitals,
                            "vitals.csv",
                            "text/csv",
                            key='download-vitals-alinhado'
                        )
                else:
                    st.error("Não foi possível encontrar um alinhamento adequado com os parâmetros fornecidos. Tente ajustar os parâmetros.")
        
    except FileNotFoundError:
        st.error("Erro ao carregar arquivos. Verifique se os CSVs estão na pasta `data/`.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
        st.exception(e)

# Para execução direta do script
if __name__ == "__main__":
    render()
