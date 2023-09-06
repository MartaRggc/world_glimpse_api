import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

from database import session
from models import *

def convert(val):
    if isinstance(val, np.generic):
        return val.item()
    else:
        return val


if __name__ == "__main__":
    cc = pd.read_csv('clean_data/countries.csv').replace({np.NaN: None})
    rr = pd.read_csv('clean_data/regions.csv').replace({np.NaN: None})
    countries_ggi = pd.read_csv('clean_data/countries_ggi.csv').replace({np.NaN: None})
    government_type = pd.read_csv('clean_data/government_type.csv').replace({np.NaN: None})
    ongoing_conflicts = pd.read_csv('clean_data/ongoing_conflicts.csv').replace({np.NaN: None})
    ongoing_conflicts.conflict_description = [bytes(i,'utf-8') for i in ongoing_conflicts.conflict_description]
    regions_ggi = pd.read_csv('clean_data/regions_ggi.csv').replace({np.NaN: None})
    countries_footprint = pd.read_csv('clean_data/countries_footprint.csv').replace({np.NaN: None})
    gross_domestic_product_GDP = pd.read_csv('clean_data/gross_domestic_product_GDP.csv').replace({np.NaN: None})
    gross_domestic_product_GDPregions = pd.read_csv('clean_data/gross_domestic_product_GDPregions.csv').replace(
        {np.NaN: None})
    inequality_and_poverty_countries = pd.read_csv('clean_data/inequality_and_poverty_countries.csv').replace(
        {np.NaN: None})
    regions_footprint = pd.read_csv('clean_data/regions_footprint.csv').replace({np.NaN: None})

    # for i in range(rr.shape[0]):
    #     a = list(rr.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(Region(*a))
    #
    # for i in range(countries_ggi.shape[0]):
    #     a = list(countries_ggi.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryGGI(*a))
    #
    # for i in range(government_type.shape[0]):
    #     a = list(government_type.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryGovernment(*a))
    #
    # for i in range(regions_ggi.shape[0]):
    #     a = list(regions_ggi.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(RegionGGI(*a))
    #
    # for i in range(countries_footprint.shape[0]):
    #     a = list(countries_footprint.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryFP(*a))
    #
    # for i in range(gross_domestic_product_GDP.shape[0]):
    #     a = list(gross_domestic_product_GDP.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryGDP(*a))
    #
    # for i in range(gross_domestic_product_GDPregions.shape[0]):
    #     a = list(gross_domestic_product_GDPregions.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(RegionGDP(*a))
    #
    # for i in range(inequality_and_poverty_countries.shape[0]):
    #     a = list(inequality_and_poverty_countries.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryInequality(*a))
    #
    # for i in range(regions_footprint.shape[0]):
    #     a = list(regions_footprint.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(RegionFP(*a))

    # for i in range(ongoing_conflicts.shape[0]):
    #     a = list(ongoing_conflicts.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(CountryConflict(*a))

    # for i in range(cc.shape[0]):
    #     a = list(cc.iloc[i, :])
    #     a = [convert(i) for i in a]
    #     session.add(Country(*a))

    session.commit()