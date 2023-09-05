from pydantic import BaseModel


class RegionSchema(BaseModel):
    region_name: str
    region_id: int