import {
  Layer,
  Source,
} from "react-map-gl/maplibre";


function H3Layer({ geojson }) {

  if (!geojson) return null;

  return (

    <Source
      id="h3-cells"
      type="geojson"
      data={geojson}
    >

      <Layer
        id="h3-fill"
        type="fill"
        paint={{

          "fill-color":
            "#00bcd4",

          "fill-opacity":
            0.35,
        }}
      />

      <Layer
        id="h3-outline"
        type="line"
        paint={{

          "line-color":
            "#000",

          "line-width":
            1,
        }}
      />

    </Source>
  );
}

export default H3Layer;