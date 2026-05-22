function DebugPanel({

  zoom,

  resolution,

  featureCount,

  loading,
}) {

  return (

    <div
      style={{

        position: "absolute",

        top: 20,
        left: 20,

        zIndex: 1000,

        background: "white",

        padding: "14px",

        borderRadius: "12px",

        boxShadow:
          "0 2px 10px rgba(0,0,0,0.2)",

        fontFamily: "sans-serif",

        minWidth: "220px",
      }}
    >

      <h3>
        MaatiTrace Spatial Engine
      </h3>

      <p>
        <strong>Zoom:</strong>{" "}
        {zoom.toFixed(2)}
      </p>

      <p>
        <strong>
          H3 Resolution:
        </strong>{" "}
        {resolution}
      </p>

      <p>
        <strong>
          Visible Cells:
        </strong>{" "}
        {featureCount}
      </p>

      <p>
        <strong>
          Loading:
        </strong>{" "}
        {loading ? "YES" : "NO"}
      </p>

    </div>
  );
}

export default DebugPanel;