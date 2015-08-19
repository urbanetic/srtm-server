from flask import Flask, request, url_for, send_file
from flask.ext.cors import cross_origin
import srtm
import numpy as np
import math
import datetime
import os
import sys
import logging
import png
import os.path

elevation_data = srtm.get_data()
app = Flask(__name__, static_folder='static', static_url_path='')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/', methods=['GET'])
@cross_origin()
def helloworld():
  return "HELLO WORLD!", 200

@app.route('/api/getElevations', methods=['GET'])
@cross_origin()
def create_task():
  print "Request received at: " + str(datetime.datetime.now())
  intime = datetime.datetime.now()
  
  north = float(request.args['north'])
  south = float(request.args['south'])
  east = float(request.args['east'])
  west = float(request.args['west'])
  resolution = float(request.args['resolution'])

  path = generate_path(north, south, east, west, resolution)
  if not os.path.isfile(path):
    generate_image(north, south, east, west, resolution)
  print "Request processed. Time elapsed: " + str(datetime.datetime.now()-intime)
  return send_file(path, mimetype='image/png')

def generate_image(north, south, east, west, resolution):
  lon = west
  lat = north
  x_step_size = math.fabs(east-west) / resolution
  y_step_size = math.fabs(north-south) / resolution
  points = []

  # Get lat/lon grid
  while(lat > south):
    if (lat <= -90): lat += 180
    lon = west
    row = []
    while(lon < east):
      if (lon >= 180): lon -=360
      row.append([lat, lon])
      lon += x_step_size
    while len(row) > resolution:
      del row[-1]
    points.append(row)
    lat -= y_step_size
  while len(points) > resolution:
    del points[-1]
  
  # Get elevations
  elevations = []
  for row in points:
    ele_row = []
    for point in row:
      height = elevation_data.get_elevation(point[0], point[1])
      if height is None: height = 0
      ele_row.append(generate_height_color(height))
    elevations.append(ele_row)

  path = generate_path(north, south, east, west, resolution)
  img = png.from_array(elevations, 'RGB').save(path)
  return path

def generate_height_color(height):
  r = int(height/255)
  g = int(height%255)
  b = int(100*height%1)
  return [r, g, b]

def generate_path(north, south, east, west, resolution):
  return "cache/" + str(north) + "_" + str(east) + "_" + str(south) + "_" + str(west) + "_" + str(resolution) + ".png"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
