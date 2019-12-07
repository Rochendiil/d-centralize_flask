import point as point
from flask import Flask
from flask import *
import shapefile
import re
from difflib import SequenceMatcher


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def searchPostalCode(query):
    result = [0,0]
    sfPostal = shapefile.Reader('schapefiles/openpostcodevlakkenpc4.shp')
    records = sfPostal.records()
    for rec in records:
        number = rec[0]
        if number == query:
            result[0] = number
            result[1] = 1
            return result[0]
        if number.startswith(query):
            if result[1] < SequenceMatcher(None, number, query).ratio():
                result[0] = number
                result[1] = SequenceMatcher(None, number, query).ratio()
    return result[0]



#searches given file for query result at index namefield
def searchall(query, result, file, namefield):
    sf = shapefile.Reader(file)
    records = sf.records()
    #loops through all records
    for rec in records:
        name = rec[namefield].lower()
        #if name is exactly query set result[1](sequence percent) to 1
        if name == query:
            result[0] = rec[namefield]
            result[1] = 1
            return result
        #if name starts with query check if result[1] is smaller then new Sequence if true result will be new record
        if name.startswith(query):
            if result[1] < SequenceMatcher(None, name, query).ratio():
                result[0] = rec[namefield]
                result[1] = SequenceMatcher(None, name, query).ratio()
    if not result:
        return 'not found'
    else:
        return result


@app.route('/requestQuery', methods=['POST'])
def requestQuery():
    query = request.args.get('query')
    #check if query is a postcode e.g. [5432 AA]
    if re.findall('[0-9]', query):
        return searchPostalCode(query)
    else:
        query = query.lower()
        result = [0,0]
        result = searchall(query, result, 'schapefiles/gis_osm_places_free_1.shp', 4)
        result = searchall(query, result, 'schapefiles/gis_osm_roads_free_1.shp', 3)
        return result[0]

if __name__ == '__main__':
    app.run()
