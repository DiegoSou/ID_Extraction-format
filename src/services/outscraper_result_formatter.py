from json import loads
from pandas import read_excel

from src.filters import FiltersPipeline, FilterPlaceId, FilterCityState, FilterGlossaryTypes
from src.utils import before_telein_cols, split_df_by_lines,format_path


def handle(source_file_dir, result_file_dir, detail):
    print('Starting - format outscrapper result process')
    
    format_pipeline = FiltersPipeline(FilterPlaceId, FilterCityState, FilterGlossaryTypes)
    source_df = read_excel(source_file_dir, dtype=before_telein_cols)
    
    mod_df = format_pipeline(source_df, detail=loads(detail))
    result_file_dir = format_path(result_file_dir)

    results = []

    # Divide os dataframes em partes de 80000
    spplited_df_list = split_df_by_lines(mod_df, 50000)

    for indx, frame in enumerate(spplited_df_list, 1):
        result_name = str(indx) + '_' + result_file_dir['file'] # 1_resultados.xlsx
        result_dir = result_file_dir['folders'] + result_name # path/path/path/1_resultados.xlsx
        
        results.append(
            [frame, result_name, result_dir]
        )
    
    print('Finishing - format outscrapper result process')
    return results
