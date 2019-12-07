from flask import *
import shapefile
import re
from difflib import SequenceMatcher


app = Flask(__name__)

#searches given file for query index of field
def searchShapefileForQuery(query, result, shapefile, field):
    sf = shapefile.Reader(shapefile)
    records = sf.records()
    #loops through all records
    for rec in records:
        name = rec[field].lower()
        #if name is exactly query set result[1](SequenceMatch ratio) to 1
        if name == query:
            result[0] = name
            result[1] = 1
            return result
        #if name starts with query check if result[1] is smaller then new Sequence if true result will be new record
        if name.startswith(query):
            if result[1] < SequenceMatcher(None, name, query).ratio():
                result[0] = name
                result[1] = SequenceMatcher(None, name, query).ratio()
    return result


@app.route('/requestQuery', methods=['POST'])
def requestQuery():
    query = request.args.get('query')
    # result[name, SequenceMatch ratio]
    result = ['not found', 0]
    #check if query is a postcode e.g. [5432 AA]
    if re.findall('[0-9]', query):
        result = searchShapefileForQuery(query, result, 'shapefiles/openpostcodevlakkenpc4.shp', 0)
    else:
        query = query.lower()
        result = searchShapefileForQuery(query, result, 'shapefiles/gis_osm_places_free_1.shp', 4)
        result = searchShapefileForQuery(query, result, 'shapefiles/gis_osm_roads_free_1.shp', 3)
    return result[0]

if __name__ == '__main__':
    app.run()
