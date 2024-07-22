# utils functions

# input
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# db init
load_dotenv()
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

# get closest node
def get_closest_node(coord, srid): 
    lon, lat = coord.split(',')
    connection = engine.connect()
    select_query = text(
    f"""
        SELECT CAST(id AS int) as node_id, ST_Distance(geom, ST_Transform(ST_GeomFromText('POINT({lon} {lat})', {srid}), st_srid(geom))) AS distance
        FROM data.bi_main_roads_vertices_gpr  
        ORDER BY 2 ASC
        LIMIT 1
    """
    )

    result = connection.execute(select_query)
    result_dict = []

    for row in result :
        # print(dict(row._asdict()))
        result_dict.append(dict(row._asdict()))
    
    if len(result_dict) == 0 :
        return None

    connection.close()

    print(result_dict[0])
    return result_dict[0]

def get_shortest_path(source_coord, target_coord, srid): 

    # init connection
    connection = engine.connect()

    # inputs
    origin_node = get_closest_node(source_coord, srid) 
    target_node = get_closest_node(target_coord, srid)

    if origin_node is None or target_node is None: 
        return None 
    
    origin_id = origin_node["node_id"] 
    target_id = target_node["node_id"]

    selectQuery = text(
    f"""
        SELECT ST_AsGeojson(ST_Transform(ST_Union(geom), {srid}))::json as path, sum(ST_Length(geom)) as distance FROM data.bi_main_roads
        WHERE gid IN ( 
        SELECT edge  
        FROM pgr_dijkstra( 
        'SELECT gid as id, source, target, cost FROM data.bi_main_roads',
            {int(origin_id)}, {int(target_id)}, false));
    """)
    print(selectQuery)
    
    # result
    result = connection.execute(selectQuery) 

    # dict result
    result_dict = []
    for row in result :
        # print(dict(row._asdict()))
        result_dict.append(dict(row._asdict()))

    connection.close()
    print(result_dict)

if __name__ == '__main__':
    coord = "3339096.4449698394,-348809.9290439975" 
    srid = 3857
    get_closest_node(coord, srid)

    source_coord = "3339096.4449698394,-348809.9290439975"
    target_coord = "3326255.0242179297,-397485.0323882745"
    get_shortest_path(source_coord, target_coord, srid)