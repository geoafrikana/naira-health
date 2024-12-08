from pathlib import Path

BASE_DIR = Path(__name__).absolute().parent
DATA_DIR = BASE_DIR / 'data'
DB_PATH = BASE_DIR / "src/dashboard/naira_health.gpkg"

HF_URL = "https://s3.dualstack.us-east-1.amazonaws.com/production-raw-data-api/ISO3/NGA/health_facilities/points/hotosm_nga_health_facilities_points_geojson.zip"
HF_ZIP_NAME = 'hf_points.zip'
HF_GEOJSON_NAME = 'hf_points.geojson'
