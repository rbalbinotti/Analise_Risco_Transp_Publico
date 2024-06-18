# Analytics com Python

> Análise de Risco no Transporte Público - *London Bus Safety Analysis*.  
> **Curso - Big Data Real-Time Analytics Com Python e Spark - Versão 3.0**  
> Projeto da Formação Cientista de Dados da [Data Science Academy](https://www.datascienceacademy.com.br/)

## Descrição Projeto

- Quais incidentes de trânsito ocorrem com mais frequência?
- Qual a faixa etária que mais se envolve em incidentes de trânsito? Qual o evento mais comum nos incidentes?
- Passageiros ou pedestres são as maiores vítimas dos incidentes?
st.get_option(key)
Essas e outras perguntas devem ser respondidas através da análise de dados reais disponíveis publicamente. Este projeto não requer Machine Learning e seu trabalho é aplicar suas habilidades de análise e responder diversas perguntas de negócio através de gráficos e storytelling.

Para a construção desse projeto, recomendamos a utilização da Linguagem Python e Linguagem SQL e o dataset disponível para download no link: [data.world](https://data.world/makeovermonday/2018w51)

O conjunto de dados lista incidentes de trânsito ocorridos na cidade de Londres.

---

## Fonte Dados

-   Andy Kriebel [link](https://data.world/vizwiz)
-   [Data.world](https://data.world/)
-   [Data Science Academy](https://www.datascienceacademy.com.br)
---
## Tecnologias Empregadas

- Conda
- Jupyterlab
- Python
- Pandas
- Seaborn
- Streamlit
- Vega-Altair
- Github
- Pycharm

### Instalação

- Criar um ambiente de trabalho com o conda
```
conda create --name busSafe --file requirements.txt
```
- Depois de criado ativa ambiente
```
conda activate busSafe
```
- Rodar aplicativo Streamlit (obs: com ambiente ativado e dentro da pasta de trabalho)
```
# baixando o repositório
streamlit run Bus_Safety.py

# direto do GitHub
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```
---
## Objetivo
#### Trabalho é analisar os dados e construir gráficos que respondam a essas 10 perguntas abaixo:

> 1. Qual a quantidade de incidentes por gênero?
> 2. Qual faixa etária esteve mais envolvida nos incidentes?  
> 3. Qual o percentual de incidentes por tipo de evento (Incident Event Type)?
> 4. Como foi a evolução de incidentes por mês ao longo do tempo?
> 5. Quando o incidente foi “Collision Incident” em qual mês houve o maior número de incidentes envolvendo pessoas do sexo feminino?
> 6. Qual foi a média de incidentes por mês envolvendo crianças (Child)?
> 7. Considerando a descrição de incidente como “Injuries treated on scene” (coluna Injury Result Description), qual o total de incidentes de pessoas do sexo masculino e sexo feminino?
> 8. No ano de 2017 em qual mês houve mais incidentes com idosos (Elderly)?
> 9. Considerando o Operador qual a distribuição de incidentes ao longo do tempo?
> 10. Qual o tipo de incidente mais comum com ciclistas?

## Vizualização projeto
- [Projeto em Streamlit](https://londonbusanalysis.streamlit.app/)

# Bibliografia e Créditos

### Material de Apoio
- [Markdown Guide](https://www.markdownguide.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn](https://seaborn.pydata.org/)
- [Python](https://docs.python.org/3/)
- [Streamlit](https://streamlit.io/)
- [Vega-Altair](https://altair-viz.github.io/getting_started/overview.html)

### Créditos

Material criado por **Roberto R Balbinotti**.  
Projeto de Conclusão do Curso 3.0 - Big Data Real-Time Analytics com Python e Spark da [Data Science Academy](https://www.datascienceacademy.com.br/)