import streamlit as st
import pandas as pd

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

st.header('Conhecendo o Dataframe :card_file_box:', divider='rainbow')

st.write('')
st.dataframe(df)

text = '''
    Fonte site [Data.world](https://data.world/)
    '''

col1, col2 = st.columns([3,1])
# col2.caption(text, )

col1.caption('Dados acidentes envolvendo transporte ônibus - Londres, UK.  Fonte: [Data.world](https://data.world/)')
