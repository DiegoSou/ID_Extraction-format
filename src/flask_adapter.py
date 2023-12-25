import json
from flask import Blueprint, request
from src.services import format_outscraper_result_service, phone_operator_name_split_service

# Ex:
# origin -> 'sem_mod/SP - São Paulo/nome_do_arquivo.xlsx'
# detail -> '{"concat_with":["sem_mod/SP - São Paulo/extracao_extra.xlsx", "sem_mod/SP - São Paulo/extracao_extra.xlsx"]}'
# result -> 'modified/nome_do_arquivo.xlsx'

flask_adapter = Blueprint("ext", __name__)
@flask_adapter.route('/format_outscrapper_result', methods=['GET', 'POST'])
def format_outscrapper_result():
    if request.method == 'POST':
        print('Starting - format outscrapper result process')
        
        request_params = request.form.to_dict()
        
        source_file_dir = request.files['origin']
        result_file_dir = request_params['result']
        request_detail = request_params['detail']
        
        # service call
        format_outscraper_result_service(source_file_dir, result_file_dir, request_detail)
        
        print('Finishing - format outscrapper result process')
    return {}
  
# Ex:    
# origin -> 'db_telein.csv'
# detail -> '{"cols":["latitude","longitude","name","place_id","query_location_city","query_location_state","query_location_country","type","owner_title","phoneOperator_operatorName"], "city":"Itabuna"}'
# result -> 'modified/nome_do_arquivo.xlsx'

@flask_adapter.route('/phone_operator_name_split', methods=['GET', 'POST'])
def phone_operator_name_split():
    if request.method == 'POST':
        print('Starting - phone operator name split process')
        
        request_params = request.form.to_dict()
        
        source_file_dir = request.files['origin']
        result_file_dir = request_params['result']
        request_detail = request_params['detail']
        
        # service call
        phone_operator_name_split_service(source_file_dir, result_file_dir, request_detail)
        
        print('Finishing - phone operator name split process')
    return {}
