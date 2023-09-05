from sqlalchemy import ForeignKey, Column, String, Integer, Float, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base


class Country(Base):
    __tablename__ = "countries"

    country_id = Column("country_id", Integer, primary_key=True)
    region_id = Column("region_id", Integer, ForeignKey("regions.region_id"))
    country_name = Column("country_name", String(255))

    def __init__(self, country_id, region_id, country_name):
        self.country_id = country_id
        self.region_id = region_id
        self.country_name = country_name

    def __repr__(self):
        return f"({self.country_id}, {self.region_id}) {self.country_name}"


class CountryGGI(Base):
    __tablename__ = "countries_ggi"

    country_id = Column("country_id", Integer, primary_key=True)
    score_av = Column("score_av", Float)
    score_ec = Column("score_ec", Float)
    score_pol = Column("score_pol", Float)
    score_ed = Column("score_ed", Float)
    score_h = Column("score_h", Float)

    def __init__(self, country_id, score_av, score_ec, score_pol, score_ed, score_h):
        self.country_id = country_id
        self.score_av = score_av
        self.score_ec = score_ec
        self.score_pol = score_pol
        self.score_ed = score_ed
        self.score_h = score_h


class CountryGovernment(Base):
    __tablename__ = "government_type"

    country_id = Column("country_id", Integer, primary_key=True)
    government_type = Column("government_type", String(255))
    head_of_state_role = Column("head_of_state_role", String(255))
    government_basis = Column("government_basis", String(255))

    @property
    def stable(self):
        if self.government_type.lower() == "provisional":
            return False
        return True

    def __init__(self, country_id, government_type, head_of_state_role, government_basis):
        self.country_id = country_id
        self.government_type = government_type
        self.head_of_state_role = head_of_state_role
        self.government_basis = government_basis


class CountryConflict(Base):
    __tablename__ = "ongoing_conflicts"

    country_id = Column("country_id", Integer, primary_key=True)
    conflict_type = Column("conflict_type", String(255))
    conflict_casualties = Column("conflict_casualties", String(255))
    conflict_description = Column("conflict_description", Text)

    def __init__(self, country_id, conflict_type, conflict_casualties, conflict_description):
        self.country_id = country_id
        self.conflict_type = conflict_type
        self.conflict_casualties = conflict_casualties
        self.government_basis = conflict_description


class CountryFP(Base):
    __tablename__ = "countries_footprint"

    country_id = Column("country_id", Integer, primary_key=True)
    life_expectancy = Column("life_expectancy", Float)
    income_group = Column("income_group", String(255))
    population_millions = Column("population_millions", Float)
    cropland_footprint = Column("cropland_footprint", Float)
    grazing_footprint = Column("grazing_footprint", Float)
    forest_product_footprint = Column("forest_product_footprint", Float)
    carbon_footprint = Column("carbon_footprint", Float)
    fish_footprint = Column("fish_footprint", Float)
    total_ecological_footprint_consumption = Column("total_ecological_footprint_consumption", Float)
    cropland = Column("cropland", Float)
    grazing_land = Column("grazing_land", Float)
    forest_land = Column("forest_land", Float)
    fishing_ground = Column("fishing_ground", Float)
    built_up_land = Column("built_up_land", Float)
    total_biocapacity = Column("total_biocapacity", Float)
    ecological_deficit_or_reserve = Column("ecological_deficit_or_reserve", Float)
    number_of_earths_required = Column("number_of_earths_required", Float)
    number_of_countries_required = Column("number_of_countries_required", Float)
    official_country_overshoot_day = Column("official_country_overshoot_day", String(255))
    official_country_ecological_deficit_day = Column("official_country_ecological_deficit_day", String(255))

    def __init__(self, country_id, life_expectancy, income_group,
                 population_millions, cropland_footprint, grazing_footprint,
                 forest_product_footprint, carbon_footprint, fish_footprint,
                 total_ecological_footprint_consumption, cropland, grazing_land,
                 forest_land, fishing_ground, built_up_land, total_biocapacity,
                 ecological_deficit_or_reserve, number_of_earths_required, number_of_countries_required,
                 official_country_overshoot_day, official_country_ecological_deficit_day):
        self.country_id = country_id
        self.life_expectancy = life_expectancy
        self.income_group = income_group
        self.population_millions = population_millions
        self.cropland_footprint = cropland_footprint
        self.grazing_footprint = grazing_footprint
        self.forest_product_footprint = forest_product_footprint
        self.carbon_footprint = carbon_footprint
        self.fish_footprint = fish_footprint
        self.total_ecological_footprint_consumption = total_ecological_footprint_consumption
        self.cropland = cropland
        self.grazing_land = grazing_land
        self.forest_land = forest_land
        self.fishing_ground = fishing_ground
        self.built_up_land = built_up_land
        self.total_biocapacity = total_biocapacity
        self.ecological_deficit_or_reserve = ecological_deficit_or_reserve
        self.number_of_earths_required = number_of_earths_required
        self.number_of_countries_required = number_of_countries_required
        self.official_country_overshoot_day = official_country_overshoot_day
        self.official_country_ecological_deficit_day = official_country_ecological_deficit_day


class CountryGDP(Base):
    __tablename__ = "gross_domestic_product_GDP"

    country_id = Column("country_id", Integer, primary_key=True)
    total_GDP = Column("total_GDP", Float)
    world_share = Column("world_share", Float)
    PPP_GDP_per_capita = Column("PPP_GDP_per_capita", Float)
    absolute_GDP_per_capita = Column("absolute_GDP_per_capita", Float)
    vsWorld_PPP_GDP_per_capita = Column("vsWorld_PPP_GDP_per_capita($20645)", Float)

    def __init__(self, country_id, total_GDP, world_share, PPP_GDP_per_capita,
                 absolute_GDP_per_capita, vsWorld_PPP_GDP_per_capita):
        self.country_id = country_id
        self.total_GDP = total_GDP
        self.world_share = world_share
        self.PPP_GDP_per_capita = PPP_GDP_per_capita
        self.absolute_GDP_per_capita = absolute_GDP_per_capita
        self.vsWorld_PPP_GDP_per_capita = vsWorld_PPP_GDP_per_capita


class CountryInequality(Base):
    __tablename__ = "inequality_and_poverty_countries"

    country_id = Column("country_id", Integer, primary_key=True)
    intensity_depravation_perc = Column("intensity_depravation_perc", Float)
    vulnerable_MP_pop = Column("vulnerable_MP_pop", Float)
    health_contribution = Column("health_contribution", Float)
    education_contribution = Column("education_contribution", Float)
    living_standard_contribution = Column("living_standard_contribution", Float)
    under_national_poverty_line = Column("under_national_poverty_line", Float)
    under_PPP_per_day = Column("under_PPP_per_day", Float)
    HDI = Column("HDI", Float)
    coefficient_human_inequality = Column("coefficient_human_inequality", Float)
    gini_coefficient = Column("gini_coefficient", Float)
    richest_10percent_share = Column("richest_10percent_share", Float)
    richest_1percent_share = Column("richest_1percent_share", Float)

    def __init__(self, country_id, intensity_depravation_perc, vulnerable_MP_pop,
                 health_contribution, education_contribution, living_standard_contribution,
                 under_national_poverty_line, under_PPP_per_day, HDI, coefficient_human_inequality,
                 richest_10percent_share, gini_coefficient,
                 richest_1percent_share):
        self.country_id = country_id
        self.intensity_depravation_perc = intensity_depravation_perc
        self.vulnerable_MP_pop = vulnerable_MP_pop
        self.health_contribution = health_contribution
        self.education_contribution = education_contribution
        self.living_standard_contribution = living_standard_contribution
        self.under_national_poverty_line = under_national_poverty_line
        self.under_PPP_per_day = under_PPP_per_day
        self.HDI = HDI
        self.gini_coefficient = gini_coefficient
        self.richest_10percent_share = richest_10percent_share
        self.richest_1percent_share = richest_1percent_share
