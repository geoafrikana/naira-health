import requests
from zipfile import ZipFile
import re
import geopandas as gpd
from constants import (HF_URL, DATA_DIR,
                       HF_ZIP_NAME, HF_GEOJSON_NAME, DB_PATH)
import sqlite3
from .utils import generate_foreign_key, generate_many_many

def extract():
    r = requests.get(HF_URL)
    if r.status_code != 200:
        raise r.raise_for_status()
    with open(DATA_DIR / HF_ZIP_NAME, 'wb') as hf_points:
        hf_points.write(r.content)
    
    with ZipFile(DATA_DIR / HF_ZIP_NAME) as zipfile:
        info_list = zipfile.infolist()
        for info in info_list:
            if re.search('.geojson$', info.filename, re.IGNORECASE):
                info.filename = HF_GEOJSON_NAME
                zipfile.extract(info, DATA_DIR)
            else:
                print(f'{info.filename} skipped, not a geojson')
            

def transform_load():
    gdf = gpd.read_file(DATA_DIR / HF_GEOJSON_NAME)
    gdf = gdf.drop(columns=['name:en','building', 'addr:full', 'addr:city', 'source', 'osm_id', 'osm_type','capacity:persons'])
    gdf = gdf.rename(columns={'amenity': 'facility_type',
                'healthcare': 'services',
                'healthcare:speciality': 'speciality',
                'operator:type': 'operator_type'})
    
    gdf['name'] = gdf['name'].str.lower()
    operator_lookup, df = generate_foreign_key(gdf, 'operator_type', index_name='operator_id')
    facility_lookup, df = generate_foreign_key(df, 'facility_type', index_name='facility_id')
    speciality_lookup, speciality_rel, df = generate_many_many(df, 'speciality')
    services_lookup, services_rel, df = generate_many_many(df, 'services')

    df.to_file(DB_PATH, driver='GPKG', layer='health_facility')
    conn = sqlite3.connect(DB_PATH)

    operator_lookup.to_sql(name='operator_type', con=conn, index=False, if_exists='replace')
    facility_lookup.to_sql(name='facility_type', con=conn, index=False, if_exists='replace')
    speciality_lookup.to_sql(name='speciality_type', con=conn, index=False, if_exists='replace')
    services_lookup.to_sql(name='services_type', con=conn, index=False, if_exists='replace')
    speciality_rel.to_sql(name="hf_speciality", con=conn, index=False, if_exists='replace')
    services_rel.to_sql(name="hf_services", con=conn, index=False, if_exists='replace')
    