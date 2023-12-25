from json import loads
from pandas import read_csv

from src.filters import FiltersPipeline, FilterByColumnsOrCity
from src.utils import after_telein_cols, split_df_by_lines, split_df_by_operator, format_path


def handle(source_file_dir, result_file_dir, detail):
    print('Starting - phone operator name split process')
    
    format_pipeline = FiltersPipeline(FilterByColumnsOrCity)
    source_df = read_csv(source_file_dir, dtype=after_telein_cols)
    
    mod_df = format_pipeline(source_df, detail=loads(detail))
    result_file_dir = format_path(result_file_dir)

    results = []

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

        for indx, frame in enumerate(spplited_df_list, 1):
            result_name = str(indx) + '_' + str(op_key) + '_' + result_file_dir['file'] # 1_claro_resultados.xlsx
            result_dir = result_file_dir['folders'] + result_name # path/path/path/1_claro_resultados.xlsx
            
            results.append(
                [frame, result_name, result_dir]
            )
            
    print('Finishing - phone operator name split process')
    return results