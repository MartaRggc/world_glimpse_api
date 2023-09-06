from datetime import datetime
from pydantic import BaseModel


class CountrySchema(BaseModel):
    country_name: str
    country_id: int
    region_id: int


class CountryPoliticsSchema(BaseModel):
    government_type: str | None
    head_of_state_role: str | None
    government_basis: str | None
    stable: bool | None
    conflict_type: str | None
    conflict_casualties: str | None
    conflict_description: str | None


class CountryFootprintSchema(BaseModel):
    country_id: int
    cropland_footprint: float | None
    grazing_footprint: float | None
    forest_product_footprint: float | None
    carbon_footprint: float | None
    fish_footprint: float | None
    total_ecological_footprint_consumption: float | None
    cropland: float | None
    grazing_land: float | None
    forest_land: float | None
    fishing_ground: float | None
    built_up_land: float | None
    total_biocapacity: float | None
    ecological_deficit_or_reserve: float | None
    number_of_earths_required: float | None
    number_of_countries_required: float | None
    official_country_overshoot_day: str | None
    official_country_ecological_deficit_day: str | None


class AllCountriesFoodPrintSchema(BaseModel):
    countries: list[CountryFootprintSchema]
    median_cropland_footprint: float
    median_grazing_footprint: float | None
    median_forest_product_footprint: float | None
    median_carbon_footprint: float | None
    median_fish_footprint: float | None
    median_total_ecological_footprint_consumption: float | None
    median_cropland: float | None
    median_grazing_land: float | None
    median_forest_land: float | None
    median_fishing_ground: float | None
    median_built_up_land: float | None
    median_total_biocapacity: float | None
    median_ecological_deficit_or_reserve: float | None
    median_number_of_earths_required: float | None
    median_number_of_countries_required: float | None


class CountryNewsSchema(BaseModel):

    title: str | None = None
    author: str | None = None
    image: str | None = None
    publish_date: datetime | None = None
    sentiment: float | None = None
    source_country: str | None = None
    text: str | None = None
    url: str | None = None


class CountryGGISchema(BaseModel):
    country_id: int
    global_ggi: float | None = None
    economic_ggi: float | None = None
    political_ggi: float | None = None
    education_ggi: float | None = None
    health_ggi: float | None = None
    rank_global_ggi: int | None = None
    rank_economic_ggi: int | None = None
    rank_political_ggi: int | None = None
    rank_education_ggi: int | None = None
    rank_health_ggi: int | None = None

class AllCountriesGGISchema(BaseModel):
    countries: list[CountryGGISchema]
    median_global_ggi: float
    median_economic_ggi: float
    median_political_ggi: float
    median_education_ggi: float
    median_health_ggi: float

class CountryGeneralSchema(BaseModel):

    capital: str | None = None
    languages: list | None = None
    area: float | None = None
    population: float | None = None
    summary: str | None = None
