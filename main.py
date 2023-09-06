import os
import statistics

import pandas as pd
import uvicorn
import wikipedia
from dotenv import load_dotenv
from fastapi import FastAPI
from restcountries import RestCountryApiV2 as rapi

import openapi_client
from datetime import timedelta

from fastapi.responses import JSONResponse
from openapi_client import ApiException

from com.worldnewsapi import news_api
from schemas.country_schemas import AllCountriesGGISchema, CountryGGISchema, CountryGeneralSchema, \
    AllCountriesGDPSchema, CountryGDPSchema, CountryInequalitySchema, AllCountriesInequalitySchema

load_dotenv()

from models import Country, CountryGovernment, CountryConflict, CountryFP, Region, CountryGGI, CountryGDP, \
    CountryInequality
from database import session, Base, engine
from schemas import (CountrySchema, CountryPoliticsSchema, RegionSchema, CountryFootprintSchema,
                     AllCountriesFoodPrintSchema, CountryNewsSchema)


def median_list(feature, alldata):
    try:
        return statistics.median([getattr(i, feature) for i in alldata if getattr(i, feature) is not None])
    except:
        return None

app = FastAPI()


########## NEWS API CONFIG


configuration = openapi_client.Configuration(
    host="https://api.worldnewsapi.com"
)

news_api_key = os.environ.get('NEWS_API_KEY')
configuration.api_key['apiKey'] = news_api_key

with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class:

    our_newsapi = news_api.NewsApi(api_client)


###########


@app.get("/countries", response_model=list[CountrySchema])
def list_countries():
    countries = session.query(Country).all()
    return countries


@app.get("/regions", response_model=list[RegionSchema])
def list_countries():
    regions = session.query(Region).all()
    return regions


@app.get("/country/{country_id}/politics", response_model=CountryPoliticsSchema)
def get_country_politics(country_id: int):
    """
    This endpoint will group the different data from the government and the current conflicts of a country.
    It will return the data in a format that will be used by the API consumers defined in the CountryPoliticsSchema.
    """

    # Here we get the needed data from the different tables involved
    country_government = session.query(CountryGovernment).filter_by(country_id=country_id).first()
    country_conflicts = session.query(CountryConflict).filter_by(country_id=country_id).first()

    # Here we map the data to the output format
    country_politics = CountryPoliticsSchema(
        government_type=country_government.government_type,
        head_of_state_role=country_government.head_of_state_role,
        government_basis=country_government.government_basis,
        stable=country_government.stable,
        conflict_type=country_conflicts.conflict_type if country_conflicts else None,
        conflict_casualties=country_conflicts.conflict_casualties if country_conflicts else None,
        conflict_description=country_conflicts.conflict_description if country_conflicts else None,
    )
    return country_politics


@app.get("/countries_footprint", response_model=AllCountriesFoodPrintSchema)
def get_countries_footprint():
    """
    This endpoint will group the different data from the country footprint in diverse dimensions.
    It will return the data in a format that will be used by the API consumers defined in the CountryFootprintsSchema.
    """

    # We get the needed data from the table involved:
    all_country_footprint = session.query(CountryFP).all()

    # We calculate the median values of each variable:

    median_cropland_footprint = median_list('cropland_footprint', all_country_footprint)
    median_grazing_footprint = median_list('grazing_footprint', all_country_footprint)
    median_forest_product_footprint = median_list('forest_product_footprint', all_country_footprint)
    median_carbon_footprint = median_list('carbon_footprint', all_country_footprint)
    median_fish_footprint = median_list('fish_footprint', all_country_footprint)
    median_total_ecological_footprint_consumption = median_list('total_ecological_footprint_consumption',
                                                                all_country_footprint)
    median_cropland = median_list('cropland', all_country_footprint)
    median_grazing_land = median_list('grazing_land', all_country_footprint)
    median_forest_land = median_list('forest_land', all_country_footprint)
    median_fishing_ground = median_list('grazing_land', all_country_footprint)
    median_built_up_land = median_list('fishing_ground', all_country_footprint)
    median_total_biocapacity = median_list('total_biocapacity', all_country_footprint)
    median_ecological_deficit_or_reserve = median_list('ecological_deficit_or_reserve', all_country_footprint)
    median_number_of_earths_required = median_list('number_of_earths_required', all_country_footprint)
    median_number_of_countries_required = median_list('number_of_countries_required', all_country_footprint)

    # Instantiate what we need to return. First the countries list:
    countries_foot_print = AllCountriesFoodPrintSchema(
        countries=[
            CountryFootprintSchema(
                country_id=country_foot_print.country_id,
                cropland_footprint=country_foot_print.cropland_footprint,
                grazing_footprint=country_foot_print.grazing_footprint,
                forest_product_footprint=country_foot_print.forest_product_footprint,
                carbon_footprint=country_foot_print.carbon_footprint,
                fish_footprint=country_foot_print.fish_footprint,
                total_ecological_footprint_consumption=country_foot_print.total_ecological_footprint_consumption,
                cropland=country_foot_print.cropland,
                grazing_land=country_foot_print.grazing_land,
                forest_land=country_foot_print.forest_land,
                fishing_ground=country_foot_print.fishing_ground,
                built_up_land=country_foot_print.built_up_land,
                total_biocapacity=country_foot_print.total_biocapacity,
                ecological_deficit_or_reserve=country_foot_print.ecological_deficit_or_reserve,
                number_of_earths_required=country_foot_print.number_of_earths_required,
                number_of_countries_required=country_foot_print.number_of_countries_required,
                official_country_overshoot_day=country_foot_print.official_country_overshoot_day,
                official_country_ecological_deficit_day=country_foot_print.official_country_ecological_deficit_day,
            ) for country_foot_print in all_country_footprint
        ],

        # Then the median values for each variable:

        median_cropland_footprint=median_cropland_footprint,
        median_grazing_footprint=median_grazing_footprint,
        median_forest_product_footprint=median_forest_product_footprint,
        median_carbon_footprint=median_carbon_footprint,
        median_fish_footprint=median_fish_footprint,
        median_total_ecological_footprint_consumption=median_total_ecological_footprint_consumption,
        median_cropland=median_cropland,
        median_grazing_land=median_grazing_land,
        median_forest_land=median_forest_land,
        median_fishing_ground=median_fishing_ground,
        median_built_up_land=median_built_up_land,
        median_total_biocapacity=median_total_biocapacity,
        median_ecological_deficit_or_reserve=median_ecological_deficit_or_reserve,
        median_number_of_earths_required=median_number_of_earths_required,
        median_number_of_countries_required=median_number_of_countries_required
    )

    return countries_foot_print


@app.get("/country/{country_id}/news", response_model=list[CountryNewsSchema])
def get_country_news(country_id: int):
    """
    This endpoint will make a request to the world news api for a specific country matching its name with the news texts.
    It will return the data in a format that will be used by the API consumers defined in the CountryNewsSchema.
    """

    # Here we get the data from the world news api:
    country_name = session.query(Country).filter_by(country_id=country_id).first().country_name
    try:
        news = our_newsapi.search_news(
            entities=f'LOC:{country_name}', earliest_publish_date=str(pd.Timestamp.now() - timedelta(days=1)),
            sort='publish-time'
        )['news']
    except ApiException as exception_to_use:
        return JSONResponse(content={"message": str(exception_to_use)}, status_code=429)

    return news


@app.get("/countries_ggi", response_model=AllCountriesGGISchema)
def get_countries_ggi():
    """
    This endpoint will group the different data from the country footprint in diverse dimensions.
    It will return the data in a format that will be used by the API consumers defined in the CountryFootprintsSchema.
    """

    # We get the needed data from the table involved:
    all_countries_ggi = session.query(CountryGGI).all()

    # We calculate the median values of each variable:

    median_global_ggi = median_list('score_av', all_countries_ggi)
    median_economic_ggi = median_list('score_ec', all_countries_ggi)
    median_political_ggi = median_list('score_pol', all_countries_ggi)
    median_education_ggi = median_list('score_ed', all_countries_ggi)
    median_health_ggi = median_list('score_h', all_countries_ggi)

    # We prepare a function to calculate the rank of each country in each category:
    def rank_list(value_ggi, feature, alldata):
        feature_list = [getattr(i, feature) for i in alldata if getattr(i, feature) is not None]
        rank = int(sorted(feature_list, reverse=True).index(value_ggi) + 1)
        return rank

    # Instantiate what we need to return. First the countries list:
    countries_ggi = AllCountriesGGISchema(
        countries=[
            CountryGGISchema(
                country_id=i.country_id,
                global_ggi=i.score_av,
                economic_ggi=i.score_ec,
                political_ggi=i.score_pol,
                education_ggi=i.score_ed,
                health_ggi=i.score_h,

                # Now the ranks:
                rank_global_ggi=rank_list(i.score_av,'score_av', all_countries_ggi),
                rank_economic_ggi=rank_list(i.score_ec, 'score_ec', all_countries_ggi),
                rank_political_ggi=rank_list(i.score_pol, 'score_pol', all_countries_ggi),
                rank_education_ggi=rank_list(i.score_ed, 'score_ed', all_countries_ggi),
                rank_health_ggi=rank_list(i.score_h, 'score_h', all_countries_ggi)

            ) for i in all_countries_ggi
        ],

        # Now the median values for each field:

        median_global_ggi=median_global_ggi,
        median_economic_ggi=median_economic_ggi,
        median_political_ggi=median_political_ggi,
        median_education_ggi=median_education_ggi,
        median_health_ggi=median_health_ggi,
    )

    return countries_ggi

# @app.get("/country/{country_id}/general", response_model=CountryGeneralSchema)
# def get_country_general(country_id: int):
#     """
#     This endpoint will make a request to the world news api for a specific country matching its name with the news texts.
#     It will return the data in a format that will be used by the API consumers defined in the CountryNewsSchema.
#     """
#
#     # We identify the country name:
#     country_name = session.query(Country).filter_by(country_id=country_id).first().country_name
#
#     # We make a request to the restcountries api to get some general info:
#     rest_country = rapi.get_countries_by_name(country_name)[0]
#
#     # Now we search for a brief summary of the country in wikipedia through its own api:

#
#     adequate_title = wikipedia.search(wrap(country_name))[0]
#     wiki_country = wikipedia.summary(adequate_title)
#
#     general_info = CountryGeneralSchema(
#         capital=rest_country.capital,
#         languages=rest_country.languages,
#         area=rest_country.area,
#         population=rest_country.population,
#         summary=wiki_country,
#     )
#
#     return general_info


@app.get("/country/{country_id}/general", response_model=CountryGeneralSchema)
def get_country_general(country_id: int):
    """
    This endpoint will make a request to the world news api for a specific country matching its name with the news texts.
    It will return the data in a format that will be used by the API consumers defined in the CountryNewsSchema.
    """
    def wrap(s): # Adequate format for wikipedia API
        return(f"+{s}+")

    # We identify the country name:
    country_name = session.query(Country).filter_by(country_id=country_id).first().country_name
    # We make a request to the restcountries api to get some general info:
    rest_country = rapi.get_countries_by_name(country_name)[0]

    # Now we search for a brief summary of the country in wikipedia through its own api:
    try:
        adequate_title = wikipedia.search(wrap(country_name))[0]
        wiki_country = wikipedia.summary(adequate_title)
    except:
        wiki_country = None

    general_info = CountryGeneralSchema(
        capital=rest_country.capital,
        languages=rest_country.languages,
        area=rest_country.area,
        population=rest_country.population,
        summary=wiki_country,
    )

    return general_info


@app.get("/countries_gdp", response_model=AllCountriesGDPSchema)
def get_countries_gdp():
    """
    This endpoint will group the different data from the country footprint in diverse dimensions.
    It will return the data in a format that will be used by the API consumers defined in the CountryFootprintsSchema.
    """

    # We get the needed data from the table involved:
    all_countries_gdp = session.query(CountryGDP).all()

    # We calculate the median values of each variable:

    median_total_gdp = median_list('total_GDP', all_countries_gdp)
    median_world_share = median_list('world_share', all_countries_gdp)
    median_ppp_gdp_capita = median_list('PPP_GDP_per_capita', all_countries_gdp)
    median_gdp_capita = median_list('absolute_GDP_per_capita', all_countries_gdp)
    median_vs_world = median_list('vsWorld_PPP_GDP_per_capita', all_countries_gdp)

    # Instantiate what we need to return. First the countries list:
    countries_gdp = AllCountriesGDPSchema(
        countries=[
            CountryGDPSchema(
                country_id=i.country_id,
                total_gdp=i.total_GDP,
                world_share=i.world_share,
                ppp_gdp_capita=i.PPP_GDP_per_capita,
                gdp_capita=i.absolute_GDP_per_capita,
                vs_world=i.vsWorld_PPP_GDP_per_capita

            ) for i in all_countries_gdp
        ],

        # Then the median values for each variable:

        median_total_gdp=median_total_gdp,
        median_world_share=median_world_share,
        median_ppp_gdp_capita=median_ppp_gdp_capita,
        median_gdp_capita=median_gdp_capita,
        median_vs_world=median_vs_world
    )

    return countries_gdp


@app.get("/countries_inequality", response_model=AllCountriesInequalitySchema)
def get_countries_inequality():
    """
    This endpoint will group the different data from the country footprint in diverse dimensions.
    It will return the data in a format that will be used by the API consumers defined in the CountryFootprintsSchema.
    """

    # We get the needed data from the table involved:
    all_countries_inequality = session.query(CountryInequality).all()

    # We calculate the median values of each variable:

    median_HDI = median_list('HDI', all_countries_inequality)
    median_coefficient_human_inequality = median_list('coefficient_human_inequality', all_countries_inequality)
    median_richest_10_percent_share = median_list('richest_10percent_share', all_countries_inequality)
    median_richest_1_percent_share = median_list('richest_1percent_share', all_countries_inequality)
    median_gini_coefficient = median_list('gini_coefficient', all_countries_inequality)

    # Instantiate what we need to return. First the countries list:
    countries_ineq = AllCountriesInequalitySchema(
        countries=[
            CountryInequalitySchema(
                country_id=i.country_id,
                intensity_depravation_perc=i.intensity_depravation_perc,
                vulnerable_MP_pop=i.vulnerable_MP_pop,
                health_contribution=i.health_contribution,
                education_contribution=i.education_contribution,
                living_standard_contribution=i.living_standard_contribution,
                under_national_poverty_line=i.under_national_poverty_line,
                under_PPP=i.under_PPP_per_day,
                HDI=i.HDI,
                coefficient_human_inequality=i.coefficient_human_inequality,
                richest_10_percent_share=i.richest_10percent_share,
                richest_1_percent_share=i.richest_1percent_share,
                gini_coefficient=i.gini_coefficient,

            ) for i in all_countries_inequality
        ],

        # Then the median values for each variable:

        median_HDI=median_HDI,
        median_coefficient_human_inequality=median_coefficient_human_inequality,
        median_richest_10_percent_share=median_richest_10_percent_share,
        median_richest_1_percent_share=median_richest_1_percent_share,
        median_gini_coefficient=median_gini_coefficient
    )

    return countries_ineq



if __name__ == "__main__":
    load_dotenv()
    Base.metadata.create_all(bind=engine)
    session.commit()
    uvicorn.run("main:app", host=os.environ.get('API_HOST'), port=int(os.environ.get('API_PORT')), reload=True)
