from pydantic import BaseModel

# =====================================================
# CREATE FARM REQUEST
# =====================================================


class Coordinate(BaseModel):
    lat: float
    lng: float


class CreateFarmRequest(BaseModel):

    # =================================================
    # FARMER
    # =================================================

    full_name: str

    mobile_number: str

    aadhaar_reference: str | None = None

    farmer_type: str = "individual"

    # =================================================
    # LOCATION
    # =================================================

    block_id: int

    village_id: int | None = None

    village_name: str | None = None

    # =================================================
    # FARM
    # =================================================

    farm_name: str

    ownership_type: str = "owned"

    primary_crop: str | None = None

    irrigation_type: str | None = None

    soil_type: str | None = None

    boundary_coordinates: list[Coordinate]
