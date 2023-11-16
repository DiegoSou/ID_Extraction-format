import json
from flask import Blueprint, request
from pandas import read_excel, read_csv

from src.utils import (
    split_df_by_lines,
    split_df_by_operator,
    format_path,
    before_telein_cols,
    after_telein_cols
)
from app_composer import extraction_composite, after_telein_composite


extraction_routes = Blueprint("ext", __name__)
# Members of API route

@extraction_routes.route('/generate_extraction', methods=['GET', 'POST'])
def extraction_03():

    # origin -> 'sem_mod/SP - São Paulo/nome_do_arquivo.xlsx'
    # detail -> '{"concat_with":["sem_mod/SP - São Paulo/extracao_extra.xlsx", "sem_mod/SP - São Paulo/extracao_extra.xlsx"]}'
    # result -> 'modificado/nome_do_arquivo.xlsx'

    if request.method == 'POST':

        print('Starting process')

        body_args = request.form.to_dict()

        origin_dir = request.files['origin']
        result_dir = format_path(body_args['result'])

        mod_df = extraction_composite(
            base_df=read_excel(
                        origin_dir,
                        dtype=before_telein_cols
                    ),
            detail=json.loads(
                        body_args['detail']
                    )
        )

        # Split dataframes in 80.100 lines per df
        spplited_df_list = split_df_by_lines(mod_df, 80100)

        for indx, frame in enumerate(spplited_df_list):

            frame.to_excel(
                result_dir['folders'] + str(1+indx) + '_' + result_dir['file'],
                index=False
            )

    print('Exiting process')
    return {}


@extraction_routes.route('/extract_operators', methods=['GET','POST'])
def after_telein():

    # origin -> 'db_telein.csv'
    # detail -> '{"cols":["latitude","longitude","name","place_id","query_location_city","query_location_state","query_location_country","type","owner_title","phoneOperator_operatorName"], "city":"Itabuna"}'
    # result -> 'modificado/nome_do_arquivo.xlsx'

    if request.method == 'POST':

        print('Starting process')

        body_args = request.form.to_dict()

        origin_dir = request.files['origin']
        result_dir = format_path(body_args['result'])

        mod_df = after_telein_composite(
            base_df=read_csv(
                        origin_dir,
                        dtype=after_telein_cols
                    ),
            detail=json.loads(
                        body_args['detail']
                    )
        )

        # Split dataframes by phone operator name
        spplited_df_list = split_df_by_operator(
                                mod_df,
                                {
                                    'oi' : ['OI'],
                                    'tim' : ['TIM'],
                                    'vivo' : ['VIVO', 'Telefônica Brasil'],
                                    'claro' : ['Claro', 'Embratel']
                                }
                            )

        for op_key, op_item in spplited_df_list.items():

            # Split items in 2.000 lines per df
            spplited_df_list = split_df_by_lines(op_item, 2000)

            for indx, frame in enumerate(spplited_df_list):

                frame.to_excel(
                    result_dir['folders'] + str(1+indx) + '_' + str(op_key) + '_' + result_dir['file'],
                    index=False
                )

    print('Exiting process')
    return {}
