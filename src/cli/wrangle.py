import glob
import pandas as pd
import geopandas as gpd
from constants import DATA_DIR
import sqlite3

def clean_data():
    geojsons = glob.glob(str(DATA_DIR / '*.geojson'))
    gdf = [gpd.read_file(geojson) for geojson in geojsons if 'point' in geojson][0]
    splitted = gdf['healthcare:speciality'].str.split(';', expand=True).reset_index(names=['hf_id'])
    relationship_df = splitted.melt(id_vars='hf_id', 
                                    value_name='speciality').dropna()
    relationship_df = relationship_df[['hf_id',
                                       'speciality']].reset_index(drop=True)
    speciality_df = pd.DataFrame({
        'speciality': relationship_df['speciality'].unique()
        }).reset_index(names='speciality_id')
    relationship_df = relationship_df.join(speciality_df.set_index('speciality'), 'speciality').drop(['speciality'], axis=1)
    hf = gdf.drop(['name:en', 'building','addr:full',
          'addr:city', 'source', 'osm_id',
          'osm_type', 'capacity:persons',
          'healthcare:speciality'
          ], axis=1)
    hf.to_file(
    'hf.gpkg',
    driver='GPKG',
    layer='health_facility')
    conn = sqlite3.connect('hf.gpkg')
    relationship_df.to_sql(name="facility_speciality",
                       con=conn,
                       index=False,
                       if_exists='replace')
    speciality_df.to_sql(name="speciality",
                       con=conn,
                       index=False,
                     if_exists='replace')


