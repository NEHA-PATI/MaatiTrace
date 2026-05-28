from pydantic import BaseModel

# =====================================================
# FARM H3 CELL RESPONSE
# =====================================================


class FarmH3CellResponse(BaseModel):

    h3_index: str

    resolution: int

    coverage_ratio: float


# =====================================================
# FARM SPATIAL RESPONSE
# =====================================================


class FarmSpatialResponse(BaseModel):

    farm_id: int

    total_cells: int

    cells: list[FarmH3CellResponse]
