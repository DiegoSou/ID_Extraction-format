from pandas import read_excel, read_csv
from src.utils import before_telein_cols, after_telein_cols, split_df_by_lines, split_df_by_operator, format_path
from src.filters import (
    FiltersPipeline,
    FilterCityState,
    FilterGlossaryTypes,
    FilterPlaceId,
    FilterByColumnsOrCity
)

def format_outscraper_result_service(source_file_dir, result_file_dir, detail):
    format_pipeline = FiltersPipeline(FilterPlaceId, FilterCityState, FilterGlossaryTypes)
    
    source_df = read_excel(source_file_dir, dtype=before_telein_cols)
    
    mod_df = format_pipeline(source_df, detail=detail)
    result_file_dir = format_path(result_file_dir)

    # Divide os dataframes em partes de 80000
    spplited_df_list = split_df_by_lines(mod_df, 80000)

    for indx, frame in enumerate(spplited_df_list):
        frame.to_excel(result_file_dir['folders'] + str(1+indx) + '_' + result_file_dir['file'], index=False)


def phone_operator_name_split_service(source_file_dir, result_file_dir, detail):
    format_pipeline = FiltersPipeline(FilterByColumnsOrCity)
    
    source_df = read_csv(source_file_dir, dtype=after_telein_cols)
    
    mod_df = format_pipeline(source_df, detail=detail)
    result_file_dir = format_path(result_file_dir)

    # Divide os dataframes por operadora
    spplited_df_list = split_df_by_operator(mod_df, {
        'oi' : ['OI'],
        'tim' : ['TIM'],
        'vivo' : ['VIVO', 'Telefônica Brasil'],
        'claro' : ['Claro', 'Embratel']
    })

    for op_key, op_item in spplited_df_list.items():
        # Divide os dataframes em partes de 2000 *(limite do google maps para pontos de localização)
        spplited_df_list = split_df_by_lines(op_item, 2000)

        for indx, frame in enumerate(spplited_df_list):
            frame.to_excel(result_file_dir['folders'] + str(1+indx) + '_' + str(op_key) + '_' + result_file_dir['file'], index=False)
