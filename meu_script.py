import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Carregar os dados de queimadas
df_2020 = pd.read_csv('queimadas_2020.csv')
df_2021 = pd.read_csv('queimadas_2021.csv')
df_2022 = pd.read_csv('queimadas_2022.csv')
df_2023 = pd.read_csv('queimadas_2023.csv')
df_2024 = pd.read_csv('queimadas_2024.csv')

# Concatenar os dados
df_combined = pd.concat([df_2020, df_2021, df_2022, df_2023, df_2024], ignore_index=True)

# Verificar os nomes das colunas
print(df_combined.columns)

# Supondo que a coluna correta com as datas seja 'DataHora'
df_combined['DataHora'] = pd.to_datetime(df_combined['DataHora'], errors='coerce')

# Criar a coluna 'ano'
df_combined['ano'] = df_combined['DataHora'].dt.year

# Remover duplicatas
df_combined.drop_duplicates(inplace=True)

# Análise do número de queimadas por ano
queimadas_por_ano = df_combined['ano'].value_counts().sort_index()

# Plotar o gráfico de barras do número de queimadas por ano
plt.figure(figsize=(10,6))
sns.barplot(x=queimadas_por_ano.index, y=queimadas_por_ano.values)
plt.title('Número de Queimadas no Amazonas por Ano (2020-2024)')
plt.xlabel('Ano')
plt.ylabel('Número de Queimadas')
plt.show()

# Análise Exploratória: Analisar a correlação entre temperatura e número de queimadas
# Verifique se a coluna 'temperatura' está no DataFrame
# Substitua 'temperatura' e 'numero_de_queimadas' pelos nomes corretos das colunas
if 'temperatura' in df_combined.columns and 'numero_de_queimadas' in df_combined.columns:
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='temperatura', y='numero_de_queimadas', data=df_combined)
    plt.title('Relação entre Temperatura e Número de Queimadas')
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Número de Queimadas')
    plt.show()

    # Calcular correlação
    correlacao = df_combined[['temperatura', 'numero_de_queimadas']].corr()
    print('Correlação entre Temperatura e Número de Queimadas:')
    print(correlacao)
else:
    print("As colunas 'temperatura' e/ou 'numero_de_queimadas' não foram encontradas no DataFrame.")

# Identificação das principais causas (exemplos)
# Aqui você pode expandir essa seção com análises adicionais conforme as colunas disponíveis
# Exemplo de documentação das causas
print("Identificação das causas das queimadas:")
# Liste as principais causas baseadas na análise
causas_identificadas = [
    "1. Condições climáticas extremas (alta temperatura e baixa umidade)",
    "2. Práticas agrícolas inadequadas",
    "3. Desmatamento para expansão agrícola"
]
for causa in causas_identificadas:
    print(causa)

# Sugestões de medidas preventivas
print("\nSugestões de Medidas Preventivas:")
medidas_preventivas = [
    "1. Melhoria na fiscalização das áreas de risco.",
    "2. Promoção de práticas agrícolas sustentáveis.",
    "3. Campanhas de conscientização sobre os impactos das queimadas."
]
for medida in medidas_preventivas:
    print(medida)

if 'Municipio' in df_combined.columns:
    queimadas_por_municipio = df_combined.groupby('Municipio').size()
    plt.figure(figsize=(12, 8))
    sns.heatmap(queimadas_por_municipio.values.reshape(-1, 1), cmap='YlOrRd', annot=True)
    plt.title('Mapa de Calor das Queimadas por Município')
    plt.xlabel('Município')
    plt.ylabel('Número de Queimadas')
    plt.xticks(ticks=range(len(queimadas_por_municipio.index)), labels=queimadas_por_municipio.index, rotation=90)
    plt.show()
    
    # Análise de Tendências Temporais
df_combined['DataHora'] = pd.to_datetime(df_combined['DataHora'], errors='coerce')
df_combined['Ano'] = df_combined['DataHora'].dt.year
df_combined['Mes'] = df_combined['DataHora'].dt.month

# Gráfico de Séries Temporais
plt.figure(figsize=(12, 6))
df_combined.groupby('DataHora').size().plot()
plt.title('Número de Queimadas ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Número de Queimadas')
plt.grid()
plt.show()

# Análise Mensal
monthly_burns = df_combined.groupby(['Ano', 'Mes']).size().unstack()
monthly_burns.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Queimadas Mensais no Amazonas')
plt.xlabel('Ano')
plt.ylabel('Número de Queimadas')
plt.legend(title='Mês')
plt.show()

# Análise Espacial com Mapas de Calor
# Criação de um mapa base
map_amazon = folium.Map(location=[-3.4653, -62.2159], zoom_start=6)

# Filtrando dados apenas do Amazonas
amazon_burns = df_combined[['Latitude', 'Longitude']].dropna()

# Adicionando um mapa de calor
heat_data = [[row['Latitude'], row['Longitude']] for index, row in amazon_burns.iterrows()]
HeatMap(heat_data).add_to(map_amazon)

# Salvar o mapa em um arquivo HTML
map_amazon.save("mapa_de_calor_queimadas.html")
print("Mapa de calor salvo como 'mapa_de_calor_queimadas.html'.")