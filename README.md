# Análise de Vendas da Amazon na Índia - README

Este projeto tem como objetivo analisar os dados de vendas da Amazon na Índia ao longo de 3 meses, utilizando a metodologia CRISP-DM (Cross-Industry Standard Process for Data Mining). A análise abrange diferentes regiões (estados) da Índia, com foco em identificar oportunidades para melhorar a estratégia de marketing e expandir as vendas. A seguir, descrevemos o contexto e os objetivos de cada etapa do código, bem como a justificativa para as decisões tomadas.

## Contexto

Os dados representam o histórico de vendas da Amazon na Índia por 3 meses, distribuídos por diversos estados e regiões. O foco da análise é avaliar o desempenho das vendas por estado e identificar regiões com maior e menor volume de vendas. A análise permite:
- Identificar os estados com as maiores vendas e decidir se devemos continuar investindo nessas regiões para maximizar o crescimento.
- Detectar estados com baixo volume de vendas e investigar como melhorar o desempenho, seja replicando estratégias bem-sucedidas ou realizando campanhas de marketing mais agressivas.

## Objetivos da Análise

1. **Avaliar os Estados com Maiores Vendas**: 
   - Analisar os dois estados que apresentaram maior volume de vendas.
   - Entender o comportamento de vendas ao longo do tempo nesses estados.
   - Replicar as estratégias aplicadas nesses estados para outras regiões que estão vendendo menos.
   
2. **Focar nas Regiões com Menores Vendas**:
   - Identificar as regiões com vendas abaixo de um determinado limite.
   - Propor ações de marketing ou outras intervenções para aumentar as vendas nessas áreas.

## Estrutura do Código

### 1. Carregamento e Preparação dos Dados

Funções responsáveis por carregar e preparar o dataset:

- **`carregarDados(nomePathArquivo)`**: Carrega o dataset CSV com as informações de vendas. O dataset contém colunas como `Order ID`, `Date`, `Qty`, `Amount`, e informações sobre as regiões (`ship-state`).
  
- **`prepararDados(dataFrame)`**: Limpa e prepara os dados para análise, removendo colunas irrelevantes, duplicatas e tratando valores nulos. Também converte as variáveis categóricas (como estados e cidades) em códigos numéricos para facilitar a análise.

### 2. Análise de Estados com Maiores Vendas

- **`pegar_maiores_vendas(dataFrame)`**: Agrupa os dados por estado e seleciona os dois estados que apresentaram o maior volume de vendas. Esses estados podem receber mais investimento para expandir o crescimento ou manter sua boa performance.

- **`gerar_graficos_comparacao(dataFrame, top_two_states)`**: Gera gráficos para comparar os dois estados com maior volume de vendas ao longo do tempo. Essa análise ajuda a entender o comportamento sazonal das vendas, picos de demanda e a necessidade de ajustar ou reforçar campanhas de marketing nesses estados.

### 3. Análise de Estados com Menores Vendas

- **`filtrar_menores_vendas(dataFrame, limite)`**: Filtra as regiões que tiveram vendas abaixo de um determinado limite, possibilitando focar em regiões que podem ser alvo de campanhas para aumentar o desempenho.

- **`plot_menores_vendas(menores_vendas)`**: Gera um gráfico para visualizar os estados com menores vendas, que podem ser o foco de ações de marketing mais intensas.

- **`pegar_dois_menores_vendas(dataFrame)`**: Identifica os dois estados com o menor volume de vendas, destacando onde as estratégias atuais podem não estar funcionando ou onde há potencial para melhorar.

### 4. Visualizações

O código gera várias visualizações para facilitar a análise:

- **Gráfico de Barras (Total de Vendas por Estado)**: Visualiza o volume total de vendas por estado e identifica as regiões com melhor desempenho.
  
- **Gráfico de Pizza (Participação de Vendas por Estado)**: Mostra a participação de cada estado no volume total de vendas.

- **Gráfico de Dispersão (Quantidade vs Valor Total de Vendas)**: Avalia a relação entre a quantidade de itens vendidos e o valor total, o que pode ajudar a entender o comportamento de vendas em relação ao volume de produtos.

- **Gráfico de Linhas (Vendas ao Longo do Tempo)**: Para regiões de maior interesse, visualiza como as vendas variaram ao longo dos meses.

- **Gráfico de Boxplot (Distribuição das Vendas por Estado)**: Ajuda a identificar outliers e variações significativas nas vendas entre os diferentes estados.

### 5. Decisões Estratégicas Baseadas nos Dados

Com base nas visualizações geradas, é possível tomar decisões como:

- **Investir nas Regiões com Maiores Vendas**: Se os dados mostram que certas regiões estão apresentando bons resultados, pode ser interessante continuar investindo nelas para garantir um crescimento contínuo.
  
- **Intervir nas Regiões com Menores Vendas**: As regiões com vendas abaixo da média podem ser o alvo de campanhas de marketing, ajustes de preços ou melhorias logísticas para aumentar seu desempenho. Replicar as boas práticas aplicadas nas regiões de maior sucesso pode ser uma estratégia eficaz.

## Dados

O dataset utilizado contém as seguintes colunas principais:
- **Order ID**: Identificador único de cada pedido.
- **Date**: Data do pedido.
- **Qty**: Quantidade de itens vendidos.
- **Amount**: Valor total do pedido.
- **ship-state**: Estado para o qual o pedido foi enviado.
- **ship-city**: Cidade de envio.
  
Esses dados permitem uma análise regional detalhada, facilitando a identificação de oportunidades de expansão ou intervenção.

## Instruções de Uso

1. Certifique-se de ter os pacotes necessários instalados:
   - pandas
   - matplotlib
   - seaborn
   - scikit-learn

2. Altere o caminho do arquivo `AmazonSaleReport.csv` para o local onde o arquivo de vendas está armazenado.

3. Execute o script para gerar as visualizações e obter insights sobre o desempenho de vendas por estado na Índia.

4. Use as visualizações para tomar decisões estratégicas sobre onde investir mais em campanhas de marketing e onde replicar as estratégias de sucesso.