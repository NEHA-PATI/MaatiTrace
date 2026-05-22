import axios from "axios"

import {

  createSpatialCacheKey,

  getSpatialCache,

  setSpatialCache,

} from "../../cache/spatialCache"

const API_BASE_URL =
  "http://127.0.0.1:8001/api/v1"

// ======================================================
// FETCH H3 CELLS
// ======================================================

export async function fetchH3Cells({

  resolution,

  minLon,
  minLat,

  maxLon,
  maxLat,
}) {

  // ==================================================
  // CACHE KEY
  // ==================================================

  const cacheKey =
    createSpatialCacheKey({

      resolution,

      minLon,
      minLat,

      maxLon,
      maxLat,
    })

  // ==================================================
  // CACHE LOOKUP
  // ==================================================

  const cached =
    getSpatialCache(cacheKey)

  if (cached) {

    return cached
  }

  // ==================================================
  // API REQUEST
  // ==================================================

  console.log("API REQUEST")

  const response = await axios.get(

    `${API_BASE_URL}/h3/cells`,

    {

      params: {

        resolution,

        min_lon: minLon,
        min_lat: minLat,

        max_lon: maxLon,
        max_lat: maxLat,
      },
    }
  )

  // ==================================================
  // STORE CACHE
  // ==================================================

  setSpatialCache(

    cacheKey,

    response.data,
  )

  // ==================================================
  // RETURN
  // ==================================================

  return response.data
}
