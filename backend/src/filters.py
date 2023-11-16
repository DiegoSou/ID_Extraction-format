from pandas import DataFrame, read_excel, concat

from src.interface.filter_interface import AbstractFilterClass
from src.utils import before_telein_cols, after_telein_cols, cities, states, drop_unnamed, merge_categories

class FilterCityState(AbstractFilterClass):
    """Unifica a planilha com a sigla do estado e filtra cidade"""

    @classmethod
    def filter_df(cls, base_df: DataFrame, detail: dict[str, any]):

        # localiza somente as cidades que pertencem à lista
        # base_df = base_df.loc[base_df['city'].isin(cities)]

        # abrevia os estados que pertencem à lista
        # base_df = base_df.loc[base_df['state'].isin(states)]
        base_df['state'] = base_df['state'].apply(
            lambda val: states[val] if val in states else (
                val if len(str(val)) == 2 else ''
            )
        )

        return drop_unnamed(base_df)


class FilterGlossaryTypes(AbstractFilterClass):
    """Filtra dataframe pelo glossário dos tipos"""

    @classmethod
    def filter_df(cls, base_df: DataFrame, detail: dict[str, any]):

        # combina as duas colunas
        base_df['category'] = merge_categories(base_df)

        return drop_unnamed(base_df)


class FilterPlaceId(AbstractFilterClass):
    """Junta duas planilhas filtrando pelo placeid"""

    @classmethod
    def filter_df(cls, base_df: DataFrame, detail: dict[str, any]):

        # retorna caso não existam df's para concatenar
        if not "concat_with" in detail:
            return base_df

        for second_df in detail["concat_with"]:
            base_df = concat([base_df, read_excel(second_df, dtype=before_telein_cols)])

            base_df.drop_duplicates(['place_id'], keep='first', inplace=True)

        return drop_unnamed(base_df)


class FilterByColumnsOrCity(AbstractFilterClass):
    """Filtra um dataframe pegando somente determinadas colunas"""

    @classmethod
    def filter_df(cls, base_df: DataFrame, detail: dict[str, any]):

        # retorna caso não existam colunas específicas
        if not "cols" in detail and not "city" in detail:
            return base_df

        if "cols" in detail:
            base_df = base_df.loc[:, detail['cols']]

        if "city" in detail:
            base_df = base_df.loc[base_df['query_location_city'] == detail['city']]

        return drop_unnamed(base_df)
