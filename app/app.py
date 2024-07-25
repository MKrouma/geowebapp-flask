# geowebapp services app

# import
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, abort, render_template
from sqlalchemy import create_engine, text
from config import config
from settings import mode
from db import read_from_db

# app initialization
app = Flask(__name__)
app.config.from_object(config[mode])
CORS(app)

# settings
db_schema = config[mode].DB_SCHEMA

# page routes
@app.route('/')
def index() : 
    return render_template('index.html')

@app.route('/viewer')
def viewer() : 
    return render_template('viewer.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# api routes
@app.route('/api/markets', methods=['GET'])
def get_markets():

    # params
    crs = 3857

    # request from geodatabase
    select_query = text(f"""
    SELECT gid, name, CAST(pop_2020 AS float) as population, categorie, ST_AsText(ST_Transform(geom, {crs})) as geometry
    FROM {db_schema}.bi_markets""")

    # json result
    result_json = jsonify(read_from_db(select_query))

    return result_json

@app.route('/api/market/<int:market_id>', methods=['GET'])
def get_market(market_id):

    # params
    crs = 3857

    # request from geodatabase
    select_query = text(f"""
    SELECT gid, name, CAST(pop_2020 AS float) as population, categorie, ST_AsText(ST_Transform(geom, {crs})) as geometry
    FROM {db_schema}.bi_markets WHERE gid={market_id}""")

    # json result
    result_json = jsonify(read_from_db(select_query))

    return result_json

@app.route('/api/service/<string:params>', methods=['GET'])
def get_service_area(params) :
    
    # inputs data
    lat, lon, size = params.split(',')
    crs_map = 3857
    crs_db = 4326

    # connect to geodatabase
    select_query = text(
        f"""
            SELECT name, ST_AsGeojson(ST_Transform(geom, {crs_map})) as geometry
            FROM {db_schema}.bi_{size} as a
            WHERE ST_Intersects(a.geom, ST_Transform(ST_GeomFromText('Point({lat} {lon})', {crs_map}), {crs_db}))
        """
    )
    # json result
    service_area = jsonify(read_from_db(select_query))

    return service_area

@app.route('/api/search/<string:params>', methods=['GET'])
def get_search_markets(params) :

    # inputs data
    lon, lat, distance_range = params.split(',')
    distance_range_km = int(distance_range)*1000
    crs_map, crs_db = 3857, 4326

    # connect to geodatabase
    select_query = text(
        f"""
            SELECT name, CAST(pop_2020 AS float) as population, ST_AsGeojson(ST_Transform(geom, {crs_map})) as geometry
            FROM {db_schema}.bi_markets as bm
            WHERE ST_DWithin(ST_GeomFromText('Point({lon} {lat})', {crs_map}), ST_Transform(bm.geom, {crs_map}), {distance_range_km})
        """
    )
    
    # json result
    search_market = jsonify(read_from_db(select_query))

    return search_market

@app.route('/api/closest/<string:params>', methods=['GET'])
def get_closest_markets(params) :

    # inputs data
    coord = params
    coord = coord.replace(',', ' ')
    crs_map = 3857
    market_type = [
        "capital_markets", "local_markets", "medium_markets", "small_markets"
    ]

    # request closest market by size
    result_dict = []
    for market in market_type : 
        select_query = text(
            f"""
                SELECT gid as id, name, categorie, ST_Distance(ST_Transform(geom, {crs_map}), ST_GeomFromText('POINT({coord})', {crs_map})) AS distance, ST_AsGeojson(ST_Transform(geom, {crs_map})) as geometry
                FROM {db_schema}.bi_markets
                WHERE categorie='{market}'
                ORDER BY distance
                LIMIT 1;
            """
        )

        result = read_from_db(select_query)[0]
        result_dict.append(result)

    # closest markets
    closest_markets = jsonify(result_dict)
    return closest_markets

if __name__ == "__main__" : 
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)