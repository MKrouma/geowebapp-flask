import os
import geopandas as gpd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement

# Database connection parameters
load_dotenv()
neon_host = os.getenv('NEON_HOST')
neon_username = os.getenv('NEON_USERNAME')
neon_password = os.getenv('NEON_PASSWORD')
neon_dbname = os.getenv('NEON_DATABASE')

# Shapefile path
shapefile_path_list = [
    "./data/bi_capital_areas.shp"
]
shapefile_path = shapefile_path_list[0]
table_name = shapefile_path.split("/")[-1].split(".")[0]
schema_name = "data"
full_table_name = f"{schema_name}.{table_name}"

# Create a connection string
connection_string = f"postgresql+psycopg2://{neon_username}:{neon_password}@{neon_host}/{neon_dbname}?sslmode=require"

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Read the shapefile using geopandas
gdf = gpd.read_file(shapefile_path)

# Convert the geometries to WKT format
gdf['geom'] = gdf['geometry'].apply(lambda geom: WKTElement(geom.wkt, srid=4326))
gdf = gdf.drop('geometry', axis=1)

print("Geodatabase", gdf)

# Define the table schema
gdf.to_sql(table_name, engine, if_exists='replace', index=False, 
           dtype={'geom': Geometry('POLYGON', srid=4326)})

print("Shapefile data has been successfully inserted into the database.")
