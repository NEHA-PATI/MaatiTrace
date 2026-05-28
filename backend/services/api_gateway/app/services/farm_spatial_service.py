import h3

from h3 import LatLngPoly

from geoalchemy2.shape import to_shape

from services.api_gateway.app.repositories.farm_h3_repository import (
    FarmH3Repository,
)

# =====================================================
# FARM SPATIAL SERVICE
# =====================================================


class FarmSpatialService:

    H3_RESOLUTION = 12
    INSERT_CHUNK_SIZE = 10_000

    @staticmethod
    async def generate_farm_h3_cells(
        db,
        farm,
        boundary,
    ):

        # =============================================
        # LOAD SHAPELY POLYGON
        # =============================================

        polygon = to_shape(boundary.boundary)

        # =============================================
        # CONVERT TO H3 LAT/LNG FORMAT
        # =============================================
        polygon_coords = [(lat, lng) for lng, lat in polygon.exterior.coords]

        h3_polygon = LatLngPoly(polygon_coords)

        # =============================================
        # GENERATE H3 CELLS
        # =============================================

        print("\nPOLYGON COORDS:")
        print(polygon_coords)

        print("\nH3 RESOLUTION:")
        print(FarmSpatialService.H3_RESOLUTION)

        h3_indexes = h3.polygon_to_cells(
            h3_polygon,
            FarmSpatialService.H3_RESOLUTION,
        )

        print("\nTOTAL H3 INDEXES:")
        print(len(h3_indexes))

        # =============================================
        # DELETE OLD LINKS
        # =============================================

        await FarmH3Repository.delete_farm_h3_cells(
            db,
            farm.id,
        )

        # =============================================
        # BUILD RECORDS
        # =============================================

        total_records = 0
        chunk = []

        for h3_index in h3_indexes:

            chunk.append(
                {
                    "farm_id": farm.id,
                    "h3_index": h3_index,
                    "resolution": FarmSpatialService.H3_RESOLUTION,
                    "coverage_ratio": 1.0,
                }
            )

            if len(chunk) >= FarmSpatialService.INSERT_CHUNK_SIZE:

                await FarmH3Repository.bulk_insert(
                    db,
                    chunk,
                )

                total_records += len(chunk)

                chunk = []

        # =============================================
        # STORE
        # =============================================

        if chunk:

            await FarmH3Repository.bulk_insert(
                db,
                chunk,
            )

            total_records += len(chunk)

        return total_records
