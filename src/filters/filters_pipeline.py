from typing import Tuple
from pandas import DataFrame

from .filter_interface import AbstractFilterClass

class FiltersPipeline():
    """Representa uma sequência de filtros"""

    def __init__(self, *filters: Tuple[AbstractFilterClass]):
        self.filters = filters

    def __call__(self, base_df: DataFrame, detail: dict[str, any]) -> DataFrame:
        for f in self.filters:
            base_df = f.filter_df(base_df, detail)

        return base_df
