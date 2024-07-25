import os
import json
from config import config
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from settings import mode


# Database connection parameters
load_dotenv()
app_config = config[mode]
db_url = app_config.DATABASE_URI
db_schema = app_config.DB_SCHEMA

# create db engine
engine = create_engine(db_url)

def get_db_connection():
    # create connection
    connection = engine.connect()
    return connection

def read_from_db(query, log=False):
    # connection
    connection = get_db_connection()

    try : 
        # read from db
        result = connection.execute(query)

        # dict result
        result_dict = []
        for row in result :
            # print(dict(row._asdict()))
            result_dict.append(dict(row._asdict()))

    except Exception as e:
        return [{"error" : str(e)}]
    
    connection.close()


    if log : 
        print("Connection : ", connection)
        print("Result dict : ", result_dict)
        print("Read from db : ", result_json)

    return result_dict

def write_to_db(query, log=False):
    # connection
    connection = get_db_connection()

    try : 
        # write to db
        result = connection.execute(query)
    
    except Exception as e:
        return [{"error" : str(e)}]
    
    connection.close()


if __name__ == "__main__" :

    # test connexion
    connection = get_db_connection()
    query = text(f"""
                SELECT gid, name, CAST(pop_2020 AS float) as population
                FROM {db_schema}.bi_markets""")
    result_json = read_from_db(query, log=True)
    