# Libraries
import streamlit as st
import func
import pandas as pd
import altair as alt

from datetime import date as dt
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
#st.sidebar.markdown('[![in](./static/linkedin.png)]()')

txt_side = '''
Projeto de Conclusão do Curso 3.0 - Big Data Real-Time Analytics com Python e Spark.  
[Data Science Academy](https://www.datascienceacademy.com.br/)
'''

st.sidebar.markdown(txt_side, unsafe_allow_html=True)
st.sidebar.image('./images/dsa.png')
#st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
###############################################################
# imagem com link usando static - verse funciona quando feito deploy
# st.sidebar.markdown("[![in](Analise_Risco_Trans_Publico/static/linkedin.png)](https://www.linkedin.com/in/roberto-balbinotti/)")

##############################################################

# leitura dos dados
@st.cache_data # quando ler pela segunda vez, utiliza o que está em cache
def load_data(url):
    '''Lê os dados'''
    df = pd.read_excel(url)
    # Extrai da variável
    month = df['Date Of Incident'].dt.strftime('%b')

    # Insere o mês extraido na segunda coluna do dataframe
    df.insert(1, 'Month', month)

    # Ordem dos meses
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Organiza ordem dos meses
    cat_month_order = CategoricalDtype(categories=month_order, ordered=True)

    # Cria categoriae ordenada
    df['Month'] = df.Month.astype(cat_month_order)

    # Cria categoria Year
    df['Year'] = df['Year'].astype('category')
    return df

df = load_data('https://query.data.world/s/vcpijynjkuc3ccycxh62juwmnitj6t?dws=00000')

################################################################

st.header('Análise :bar_chart:', divider='rainbow')
st.write('')
st.write('')

col1, col2, col3, col4, col5 = st.columns([2, 0.5, 2, 0.5, 4])

with col1:
    st.subheader('1- Qual a quantidade de incidentes por gênero?')

with col1:
    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            x='Victims Sex',
            y='count(Year)', )
        .properties(
            title='Incident for gender',
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

with col3:
    st.subheader('2- Qual faixa etária esteve mais envolvida nos incidentes?')

with col3:
    st.altair_chart(
        alt.Chart(df)
        .configure_title(
            fontSize=20,
            # font='Courier',
            anchor='middle',
            color='gray')
        .mark_bar()
        .encode(
            x=alt.X('Victims Age').sort('-y'),
            y='count(Year)'
        )
        .properties(
            title='Incident for age range',
            width='container',
            height=480
        )
        .configure_axisX(labelAngle=0).interactive(),
        use_container_width=True, theme='streamlit')

with col5:
    st.subheader('3- Qual o percentual de incidentes por tipo de evento?')

with col5:
    df_getype = pd.DataFrame(df.groupby(['Incident Event Type'], observed=True, as_index=False)['Year'].count()).sort_values(by='Year', ascending=False)
    df_getype['Percent'] = (df_getype['Year'] / df.shape[0]) * 100
    df_getype['Percent'] = df_getype.Percent.apply(func.formata_numero)

    chart_3 = (alt.Chart(df_getype,
                         title=alt.Title('Percent for incident event type',
                         anchor='middle', color='gray', fontSize=20))
               .mark_bar()
               .properties(width='container', height=480)
               .encode(x=alt.X('Year', title='Count', sort=None), y=alt.Y('Incident Event Type', sort=None))
               )

    annotation_layer = (
        alt.Chart(df_getype)
        .mark_text(size=12, align='left', color='gray', dx=10)
        .encode(x=alt.X('Year'), y=alt.Y('Incident Event Type', sort=None), text='Percent')
    )

    combined_chart = chart_3 + annotation_layer
    # Display chart
    st.altair_chart(combined_chart, use_container_width=True, theme='streamlit')


st.divider()

st.subheader('4- Como foi a evolução de incidentes por mês ao longo do tempo?')

col1, col2, col3 = st.columns([2, 0.5, 2])

count_incident = df.groupby(['Date Of Incident', 'Year', 'Month'], as_index=False, observed=True).count()

with col1:
    # Criando hover
    hover = alt.selection_single(
        fields=["Month"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Cria o gráfico
    lines = (
        alt.Chart(count_incident)
        .mark_line(point=True)
        .encode(x=alt.X('Month'), y=alt.Y('Route', title='Count')
                .scale(zero=False), color='Year', strokeDash='Year')
        .properties(title='Incident for gender', width='container', height=480)
    )

    # Points on hover
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Tooltips
    tooltips_line = (
        alt.Chart(count_incident)
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
    data_layer = ((lines + points + tooltips_line)
                  .configure_title(fontSize=20, anchor='middle', color='gray')
                  .configure_axisX(labelAngle=0)).interactive()

    st.altair_chart(data_layer, use_container_width=True, theme='streamlit')

with col3:
    # grafic accumulate for month
    st.altair_chart(
        alt.Chart(count_incident)
        .configure_title(
            fontSize=20,
            # font='Courier',
            anchor='middle',
            color='gray')
        .mark_bar()
        .encode(
            x=alt.X('Month'),
            y=alt.Y('Route', aggregate='sum', title='Total')
        )
        .properties(
            title='Accumulate incident for Month - Year 2015/2018',
            width='container',
            height=480
        )
        .configure_axisX(labelAngle=0).interactive(),
        use_container_width=True, theme='streamlit')

st.divider()
