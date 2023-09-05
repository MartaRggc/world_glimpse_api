from sqlalchemy import Column, String, Integer, Float
from database import Base


class Region(Base):
    __tablename__ = "regions"

    region_id = Column("region_id", Integer, primary_key=True)
    region_name = Column("region_name", String(255))

    def __init__(self, region_id, region_name):
        self.region_id = region_id
        self.region_name = region_name

    def __repr__(self):
        return f"({self.region_id}) {self.region_name}"


class RegionGGI(Base):
    __tablename__ = "regions_ggi"

    country_id = Column("country_id", Integer, primary_key=True)
    overall_index = Column("overall_index", Float)
    economic_part_and_opp = Column("economic_part_and_opp", Float)
    educational_attainment = Column("educational_attainment", Float)
    health_survival = Column("health_survival", Float)
    political_empowerment = Column("political_empowerment", Float)

    def __init__(self, country_id, overall_index, economic_part_and_opp, educational_attainment, health_survival,
                 political_empowerment):
        self.country_id = country_id
        self.overall_index = overall_index
        self.economic_part_and_opp = economic_part_and_opp
        self.educational_attainment = educational_attainment
        self.health_survival = health_survival
        self.political_empowerment = political_empowerment


class RegionGDP(Base):
    __tablename__ = "gross_domestic_product_GDPregions"

    region_id = Column("region_id", Integer, primary_key=True)
    total_GDP = Column("total_GDP", Float)
    world_share = Column("world_share", Float)
    absolute_GDP_per_capita = Column("absolute_GDP_per_capita", Float)

    def __init__(self, region_id, total_GDP, world_share, absolute_GDP_per_capita):
        self.region_id = region_id
        self.total_GDP = total_GDP
        self.world_share = world_share
        self.absolute_GDP_per_capita = absolute_GDP_per_capita


class RegionFP(Base):
    __tablename__ = "regions_footprint"

    region_id = Column("region_id", Integer, primary_key=True)
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

    def __init__(self, region_id,
                 population_millions, cropland_footprint, grazing_footprint,
                 forest_product_footprint, carbon_footprint, fish_footprint,
                 total_ecological_footprint_consumption, cropland, grazing_land,
                 forest_land, fishing_ground, built_up_land, total_biocapacity,
                 ecological_deficit_or_reserve, number_of_earths_required):
        self.region_id = region_id
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
