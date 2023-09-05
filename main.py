import os
import statistics

import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

import openapi_client
from datetime import timedelta

from fastapi.responses import JSONResponse
from openapi_client import ApiException

from com.worldnewsapi import news_api

load_dotenv()

from models import Country, CountryGovernment, CountryConflict, CountryFP, Region
from database import session, Base, engine
from schemas import CountrySchema, CountryPoliticsSchema, RegionSchema, CountryFootprintSchema
from schemas.country_schemas import AllCountriesFoodPrintSchema, CountryNewsSchema

app = FastAPI()

# newsapi = NewsApiClient(api_key='acade396511c4284bde1a972db2ca181')

################################### NEWS API CONFIGURATION


configuration = openapi_client.Configuration(
    host="https://api.worldnewsapi.com"
)

news_api_key = os.environ.get('NEWS_API_KEY')
configuration.api_key['apiKey'] = news_api_key

with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class:

    our_newsapi = news_api.NewsApi(api_client)


###################################


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

    def median_list(feature, alldata):
        return statistics.median([getattr(i, feature) for i in alldata if getattr(i, feature) is not None])

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


@app.get("/country/{country_id}/{news_text}/news", response_model=list[CountryNewsSchema])
def get_country_news(country_id: int, news_text: str):
    """
    This endpoint will make a request to the world news api for a specific country matching its name with the news texts.
    It will return the data in a format that will be used by the API consumers defined in the CountryNewsSchema.
    """

    # Here we get the data from the world news api:
    country_name = session.query(Country).filter_by(country_id=country_id).first().country_name
    try:
        news = our_newsapi.search_news(
            text=country_name + ' ' + news_text, earliest_publish_date=str(pd.Timestamp.now() - timedelta(days=1)),
            sort='publish-time'
        )['news']
    except ApiException as exception_to_use:
        return JSONResponse(content={"message": str(exception_to_use)}, status_code=429)

    return news


# @app.get("/news_info")
# def read_item(country: Union[str, None] = None):
#     headlines = newsapi.get_top_headlines(
#         language='en',
#         country=country
#     )
#     headlines_title = [i['title'] for i in headlines['articles']]
#     headlines_content = [i['content'] for i in headlines['articles']]
#
#     return {
#         "subsec": "news_info",
#         "country": country,
#         "titles": headlines_title,
#         "content": headlines_content
#     }


#
# @app.get("/country/{country_id}/footprint", response_model=CountryFootprintSchema)
# def get_country_footprint(country_id: int):
#     """
#     This endpoint will group the different data from the country footprint in diverse dimensions.
#     It will return the data in a format that will be used by the API consumers defined in the CountryFootprintsSchema.
#     """
#
#     # We get the needed data from the table involved
#     country_footprint = session.query(CountryFP).filter_by(country_id=country_id).first()
#
#     return country_footprint

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session.commit()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
