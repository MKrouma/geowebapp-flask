# geowebapp services app

# import
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, abort, render_template
from sqlalchemy import create_engine, text
from config import config

# app initialization
app = Flask(__name__)
app_config = config['development']
app.config.from_object(app_config)
app_config.init_app(app)
CORS(app)

# settings
db_url = app_config.DATABASE_URI
db_schema = app_config.DB_SCHEMA

print("db_url : ", db_url)
engine = create_engine(db_url)

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
    
    # create connection
    connection = engine.connect()

    # inputs
    crs = 3857

    # request from geodatabase
    select_query = text(f"""
    SELECT gid, name, CAST(pop_2020 AS float) as population, categorie, ST_AsText(ST_Transform(geom, {crs})) as geometry
    FROM {db_schema}.bi_markets""")

    result = connection.execute(select_query)

    # dict result
    result_dict = []
    for row in result :
        # print(dict(row._asdict()))
        result_dict.append(dict(row._asdict()))

    connection.close()

    # json result
    result_json = json.dumps(result_dict)

    return result_json

@app.route('/api/market/<int:market_id>', methods=['GET'])
def get_market(market_id):

    # market_id = int(market_id)
    
    # create connection
    connection = engine.connect()

    # inputs
    crs = 3857

    # request from geodatabase
    select_query = text(f"""
    SELECT gid, name, CAST(pop_2020 AS float) as population, categorie, ST_AsText(ST_Transform(geom, {crs})) as geometry
    FROM {db_schema}.bi_markets WHERE gid={market_id}""")

    result = connection.execute(select_query)
    row = result.fetchone()

    # wrong id
    if row is None:
        abort(404)  # Not Found

    connection.close()

    # json result
    result_json = jsonify(dict(row._mapping))

    return result_json

@app.route('/api/service/<string:params>', methods=['GET'])
def get_service_area(params) :
    
    # inputs data
    lat, lon, size = params.split(',')
    crs_map = 3857
    crs_db = 4326

    # connect to geodatabase
    connection = engine.connect()
    select_query = text(
        f"""
            SELECT name, ST_AsGeojson(ST_Transform(geom, {crs_map})) as geometry
            FROM {db_schema}.bi_{size} as a
            WHERE ST_Intersects(a.geom, ST_Transform(ST_GeomFromText('Point({lat} {lon})', {crs_map}), {crs_db}))
        """
    )
    result = connection.execute(select_query)

    # dict result
    result_dict = []
    for row in result :
        # print(dict(row._asdict()))
        result_dict.append(dict(row._asdict()))

    connection.close()

    # json result
    service_area = jsonify(result_dict)

    return service_area

@app.route('/api/search/<string:params>', methods=['GET'])
def get_search_markets(params) :

    # inputs data
    lon, lat, distance_range = params.split(',')
    distance_range_km = int(distance_range)*1000
    crs_map, crs_db = 3857, 4326

    # connect to geodatabase
    connection = engine.connect()
    select_query = text(
        f"""
            SELECT name, CAST(pop_2020 AS float) as population, ST_AsGeojson(ST_Transform(geom, {crs_map})) as geometry
            FROM {db_schema}.bi_markets as bm
            WHERE ST_DWithin(ST_GeomFromText('Point({lon} {lat})', {crs_map}), ST_Transform(bm.geom, {crs_map}), {distance_range_km})
        """
    )
    result = connection.execute(select_query)

    # dict result
    result_dict = []
    for row in result :
        # print(dict(row._asdict()))
        result_dict.append(dict(row._asdict()))

    connection.close()

    # json result
    search_market = jsonify(result_dict)

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

    # connection
    connection = engine.connect()

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

        result = connection.execute(select_query)

        for row in result :
            result_dict.append(dict(row._asdict()))

    connection.close()

    print(result_dict)
    print(len(result_dict))

    # closest markets
    closest_markets = jsonify(result_dict)
    return closest_markets

if __name__ == "__main__" : 
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)