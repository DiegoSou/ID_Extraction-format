import time
import streamlit as st
from src.services import format_outscraper_result_service, phone_operator_name_split_service

def st_callback(func):
    def inner(*args, **kwargs):
        with st.spinner('Processing and generating new files'):
            func(*args, **kwargs)        
        
        col1, col2 = st.columns([11, 1])
        info = col1.info('Done')
        col2.button('❌', on_click=info.empty)

    return inner

@st_callback
def service_call(service_name, req_origin_file, req_result_dir, req_detail):
    if service_name == 'format_outscraper_result':
        format_outscraper_result_service(req_origin_file, req_result_dir, req_detail)
        
    if service_name == 'phone_operator_name_split':
        phone_operator_name_split_service(req_origin_file, req_result_dir, req_detail)


def format_outscraper_result_route():
    request_origin_file = st.file_uploader('Arquivo com os resultados da extração', type=['xlsx'])
    
    detail_default_value = '{"concat_with":[]}'
    
    request_result_directory = 'modified/resultados.xlsx'
    request_detail = st.text_area('Configurações para a formatação', value=detail_default_value)
    
    if request_origin_file is not None:
        st.button(
            'Enviar',
            type='primary',
            on_click=service_call,
            args=('format_outscraper_result', request_origin_file, request_result_directory, request_detail)
        )
   

def phone_operator_name_split_route():
    request_origin_file = st.file_uploader('Arquivo com as informações de operadora', type=['csv'])
    
    detail_dafault_value = '{"cols":["latitude","longitude","name","place_id","query_location_city","query_location_state","query_location_country","type","owner_title","phoneOperator_operatorName"], "city":"SAO PAULO"}'
    
    request_result_directory = 'modified/resultados_operadora.xlsx'
    request_detail = st.text_area('Configurações para a formatação', value=detail_dafault_value)
    
    if request_origin_file is not None:
        st.button(
            'Enviar',
            type='primary',
            on_click=service_call,
            args=('phone_operator_name_split', request_origin_file, request_result_directory, request_detail)
        )


def st_init():
    st.markdown('## Extração Claro')

    with st.expander('Sessão 1: Formatar resultados do Outscrapper'):
        format_outscraper_result_route()
        
    with st.expander('Sessão 2: Dividir resultados pelo nome da operadora'):
        phone_operator_name_split_route()

