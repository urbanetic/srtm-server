from flask import *
from flask.ext.cors import cross_origin
import srtm
import numpy as np
import math
import logging
import datetime

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

elevation_data = srtm.get_data()
app = Flask(__name__)


@app.route('/', methods=['GET'])
@cross_origin()
def create_task():
  return "HELLO WORLD!", 200

@app.route('/api/getElevations', methods=['GET'])
@cross_origin()
def create_task():
  print "INCOMING!!!!!!--: " + str(datetime.datetime.now())
  intime = datetime.datetime.now()
  # TODO (gbcowan) check if input is valid
  



  north = float(request.args['north'])
  south = float(request.args['south'])
  east = float(request.args['east'])
  west = float(request.args['west'])
  resolution = float(request.args['resolution'])
  print north
  print south
  print east
  print west
  print resolution

  lon = west
  lat = north
  x_step_size = math.fabs(east-west) / resolution
  y_step_size = math.fabs(north-south) / resolution
  points = []

  while(lat > south):
    if (lat <= -90): lat += 180
    lon = west
    row = []
    while(lon < east):
      if (lon >= 180): lon -=360
      row.append([lat, lon])
      lon += x_step_size
    points.append(row)
    lat -= y_step_size
  elevations = []
  for row in points:
    ele_row = []
    for point in row:
      ele_row.append(elevation_data.get_elevation(point[0], point[1]))
    elevations.append(ele_row)
  print "THAR SHE BLOWS, process time: " + str(datetime.datetime.now()-intime)
  
  ele_str = "|".join([(",".join(str(i) for i in a)) for a in elevations])
  return (ele_str), 200
  # return jsonify(east= east, west= west, north= north, south= south, resolution= resolution,
  #                   points= elevations), 200

if __name__ == '__main__':
    app.run(debug=True, port=33507)
