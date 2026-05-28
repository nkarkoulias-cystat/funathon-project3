import folium
from folium.raster_layers import ImageOverlay
from rasterio.warp import transform_bounds
import rasterio
import numpy as np

nuts_code = "CY000"
year = "2024"
tile_filename = "6462450_1640330_1_4473.tif"

tile_url = f"https://minio.lab.sspcloud.fr/projet-funathon/2026/project3/data/images/{nuts_code}/{year}/{tile_filename}"

with rasterio.open(tile_url) as src:
    rgb_data = src.read([4, 3, 2])
    tile_crs = src.crs
    tile_bounds = src.bounds

rgb = np.transpose(rgb_data, (1, 2, 0)).astype(np.float32)
rgb = np.clip(rgb / np.percentile(rgb, 98), 0, 1)

west, south, east, north = transform_bounds(
    tile_crs, "EPSG:4326", *tile_bounds
)

center_lat = (south + north) / 2
center_lon = (west + east) / 2

m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

ImageOverlay(
    image=rgb,
    bounds=[[south, west], [north, east]],
    opacity=0.7,
).add_to(m)

m.save("map.html")
