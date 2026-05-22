// ======================================================
// SPATIAL RESPONSE CACHE
// ======================================================

const spatialCache = new Map()

// ======================================================
// CACHE TTL
// ======================================================

const CACHE_TTL_MS = 1000 * 60 * 5

// ======================================================
// VIEWPORT QUANTIZATION
// ======================================================

function quantize(value) {

    // aggressive rounding

    return Number(value.toFixed(1))
}

// ======================================================
// CREATE CACHE KEY
// ======================================================

export function createSpatialCacheKey({

    resolution,

    minLon,
    minLat,

    maxLon,
    maxLat,
}) {

    return [

        resolution,

        quantize(minLon),
        quantize(minLat),

        quantize(maxLon),
        quantize(maxLat),

    ].join("_")
}

// ======================================================
// GET CACHE
// ======================================================

export function getSpatialCache(key) {

    const cached = spatialCache.get(key)

    if (!cached) {

        return null
    }

    const now = Date.now()

    const isExpired = (

        now - cached.timestamp

    ) > CACHE_TTL_MS

    if (isExpired) {

        spatialCache.delete(key)

        return null
    }

    console.log("CACHE HIT")

    return cached.data
}

// ======================================================
// SET CACHE
// ======================================================

export function setSpatialCache(

    key,
    data,
) {

    spatialCache.set(

        key,

        {

            timestamp: Date.now(),

            data,
        },
    )

    console.log("CACHE SET")
}

// ======================================================
// CLEAR CACHE
// ======================================================

export function clearSpatialCache() {

    spatialCache.clear()

    console.log("CACHE CLEARED")
}