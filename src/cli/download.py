import requests
from zipfile import ZipFile
from constants import (HF_POINTS_URL,
                       HF_POLYGON_URL, DATA_DIR)


def download_hf(geometry):
    geometry_dict ={'point': HF_POINTS_URL,
                  'polygon': HF_POLYGON_URL }
    
    url = geometry_dict.get(geometry)

    if url is None:
        raise KeyError(f'Geometry must be one of {geometry_dict.keys()}')
    r = requests.get(url)
    if r.status_code != 200:
        raise r.raise_for_status()
    with open(DATA_DIR / f'hf_{geometry}.zip', 'wb') as hf_geom:
        hf_geom.write(r.content)

def extract_hf(dest_dir, geom):
    with ZipFile(DATA_DIR / f'hf_{geom}.zip') as zipfile:
        zipfile.extractall(dest_dir)