# Libraries
import streamlit as st
import pandas as pd
import altair as alt

from pandas.api.types import CategoricalDtype

# configuração da página e dos menus (são os 3 pontos à direita da página)
st.set_page_config(
    page_title='London Bus Safety Analysis',
    page_icon=':oncoming_bus:',
    layout='wide',
    menu_items={
        'Get Help': 'https://streamlit.io/',
        'Report a bug': "https://github.com/rbalbinotti/Analise_Risco_Transp_Publico",
        'About': "## London Bus Safety Analysis\n"
                 "#### Curse Big Data Real-Time Analytics with Python and Spark\n"
                 "**in Data Science Academy** - by Roberto Balbinotti"
    }
)

###############################################################################################

assin = '''**Roberto R Balbinotti**
[Linkedin](https://www.linkedin.com/in/roberto-balbinotti/) - [GitHub](https://github.com/rbalbinotti/)'''

# Sidebar
st.sidebar.write('Criado por:')
st.sidebar.markdown(assin, unsafe_allow_html=True)

txt_side = '''
Projeto de Conclusão do Curso 3.0 - Big Data Real-Time Analytics com Python e Spark.  
[Data Science Academy](https://www.datascienceacademy.com.br/)
'''

st.sidebar.markdown(txt_side, unsafe_allow_html=True)
st.sidebar.image('./images/dsa.png')


# leitura dos dados
@st.cache_data  # quando ler pela segunda vez, utiliza o que está em cache
def load_data(url):
    """Lê os dados"""
    data = pd.read_excel(url)
    # Extrai da variável
    month = data['Date Of Incident'].dt.strftime('%b')

    # Insere o mês extraido na segunda coluna do dataframe
    data.insert(1, 'Month', month)

    # Ordem dos meses
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Organiza ordem dos meses
    cat_month_order = CategoricalDtype(categories=month_order, ordered=True)

    # Cria categoriae ordenada
    data['Month'] = data.Month.astype(cat_month_order)

    # Cria categoria Year
    data['Year'] = data['Year'].astype('category')
    return data


df = load_data('https://query.data.world/s/vcpijynjkuc3ccycxh62juwmnitj6t?dws=00000')

################################################################

st.header('Continuando a Análise :bar_chart:', divider='rainbow')
st.write('')
st.write('')

sex_list = df['Victims Sex'].unique().tolist()
df_type = df[df['Incident Event Type'] == 'Collision Incident']

col1, col2, col3 = st.columns([2, 0.5, 4])

with col1:
    st.subheader('5- Quando o incidente foi “Collision Incident” em qual mês houve o maior número de incidentes '
                 'envolvendo pessoas do sexo feminino?')
    st.write('O mês que acumula o maior nível de incidentes envolvendo gênero feminino e colisão foi **setembro** com '
             '**158** eventos.')
    options = st.multiselect('Select Gender', sex_list, default=sex_list)


with col3:

    st.altair_chart(
        alt.Chart(df_type[df_type['Victims Sex'].isin(options)])
        .configure_title(
            fontSize=20,
            anchor='middle',
            color='gray')
        .mark_bar()
        .encode(
            x=alt.X('Month'),
            xOffset='Victims Sex:N',
            y=alt.Y('Route', aggregate='count', title='Count'),
            color=alt.Color('Victims Sex:N')
        )
        .properties(
            title='Collision incident for gender',
            width='container',
            height=480
        )
        .configure_axisX(labelAngle=0).interactive(),
        use_container_width=True, theme='streamlit')

st.divider()

col1, col2, col3 = st.columns([5, 0.15, 3])

with col1:
    st.subheader('6- Qual foi a média de incidentes por mês envolvendo crianças?')

with col1:
    # Agrupa
    df_child = df.groupby(['Month', 'Victims Age'], observed=False, as_index=False)['Year'].count()

    # Soma quantidade de anos do dataframe
    year_count = df.Year.unique().value_counts().sum()

    # Calcula média# .transform_filter(df['Victims Sex'] )
    df_child['Mean'] = (df_child.Year / year_count)
    # Filtra
    df_child_mean = df_child[df_child['Victims Age'] == 'Child']
    # df_child_mean

    chart_6 = (alt.Chart(df_child_mean, title=alt.Title('Mean child victims for month - period(2015-18)',
                                                        anchor='middle', color='gray', fontSize=20))
               .mark_bar()
               .properties(width='container', height=480)
               .encode(x=alt.X('Month', axis=alt.Axis(labelAngle=0)), y=alt.Y('Mean', title=''))
               )

    annotation_layer_2 = (
        alt.Chart(df_child_mean)
        .mark_text(size=12, align='center', color='gray', dy=-10)
        .encode(x='Month', y=alt.Y('Mean'), text='Mean')
    )

    combined_chart_2 = chart_6 + annotation_layer_2
    # Display chart
    st.altair_chart(combined_chart_2, use_container_width=True, theme='streamlit')

with col3:
    st.subheader('7- Considerando a descrição de incidente como “Injuries treated on scene”, '
                 'qual o total de incidentes de pessoas do sexo masculino e sexo feminino?')

with col3:
    # Agrupa
    onscene = df.groupby(['Injury Result Description', 'Victims Sex'], observed=False, as_index=False)['Year'].count()
    # Filtra
    onscene = onscene[onscene['Injury Result Description'] == 'Injuries treated on scene']

    st.altair_chart(
        alt.Chart(onscene)
        .configure_title(
            fontSize=20,
            anchor='middle',
            color='gray')
        .mark_bar()
        .encode(
            x=alt.X('Victims Sex'),
            y=alt.Y('Year', title='')
        )
        .properties(
            title='Injuries treated on scene for gender - Year (2015-18)',
            width='container',
            height=360
        )
        .configure_axisX(labelAngle=0).interactive(),
        use_container_width=True, theme='streamlit')

col1, col2, col3 = st.columns([2, 0.2, 2])

with col1:
    st.subheader('8- No ano de 2017 em qual mês houve mais incidentes com idosos?')

with col1:
    # Criando hover
    hover = alt.selection_single(
        fields=["Month"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Agrupa
    elderly = df.groupby(['Month', 'Victims Age', 'Year'], observed=False, as_index=False)['Route'].count()

    # Faz o filtro por idade e ano
    elderly = elderly[(elderly['Victims Age'] == 'Elderly') & (elderly['Year'] == 2017)]

    chart_8 = (alt.Chart(elderly,
                         title=alt.Title('Incident with elderly in 2017', anchor='middle',
                                         color='gray', fontSize=20))
               .mark_area(line=True, point=True, opacity=0.1)
               .properties(width='container', height=480)
               .encode(x=alt.X('Month', axis=alt.Axis(labelAngle=0)), y=alt.Y('Route:Q', title='Count'))
               )

    annotation_layer_8 = (
        alt.Chart(elderly)
        .mark_text(size=12, align='center', color='gray', dy=-15)
        .encode(x='Month', y=alt.Y('Route'), text='Route')
    )

    # Points on hover
    points = chart_8.transform_filter(hover).mark_circle(size=65)

    # Tooltips
    tooltips_line = (
        alt.Chart(elderly)
        .mark_rule()
        .encode(
            x="Month",
            y="Route",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Month", title="Month"),
                alt.Tooltip("Route", title="Qty"),
            ],
        )
        .add_selection(hover)
    )

    # Conect all
    data_layer = ((chart_8 + annotation_layer_8 + points + tooltips_line)
                  .configure_title(fontSize=20, anchor='middle', color='gray')
                  .configure_axisX(labelAngle=0)).interactive()

    # st.altair_chart(data_layer, use_container_width=True, theme='streamlit')

    # combined_chart_8 = data_layer + annotation_layer_8
    # Display chart# Criando hover
    hover = alt.selection_single(
        fields=["Month"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    st.altair_chart(data_layer, use_container_width=True, theme='streamlit')


with col3:
    st.subheader('9- Qual o tipo de incidente mais comum com ciclistas?')

with col3:
    # Remove espaços no início e final das palavras
    df['Victim Category'] = df['Victim Category'].str.strip()

    # Filtra somente ciclistas
    cyclist = df[df['Victim Category'] == 'Cyclist']
    # cyclist

    st.altair_chart(
        alt.Chart(cyclist)
        .mark_bar()
        .encode(
            x='Incident Event Type',
            y='count(Year)', )
        .properties(
            title='Incident type by cyclist',
            width='container',
            height=480
        )
        .configure_title(
            fontSize=20,
            # font='Courier',
            anchor='middle',
            color='gray'
        )
        .configure_axisX(labelAngle=0).interactive()
        , use_container_width=True, theme='streamlit')

st.divider()

col4, col5, col6 = st.columns([1, 6, 1])

with col5:
    st.subheader('10- Considerando o Operador qual a distribuição de incidentes ao longo do tempo?')

with col5:
    # Agrupa
    operator = (df.groupby('Operator', observed=False, as_index=False)['Year']
                .count()
                .sort_values(by='Year', ascending=False))

    chart_9 = (alt.Chart(operator,
                         title=alt.Title('Operator incident distribuition - year (2015-2018)',
                                         anchor='middle', color='gray', fontSize=20))
               .mark_bar()
               .properties(width='container', height=640)
               .encode(x=alt.X('Year', title='Count'), y=alt.Y('Operator', sort=None))
               )

    annotation_layer_9 = (
        alt.Chart(operator)
        .mark_text(size=12, align='left', color='gray', dx=3)
        .encode(x=alt.X('Year:Q'), y=alt.Y('Operator:N', sort=None), text='Year')
    )

    combined_chart_9 = chart_9 + annotation_layer_9
    # Display chart
    st.altair_chart(combined_chart_9, use_container_width=True, theme='streamlit')
