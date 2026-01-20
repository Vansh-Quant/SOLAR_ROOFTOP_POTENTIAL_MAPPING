import geopandas as gpd
import math
import json

# Load buildings
buildings = gpd.read_file("../data/buildings.geojson")

# Clean data
buildings = buildings.dropna(subset=["roof_type", "geometry"])
buildings = buildings[buildings.geometry.is_valid]

# Convert to metric CRS
buildings = buildings.to_crs(epsg=32643)

# Area
buildings["area_m2"] = buildings.geometry.area

# Orientation
def get_orientation(polygon):
    coords = list(polygon.exterior.coords)
    longest = 0
    angle = 0
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist > longest:
            longest = dist
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if -45 <= angle <= 45:
        return "East"
    elif 45 < angle <= 135:
        return "North"
    elif angle > 135 or angle < -135:
        return "West"
    else:
        return "South"

buildings["orientation"] = buildings.geometry.apply(get_orientation).astype(str)
print(buildings[["orientation"]].head())


# Scoring
def area_score(a): return 1.0 if a > 80 else 0.7 if a > 40 else 0.3
def roof_score(r): return {"RCC": 1.0, "Tin": 0.7, "Tiled": 0.5}.get(r, 0.4)
def orient_score(o): return {"South": 1.0, "East": 0.7, "West": 0.7, "North": 0.4}.get(o, 0.5)

buildings["score"] = (
    0.4 * buildings["area_m2"].apply(area_score) +
    0.3 * buildings["roof_type"].apply(roof_score) +
    0.3 * buildings["orientation"].apply(orient_score)
)

buildings["suitability"] = buildings["score"].apply(
    lambda s: "Excellent" if s > 0.75 else "Good" if s > 0.5 else "Poor"
)

# Energy calculation
UTIL = 0.7
HOURS = 4.5
buildings["capacity_kw"] = buildings["area_m2"] * 0.15 * UTIL
buildings["annual_kwh"] = buildings["capacity_kw"] * HOURS * 365

# Summary
summary = {
    "total_buildings": len(buildings),
    "excellent": int((buildings["suitability"] == "Excellent").sum()),
    "good": int((buildings["suitability"] == "Good").sum()),
    "poor": int((buildings["suitability"] == "Poor").sum()),
    "total_kw": round(buildings["capacity_kw"].sum(), 2),
    "total_kwh": round(buildings["annual_kwh"].sum(), 0)
}

with open("../output/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Back to lat/lon
buildings = buildings.to_crs(epsg=4326)

buildings.to_file("../output/solar_potential.geojson", driver="GeoJSON")
print("DONE")
