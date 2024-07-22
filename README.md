# geowebapp-flask
Burundi Market Analytics is a project from the Geowebapp wourse at Geoversity (ITC). We'll change the architecture and do the backend with flask, a python framework.

# Basics commands
```
python -V
python -m venv venv
pip install -r requirements.txt
pip freeze > requirements.txt
```

# Run your wsgi server
```
run_flask.bat
sh run_flask.sh
```

# Populate neon database
```
shp2pgsql -I -s 4326 'C:\Users\Mamadou\Documents\GEODAFTAR\geowebapp-flask\data\bi_capital_areas.shp' data.bi_capital_areas | psql -h ep-solitary-tree-a2v2l0gq.eu-central-1.aws.neon.tech -U db_burundi_owner -d db_burundi

ogr2ogr -f “PostgreSQL” PG:”dbname=’db_burundi’ host=’ep-solitary-tree-a2v2l0gq.eu-central-1.aws.neon.tech’ port=’5432′ user=’db_burundi_owner’ password=’g6zWtOXk9Taj'” 'C:\Users\Mamadou\Documents\GEODAFTAR\geowebapp-flask\data\bi_capital_areas.shp' -nln bi_capital_areas -s_srs EPSG:4326 -t_srs EPSG:4326


```
