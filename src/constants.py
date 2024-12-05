from pathlib import Path

BASE_DIR = Path(__name__).absolute().parent
DATA_DIR = BASE_DIR / 'data'

# Source https://data.humdata.org/dataset/hotosm_nga_health_facilities
HF_POINTS_URL = "https://s3.dualstack.us-east-1.amazonaws.com/production-raw-data-api/ISO3/NGA/health_facilities/points/hotosm_nga_health_facilities_points_geojson.zip"
HF_POLYGON_URL = "https://s3.dualstack.us-east-1.amazonaws.com/production-raw-data-api/ISO3/NGA/health_facilities/polygons/hotosm_nga_health_facilities_polygons_geojson.zip"