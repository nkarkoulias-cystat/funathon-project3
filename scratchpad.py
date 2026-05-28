# %%

# example:

# import os
# import urllib.request
import rasterio
import numpy as np

tile_url = (
    "https://minio.lab.sspcloud.fr/projet-funathon/2026/"
    "project3/data/images/LU000/"
    "2024/4042000_2951690_0_637.tif"
)

with rasterio.open(tile_url) as src:
    tile_crs = src.crs
    tile_bounds = src.bounds
    tile_count = src.count
    tile_height = src.height
    tile_width = src.width
    # Read RGB bands: B4 (Red), B3 (Green), B2 (Blue)
    rgb_data = src.read([4, 3, 2])

print(f"CRS:    {tile_crs}")
print(f"Bounds: {tile_bounds}")
print(f"Shape:  {tile_count} bands x {tile_height} x {tile_width} px")

# %%

# example, conjtinued:

import matplotlib.pyplot as plt

# Transpose to (H, W, 3) and normalize for display
rgb = np.transpose(rgb_data, (1, 2, 0)).astype(np.float32)
p98 = np.percentile(rgb, 98)
rgb = np.clip(rgb / p98, 0, 1)

fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(rgb)
ax.set_title("Sentinel-2 RGB composite (B4, B3, B2) — LU000")
ax.axis("off")
plt.tight_layout()
plt.show()

# %%

# exercise 1:

import rasterio
import numpy as np
import matplotlib.pyplot as plt

tile_url = (
    "https://minio.lab.sspcloud.fr/projet-funathon/2026/"
    "project3/data/images/LU000/"
    "2024/4042000_2951690_0_637.tif"
)

# Step 1: Open the tile and read RGB bands (4, 3, 2)
with rasterio.open(tile_url) as src:
    rgb_data = src.read([4, 3, 2])  # TODO: read bands 4, 3, 2
    tile_crs = src.crs  # TODO
    tile_bounds = src.bounds  # TODO

# Step 2: Transpose to (H, W, 3) and normalize
rgb = np.transpose(rgb_data, (1, 2, 0)).astype(np.float32)   # TODO: np.transpose, then normalize with 98th percentile and clip
p98 = np.percentile(rgb, 98)
rgb = np.clip(rgb / p98, 0, 1)

# Step 3: Display
fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(rgb)  # TODO: ax.imshow(...)
ax.set_title("Sentinel-2 RGB composite")
ax.axis("off")
plt.tight_layout()
plt.show()

# %%

# exercise 2:

import rasterio
import numpy as np
import matplotlib.pyplot as plt

tile_url = (
    "https://minio.lab.sspcloud.fr/projet-funathon/2026/"
    "project3/data/images/LU000/"
    "2024/4042000_2951690_0_637.tif"
)

# Step 2a: Open the tile and print the raster profile
with rasterio.open(tile_url) as src:
    print(src.profile) # TODO: print src.profile

    # Step 2b: Read false-colour bands (NIR=8, Red=4, Green=3)
    fc_data = src.read([8, 4, 3]) # TODO: src.read([8, 4, 3])

# Step 2c: Normalize for display
fc = np.transpose(fc_data, (1, 2, 0)).astype(np.float32)
p98 = np.percentile(fc, 98)  # TODO: np.percentile(fc, 98)
fc = np.clip(fc / p98, 0, 1)   # TODO: np.clip(fc / p98, 0, 1)

# Step 2d: Display side by side with the true-colour RGB
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(rgb)
axes[0].set_title("True colour (B4, B3, B2)")
axes[0].axis("off")
axes[1].imshow(fc)  # TODO: axes[1].imshow(fc)
axes[1].set_title("False colour (B8, B4, B3)")
axes[1].axis("off")
plt.tight_layout()
plt.show()

# %%

# exercise 3:

import rasterio
import numpy as np
import matplotlib.pyplot as plt

tile_url = (
    "https://minio.lab.sspcloud.fr/projet-funathon/2026/"
    "project3/data/images/LU000/"
    "2024/4042000_2951690_0_637.tif"
)

# Step 3a: Read NIR (band 8) and Red (band 4) as float32
with rasterio.open(tile_url) as src:
    nir = src.read(8).astype(np.float32)  # TODO: src.read(8).astype(np.float32)
    red = src.read(4).astype(np.float32)  # TODO: src.read(4).astype(np.float32)

# Step 3b: Compute NDVI (handle division by zero)
ndvi = np.where(nir + red == 0, 0, (nir - red) / (nir + red))  # TODO: np.where(nir + red == 0, 0, (nir - red) / (nir + red))

# Step 3c: Display
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1) # TODO: ax.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
ax.set_title("NDVI — LU000 (2024)")
ax.axis("off")
fig.colorbar(im, ax=ax, shrink=0.8, label="NDVI")  # TODO: fig.colorbar(im, ax=ax, shrink=0.8, label="NDVI")
plt.tight_layout()
plt.show()


# %%

# exercise 4:

import requests
import geopandas as gpd
from shapely.geometry import Point

# Step 1: Geocode
response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Luxemburg", "format": "json", "limit": 1},  # TODO: city name
    headers={"User-Agent": "funathon-project3"},
)
result = response.json()[0]
lon, lat = float(result["lon"]), float(result["lat"])  # TODO: extract coordinates

# Step 2: Create GeoDataFrame and reproject
city_point = gpd.GeoDataFrame(
    {"city": ["Luxemburg"]},
    geometry=[Point(lon, lat)],
    crs="EPSG:4326",  # TODO
)
city_point = city_point.to_crs("EPSG:3035")  # TODO: target CRS

# Step 3: Load NUTS3 boundaries and spatial join
nuts_url = (
    "https://gisco-services.ec.europa.eu/distribution/v2/"
    "nuts/geojson/NUTS_RG_01M_2021_3035_LEVL_3.geojson"
)
nuts = gpd.read_file(nuts_url)
city_nuts = gpd.sjoin(city_point, nuts, predicate="within")  # TODO
# print(city_nuts.iloc)
nuts_code = city_nuts.iloc[0]["NUTS_ID"]  # TODO: column name

# Step 4: Check availability
available = [
    "AT130",
    "BE100",
    "BG411",
    "CZ010",
    "DE300",
    "DEA23",
    "EE001",
    "EL303",
    "ES300",
    "FI1B1",
    "FR101",
    "FRJ27",
    "LU000",
    "HRO41",
    "HU110",
    "ITI43",
    "LT011",
    "LV006",
    "MT001",
    "NL329",
    "PL127",
    "PT170",
    "RO321",
    "SE110",
    "SI041",
    "SK010",
]
print(f"NUTS3 code: {nuts_code}, available: {nuts_code in available}")

# Step 5: Build S3 URL
base_url = f"s3://projet-funathon/2026/project3/data/images/{nuts_code}"  # TODO
print(base_url)


# %%

#### #### #### #### ####

# exercise 11:

