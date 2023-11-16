from src.filters_pipeline import FiltersPipeline

from src.filters import (
    FilterCityState,
    FilterGlossaryTypes,
    FilterPlaceId,
    FilterByColumnsOrCity
)


extraction_composite = FiltersPipeline(FilterPlaceId, FilterCityState, FilterGlossaryTypes)

after_telein_composite = FiltersPipeline(FilterByColumnsOrCity)
