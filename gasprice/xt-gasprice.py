from datetime import datetime
import requests
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.datasets import register_url
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS



@st.cache(allow_output_mutation=True)
def get_html_coviddata():
    register_url("https://echarts-maps.github.io/echarts-countries-js/")
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'cache-control': 'max-age=0',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
          }
    url = 'https://gasprices.aaa.com/state-gas-price-averages/'
    resp = requests.get(url, headers=headers)
    data = pd.read_html(resp.text)[0]
    
    cols = ['Regular', 'Mid-Grade','Premium','Diesel']
    data[cols] = data[cols].replace(r'[$,]', '', regex=True).astype('float64')
    return data


def draw_map(data, col_name):
    data = data.copy()  
    col = col_name.title().replace(' ', '')
    data[col] = data[col].map(lambda x: np.nan if pd.isna(x) else float(x))
    max_, min_ = data[col].max(), data[col].min()
    c = (
        Map()
        .add(col_name, data[['State', col]].values, '美国', is_map_symbol_show=False)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Gas Price in U.S ({col_name}) : {datetime.today().strftime('%m-%d-%Y')}"),
            visualmap_opts=opts.VisualMapOpts(max_=max_, min_=min_, precision=True),
            legend_opts=opts.LegendOpts(selected_mode='single',
                                       pos_top='bottom')
        )
    )
    return c.render_embed()

## Page expands to full width
st.set_page_config(layout="wide")

# Title
st.title("U.S Today's Gasprice")
st.markdown("""
**Data source:** [AAA GAS PRICE](https://gasprices.aaa.com/state-gas-price-averages/)

""")


# get_covid_data for usa
price_data = get_html_coviddata()


# selected box
choice = ['Regular', 'Mid-Grade', 'Premium', 'Diesel']
choice_selected = st.selectbox("Select Gas Type", choice)
st.write(choice_selected)
# Draw Map
components.html(draw_map(price_data, choice_selected), width=3000, height=600)

st.write('---')



#layout
col1,col2 = st.columns(2)

#Show the top gas price in selected gas type
def price_plot(data, column, num):
    data = data.copy()
    plt.figure(figsize=(5,7))
    plt.subplots_adjust(top=1, bottom=0)
    data = data[['State', column]].sort_values(by=column, ascending=False)[:num].copy()
    plt.barh(data['State'], data[column], label=column)
    plt.xlabel('$ Dallor')
    plt.ylabel('States')
    plt.legend(loc='upper right')
    return plt

col1.subheader('Show the top gas price in selected gas type')
num_states = col1.slider('Slider to get numbers of top gas price in states', 1, 50, 15)
st.set_option('deprecation.showPyplotGlobalUse', False)
col1.pyplot(price_plot(price_data, choice_selected, num_states))


#wordcloud for seletced gas type
col2.subheader("Today's Gas Price")
price_data1=price_data.copy()
col2.write(price_data1)
price_data1= price_data1[['State',choice_selected]]
dict = {} 
for col in price_data1.values:
    dict[col[0]] = col[1]
wordcloud = WordCloud(background_color = 'White', width=1920,height=1080)
wordcloud.generate_from_frequencies(dict)
plt.figure(figsize=(5,8))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
col2.subheader('Wordcloud for Selected Gas Price')
col2.pyplot(plt)

col2.write('---')
