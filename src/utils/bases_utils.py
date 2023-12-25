from pandas import DataFrame, Series, read_csv, merge, concat, isnull

categories = read_csv("resources/glossario_de_tipos.csv").rename(columns={'Type' : 'type','Categoria' : 'category'}).set_index('type')

### DATAFRAME UTILS
def drop_unnamed(df: DataFrame) -> DataFrame:
    """remove colunas unnamed do dataframe"""
    return df.drop(df.columns[df.columns.str.contains('unnamed',case = False)], axis = 1)

def merge_categories(df: DataFrame) -> Series:
    """refatora coluna de categorias de acordo com a especificação das categorias"""
    return (
        merge(
            df,
            categories,
            how='left',
            left_on='type',
            right_index=True,
            suffixes=('', '_y')
        )
        .apply(
            lambda row: row['category'] if isnull(row['category_y']) else row['category_y'],
            axis=1
        )
    )

def split_df_by_lines(df: DataFrame, limit_lines: int) -> list[DataFrame]:
    """divide o dataframe em partes limitando o nº de linhas"""
    result_list = []

    for i in range(1+ int(len(df.index)/limit_lines)):
        start = (i) * limit_lines  # 0 * 50.000
        end = (i+1) * limit_lines  # 1 * 50.000
        result_list.append(df.iloc[start:end])
        
    return result_list

def split_df_by_operator(df: DataFrame, operators_dict: dict[str, list]) -> dict[str, DataFrame]:
    """divide o dataframe em partes limitando por operadora"""
    result_dict = {'outro' : df.copy()}

    # Vai retirando do dataframe principal os que batem com a operadora
    for opr_key, opr_list in operators_dict.items():
        # Salva em uma 'key' os da operadora
        result_dict[str(opr_key)] = result_dict['outro'].loc[df['phoneOperator_operatorName'].isin(opr_list)]
        # Retira os salvos
        result_dict['outro'].drop(
            (result_dict[str(opr_key)]).index,
            inplace=True
        )

    return result_dict

### GENERAL UTILS
def format_path(file_path: str) -> dict[str, str]:
    """divide um diretório em local das pastas e nome do arquivo"""
    file_path = file_path.split('/')
    file_path.reverse()
    
    return {
        'folders' : "/".join(file_path[1:]) + "/",
        'file' : file_path[0]
    }
