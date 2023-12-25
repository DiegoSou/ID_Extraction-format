import streamlit as st
import pandas as pd
from src.services import outscraper_result_handler, phone_operator_handler

dataframe_results = [] # [[dataframe, 'Result Name', 'Result Directory'], ...]

# Loading decorator
def st_callback(func):
    def inner(*args, **kwargs):
        with st.spinner('Processing and generating new files'):
            return_value = func(*args, **kwargs)        
        col1, col2 = st.columns([11, 1])
        col2.button('❌', on_click=col1.info('Done').empty)
        return return_value
    return inner

# Add to df results decorator
def df_result_callback(func):
    def inner(*args, **kwargs):
        st_cb_func = st_callback(func)
        new_results = st_cb_func(*args, **kwargs)
        dataframe_results.extend(new_results)
    return inner

# Routes

def format_outscraper_result_route():
    request_origin_file = st.file_uploader('Arquivo com os resultados da extração', type=['xlsx'])
    request_result_directory = st.text_input(label='Diretório para os resultados', key='ext_route_result_dir', value='modified/resultados_operadora.xlsx')
    
    detail_default_value = '{"concat_with":[]}'
    request_detail = st.text_area('Configurações para a formatação', value=detail_default_value)
    
    if request_origin_file is not None:
        st.button(
            'Enviar',
            key='ext_route_send_btn',
            type='primary',
            on_click=df_result_callback(outscraper_result_handler),
            args=(request_origin_file, request_result_directory, request_detail)
        )


def phone_operator_name_split_route():
    request_origin_file = st.file_uploader('Arquivo com as informações de operadora', type=['csv'])
    request_result_directory = st.text_input(label='Diretório para os resultados', key='op_route_result_dir', value='modified/resultados_operadora.xlsx')
    
    detail_dafault_value = '{"cols":["latitude","longitude","name","place_id","query_location_city","query_location_state","query_location_country","type","owner_title","phoneOperator_operatorName"], "city":"SAO PAULO"}'
    request_detail = st.text_area('Configurações para a formatação', value=detail_dafault_value)
    
    if request_origin_file is not None:
        st.button(
            'Enviar',
            key='op_route_send_btn',
            type='primary',
            on_click=df_result_callback(phone_operator_handler),
            args=(request_origin_file, request_result_directory, request_detail)
        )


# Update results
def update_results():
    def download(frame, dir):
        frame.to_excel(dir, index=False)
    
    st.markdown('## Resultados')
    for i, item in enumerate(dataframe_results):
        with st.expander(item[1]):
            st.dataframe(item[0])
            st.button('Download', key=str(i) + '_' + item[2], on_click=download(item[0], item[2]))

# Init
def st_init():
    st.markdown('## Rotas')

    with st.expander('Sessão 1: Formatar resultados do Outscrapper'):
        format_outscraper_result_route()   
    with st.expander('Sessão 2: Dividir resultados pelo nome da operadora'):
        phone_operator_name_split_route()
    
    if len(dataframe_results) > 0:
        update_results()
