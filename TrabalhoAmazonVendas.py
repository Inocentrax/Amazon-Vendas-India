import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# 1º Fase: descrição do negócio (definir regara de negocio do BD)
#Avaliar 

# 2° fase: carregar o dataset ou arquivos e preparar os dados 
def carregarDados(nomePathArquivo):
    dataFrame = pd.read_csv(nomePathArquivo, sep=",", encoding="utf-8")
    print(dataFrame)
    return dataFrame

def prepararDados(dataFrame):
    print(dataFrame.info())
    print(dataFrame.head())
    print(dataFrame.tail())
    print(dataFrame.describe())
    dataFrame.drop_duplicates(inplace=True)
    colunas_para_remover = ['New', 'PendingS', 'fulfilled-by', 'Order ID', 'index', 'Fulfilment', 'B2B']
    colunas_existentes = [col for col in colunas_para_remover if col in dataFrame.columns]
    dataFrame.drop(columns=colunas_existentes, inplace=True)
    dataFrame.dropna(inplace=True) 
    if 'Status' in dataFrame.columns:
        dataFrame['Status'] = pd.Categorical(dataFrame['Status']).codes
    colunas = ['ship-service-level', 'Courier Status']
    for coluna in colunas:
        if coluna in dataFrame.columns:
            dataFrame[coluna] = pd.Categorical(dataFrame[coluna]).codes
    if 'Qty' in dataFrame.columns:
        dataFrame['Qty'] = dataFrame['Qty'].astype(int)
    if 'Amount' in dataFrame.columns:
        dataFrame['Amount'] = dataFrame['Amount'].astype(float)
    cotacao = {'INR': 1, 'R$': 14, 'US$': 83}
    moedas = {
        'INR': dataFrame['Amount'].sum(),
        'R$': dataFrame['Amount'].sum() / cotacao['R$'],
        'US$': dataFrame['Amount'].sum() / cotacao['US$']
    }
    print(f'Total em Reais: R$ {round(moedas["R$"], 2)}')
    print(f'Total em Dólares: US$ {round(moedas["US$"], 2)}')
    print(moedas)
    LE = LabelEncoder()
    if 'ship-city' in dataFrame.columns:
        dataFrame['ship-city_code'] = LE.fit_transform(dataFrame['ship-city'])
    if 'ship-state' in dataFrame.columns:
        dataFrame['ship-state_code'] = LE.fit_transform(dataFrame['ship-state'])
    if 'ship-country' in dataFrame.columns:
        dataFrame['ship-country_code'] = LE.fit_transform(dataFrame['ship-country'])
    return dataFrame

# 3° fase: visualizar os dados ()
def grafico1(dataFrame):
    plt.figure(figsize=(12, 8))
    state_sales = dataFrame.groupby('ship-state')['Amount'].sum().sort_values()
    sns.barplot(x=state_sales.index, y=state_sales.values, palette='coolwarm')
    plt.title('Total de Vendas por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Total de Vendas')
    plt.xticks(rotation=90)
    plt.show()

def grafico2(dataFrame):
    plt.figure(figsize=(12, 8))  # Aumentar o tamanho da figura
    state_sales = dataFrame.groupby('ship-state')['Amount'].sum()
    explode = [0.05 if val > state_sales.mean() else 0 for val in state_sales]    # Explodir as fatias maiores
    def autopct_format(pct):
        return ('%1.1f%%' % pct) if pct > 1 else ''  #Exibir porcentagens<1%
    # Criar o gráfico de pizza sem rótulos
    wedges, texts, autotexts = plt.pie(state_sales,autopct=autopct_format,  startangle=140, colors=sns.color_palette("coolwarm", len(state_sales)),pctdistance=0.85,  explode=explode)# Distância das porcentagens# Mostrar porcentagens
    for text in autotexts:    # Ajustar o tamanho das porcentagens
        text.set_fontsize(10)  # Tamanho da fonte para as porcentagens
    # Adicionar legenda fora do gráfico para exibir os nomes dos estados
    plt.legend(wedges, state_sales.index, title="Estados", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Participação de Vendas por Estado')
    plt.axis('equal')  # Garantir que o gráfico seja circular
    plt.show()
    
def grafico3(dataFrame):
    plt.figure(figsize=(12, 8))
    sns.histplot(dataFrame['Qty'], bins=30, kde=True)
    plt.title('Distribuição da Quantidade de Produtos Vendidos')
    plt.xlabel('Quantidade')
    plt.ylabel('Frequência')
    plt.show()    
    
def grafico4(dataFrame):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Qty', y='Amount', data=dataFrame)
    plt.title('Quantidade vs Valor Total de Vendas')
    plt.xlabel('Quantidade')
    plt.ylabel('Valor Total')
    plt.show()

def grafico5(dataFrame):
    if 'Order Date' in dataFrame.columns:
        dataFrame['Order Date'] = pd.to_datetime(dataFrame['Order Date'])  # Converter para datetime se necessário
        sales_over_time = dataFrame.groupby(dataFrame['Order Date'].dt.to_period('M'))['Amount'].sum()
        plt.figure(figsize=(12, 8))
        sales_over_time.plot(kind='line')
        plt.title('Vendas ao Longo do Tempo')
        plt.xlabel('Data')
        plt.ylabel('Total de Vendas')
        plt.show()
        
def pegar_maiores_vendas(dataFrame):
    # Agrupar por estado e somar as vendas
    state_sales = dataFrame.groupby('ship-state')['Amount'].sum().sort_values(ascending=False)
    # Selecionar os dois estados com maior volume de vendas
    top_two_states = state_sales.head(2)
    return top_two_states

# Função para gerar gráficos de comparação
def gerar_graficos_comparacao(dataFrame, dois_principais_estados_vendedores):
    # Filtrar os dados para os dois estados
    estados_filtrados = dataFrame[dataFrame['ship-state'].isin(dois_principais_estados_vendedores.index)]
    # Gráfico de Barras para comparar os dois estados
    plt.figure(figsize=(8, 6))
    sns.barplot(x=dois_principais_estados_vendedores.index, y=dois_principais_estados_vendedores.values, palette='coolwarm')
    plt.title('Comparação do Total de Vendas entre os Dois Estados que mais venderam')
    plt.xlabel('Estado')
    plt.ylabel('Total de Vendas')
    plt.show()
    # Gráfico de Linhas (se houver uma coluna de data)
    if 'Date' in dataFrame.columns:
        estados_filtrados['Date'] = pd.to_datetime(estados_filtrados['Date'])
        sales_over_time = estados_filtrados.groupby([estados_filtrados['Date'].dt.to_period('M'), 'ship-state'])['Amount'].sum().unstack()
        sales_over_time.plot(kind='line', figsize=(12, 8))
        plt.title('Vendas ao Longo do Tempo nos Dois Estados com Mais Vendas')
        plt.xlabel('Data')
        plt.ylabel('Total de Vendas')
        plt.show()
    # Gráfico de Dispersão
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='ship-state', y='Amount', hue='ship-state', data=estados_filtrados)
    plt.title('Scatter Plot: Vendas entre os Dois Estados')
    plt.xlabel('Estado')
    plt.ylabel('Total de Vendas')
    plt.show()


# Função para filtrar os estados/regiões com os menores valores de vendas
def filtrar_menores_vendas(dataFrame, limite):
    # Agrupar por estado e somar as vendas
    state_sales = dataFrame.groupby('ship-state')['Amount'].sum().sort_values()
    # Filtrar os estados/regiões com vendas abaixo do limite definido
    menores_vendas = state_sales[state_sales < limite]
    return menores_vendas

# Função para plotar os estados com menor volume de vendas
def plot_menores_vendas(menores_vendas):
    plt.figure(figsize=(12, 8))
    sns.barplot(x=menores_vendas.index, y=menores_vendas.values, palette='coolwarm')
    plt.title('Estados com Menores Vendas - Foco em Marketing')
    plt.xlabel('Estado')
    plt.ylabel('Total de Vendas')
    plt.xticks(rotation=90)
    plt.show()
limite_vendas = 700 # Limite de vendas abaixo do qual você quer focar

def estados_menos_vendas(dataFrame):# Função para pegar os dois estados/regiões com as menores vendas
    vendas_estados = dataFrame.groupby('ship-state')['Amount'].sum().sort_values() # Agrupando por estado e somando as vendas
    dois_menores_vendedores = vendas_estados.head(2)    # Selecionando dois estados com menor volume de vendas
    return dois_menores_vendedores

def plot_dois_menores_vendedores(dois_menores_vendedores):# Função para plotar os dois estados com menor volume de vendas
    plt.figure(figsize=(8, 6))
    sns.barplot(x=dois_menores_vendedores.index, y=dois_menores_vendedores.values, palette='coolwarm')
    plt.title('Comparação dos Dois Estados com Menores Vendas')
    plt.xlabel('Estado')
    plt.ylabel('Total de Vendas')
    plt.show()

def grafico6(dataFrame):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='ship-state', y='Amount', data=dataFrame)
    plt.title('Distribuição das Vendas por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Valor Total de Vendas')
    plt.xticks(rotation=90)
    plt.show()

arquivo = "C:\\Users\\Usuario\\Desktop\\Trabalho Jairo\\AmazonSaleReport.csv"
dataFrame = carregarDados(arquivo)
dataFrame = prepararDados(dataFrame)
grafico1(dataFrame)  
grafico2(dataFrame)  
grafico3(dataFrame)  
grafico4(dataFrame)  
grafico6(dataFrame)  
grafico5(dataFrame) 
dois_principais_estados_vendedores = pegar_maiores_vendas(dataFrame)
dois_menores_vendedores = estados_menos_vendas(dataFrame)
gerar_graficos_comparacao(dataFrame, dois_principais_estados_vendedores)
menores_vendas = filtrar_menores_vendas(dataFrame, limite_vendas)
plot_menores_vendas(menores_vendas)
plot_dois_menores_vendedores(dois_menores_vendedores)
