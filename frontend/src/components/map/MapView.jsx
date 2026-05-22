// import {
//   useRef,
//   useState,
// } from "react";

// import Map from "react-map-gl/maplibre";

// import "maplibre-gl/dist/maplibre-gl.css";

// import {

//   INITIAL_VIEW_STATE,

//   MAP_STYLE,

// } from "../../constants/mapConfig";

// import {
//   getResolutionFromZoom,
// } from "../../utils/spatial/h3Resolution";

// import {
//   fetchH3Cells,
// } from "../../services/api/spatialApi";

// import H3Layer from "./H3Layer";

// import DebugPanel from "./DebugPanel";


// // =====================================================
// // MAP VIEW
// // =====================================================

// function MapView() {

//   // =================================================
//   // MAP REFERENCE
//   // =================================================

//   const mapRef = useRef();


//   // =================================================
//   // REQUEST CACHE
//   // =================================================

//   const lastRequestKey =
//     useRef(null);


//   // =================================================
//   // GEOJSON STATE
//   // =================================================

//   const [geojson, setGeojson] =
//     useState(null);


//   // =================================================
//   // CURRENT ZOOM
//   // =================================================

//   const [currentZoom, setCurrentZoom] =
//     useState(INITIAL_VIEW_STATE.zoom);


//   // =================================================
//   // LOADING STATE
//   // =================================================

//   const [loading, setLoading] =
//     useState(false);


//   // =================================================
//   // ACTIVE RESOLUTION
//   // =================================================

//   const [
//     activeResolution,
//     setActiveResolution,
//   ] = useState(
//     getResolutionFromZoom(
//       INITIAL_VIEW_STATE.zoom
//     )
//   );


//   // =================================================
//   // FEATURE COUNT
//   // =================================================

//   const [
//     featureCount,
//     setFeatureCount,
//   ] = useState(0);


//   // =================================================
//   // LOAD H3 CELLS
//   // =================================================

//   const loadCells =
//     async (viewport) => {

//       const map =
//         mapRef.current?.getMap();

//       if (!map) return;


//       // =============================================
//       // EXTRACT VIEWPORT BOUNDS
//       // =============================================

//       const bounds =
//         map.getBounds();

//       const min_lon =
//         bounds.getWest();

//       const min_lat =
//         bounds.getSouth();

//       const max_lon =
//         bounds.getEast();

//       const max_lat =
//         bounds.getNorth();


//       // =============================================
//       // DETERMINE RESOLUTION
//       // =============================================

//       const resolution =
//         getResolutionFromZoom(
//           viewport.zoom
//         );

//       setActiveResolution(
//         resolution
//       );


//       // =============================================
//       // CREATE REQUEST HASH
//       // =============================================

//       const requestKey =
//         JSON.stringify({

//           resolution,

//           min_lon:
//             min_lon.toFixed(2),

//           min_lat:
//             min_lat.toFixed(2),

//           max_lon:
//             max_lon.toFixed(2),

//           max_lat:
//             max_lat.toFixed(2),
//         });


//       // =============================================
//       // PREVENT DUPLICATE REQUESTS
//       // =============================================

//       if (
//         requestKey ===
//         lastRequestKey.current
//       ) {

//         console.log(
//           "SKIPPING DUPLICATE REQUEST"
//         );

//         return;
//       }

//       lastRequestKey.current =
//         requestKey;


//       // =============================================
//       // FETCH DATA
//       // =============================================

//       try {

//         setLoading(true);

//         console.log(
//           "FETCHING H3 CELLS..."
//         );

//         const start =
//           performance.now();

//         const data =
//           await fetchH3Cells({

//             resolution,

//             minLon: min_lon,
//             minLat: min_lat,

//             maxLon: max_lon,
//             maxLat: max_lat,
//           });

//         const end =
//           performance.now();

//         console.log(
//           `FETCH TIME: ${(end - start).toFixed(2)
//           } ms`
//         );

//         setGeojson(data);

//         setFeatureCount(
//           data?.features?.length || 0
//         );

//       } catch (error) {

//         console.error(
//           "FAILED TO FETCH:",
//           error
//         );

//       } finally {

//         setLoading(false);
//       }
//     };

//   // =================================================
//   // RENDER
//   // =================================================

//   return (

//     <div
//       style={{
//         width: "100vw",
//         height: "100vh",
//       }}
//     >

//       {/* ========================================= */}
//       {/* DEBUG PANEL                               */}
//       {/* ========================================= */}

//       <DebugPanel

//         zoom={currentZoom}

//         resolution={
//           activeResolution
//         }

//         featureCount={
//           featureCount
//         }

//         loading={loading}
//       />


//       {/* ========================================= */}
//       {/* MAP                                       */}
//       {/* ========================================= */}

//       <Map

//         ref={mapRef}

//         initialViewState={
//           INITIAL_VIEW_STATE
//         }

//         onLoad={() => {

//           loadCells(
//             INITIAL_VIEW_STATE
//           );
//         }}

//         onMoveEnd={(evt) => {

//           setCurrentZoom(
//             evt.viewState.zoom
//           );

//           loadCells(
//             evt.viewState
//           );
//         }}

//         style={{
//           width: "100%",
//           height: "100%",
//         }}

//         mapStyle={MAP_STYLE}
//       >

//         {/* ===================================== */}
//         {/* H3 LAYER                              */}
//         {/* ===================================== */}

//         <H3Layer
//           geojson={geojson}
//         />

//       </Map>

//     </div>
//   );
// }

// export default MapView;






import {
  useRef,
} from "react";

import Map from "react-map-gl/maplibre";

import "maplibre-gl/dist/maplibre-gl.css";

import {

  INITIAL_VIEW_STATE,

  MAP_STYLE,

} from "../../constants/mapConfig";


// =====================================================
// MAP VIEW
// =====================================================

function MapView() {

  // =================================================
  // MAP REFERENCE
  // =================================================

  const mapRef = useRef(null);


  // =================================================
  // MAP LOAD
  // =================================================

  const handleMapLoad = () => {

    console.log(
      "MAP LOADED"
    );

    const map =
      mapRef.current.getMap();

    // ===============================================
    // VECTOR TILE SOURCE
    // ===============================================

    map.addSource(
      "h3_tiles",
      {

        type: "vector",

        tiles: [

          "http://127.0.0.1:8001/api/v1/tiles/{z}/{x}/{y}.mvt",

        ],

        minzoom: 0,

        maxzoom: 14,
      }
    );

    console.log(
      "VECTOR TILE SOURCE ADDED"
    );

    // ===============================================
    // H3 FILL LAYER
    // ===============================================

    map.addLayer({

      id: "h3-fill",

      type: "fill",

      source: "h3_tiles",

      "source-layer":
        "h3_cells",

      paint: {

        "fill-color":
          "#00FF88",

        "fill-opacity":
          0.25,
      },
    });

    // ===============================================
    // H3 BORDER LAYER
    // ===============================================

    map.addLayer({

      id: "h3-line",

      type: "line",

      source: "h3_tiles",

      "source-layer":
        "h3_cells",

      paint: {

        "line-color":
          "#00FF88",

        "line-width":
          1,
      },
    });

    console.log(
      "VECTOR TILE LAYERS ADDED"
    );
  };

  // =================================================
  // RENDER
  // =================================================

  return (

    <div

      style={{

        width: "100vw",

        height: "100vh",
      }}
    >

      <Map

        ref={mapRef}

        initialViewState={
          INITIAL_VIEW_STATE
        }

        onLoad={handleMapLoad}

        style={{

          width: "100%",

          height: "100%",
        }}

        mapStyle={MAP_STYLE}
      />

    </div>
  );
}

export default MapView;