from abc import ABC, abstractmethod
from pandas import DataFrame

class AbstractFilterClass(ABC):
    """classe para filtragem de uma estrutura"""

    @classmethod
    @abstractmethod
    def filter_df(cls, base_df: DataFrame, detail: dict[str, any]):
        """refatora uma estrutura de dados"""
