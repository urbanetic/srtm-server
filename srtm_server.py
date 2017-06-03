from flask import Flask, request, url_for, send_file
from flask_cors import cross_origin
import srtm
import math
import datetime
import os
import sys
import logging
import png
import os.path
from itertools import product, starmap, islice
from country_poligons import CountryPoligons

elevation_data = srtm.get_data()
country_data = CountryPoligons()
app = Flask(__name__, static_folder='static', static_url_path='')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/', methods=['GET'])
@cross_origin()
def helloworld():
  return "SRTM-server is up and running. See readme for usage instructions.", 200

@app.route('/api/getCountry', methods=['GET'])
@cross_origin()
def get_country():
  print "Request received at: " + str(datetime.datetime.now())
  intime = datetime.datetime.now()

  lat = float(request.args['lat'])
  lon = float(request.args['lon'])
  return country_data.get_country(lat, lon)

@app.route('/api/getElevation', methods=['GET'])
@cross_origin()
def get_elevation():
  print "Request received at: " + str(datetime.datetime.now())
  intime = datetime.datetime.now()

  lat = float(request.args['lat'])
  lon = float(request.args['lon'])
  height = elevation_data.get_elevation(lat, lon)
  return str(height)

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
  # try: ignore_cache = bool(request.args['ignore_cache'])
  # except e: ignore_cache = False
  # try: ignore_cache = bool(request.args['clean_data'])
  # except e: clean_data = False

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
      ele_row.append(height)
    elevations.append(ele_row)

  elevations = [map(generate_height_color, h) for h in fill_holes(elevations)]
  path = generate_path(north, south, east, west, resolution)
  img = png.from_array(elevations, 'RGB').save(path)
  return path

def fill_holes(matrix):
  for i, row in enumerate(matrix):
    for j, val in enumerate(row):
      if val is None:
        matrix[i][j] = average(find_neighbors(matrix,i,j))
  return matrix

def average(array):
  count = 0
  total = 0
  for i in array:
    if i is not None:
      count += 1
      total += i
  return total/(count or 1)

def find_neighbors(grid, x, y):
    xi = (0, -1, 1) if 0 < x < len(grid) - 1 else ((0, -1) if x > 0 else (0, 1))
    yi = (0, -1, 1) if 0 < y < len(grid[0]) - 1 else ((0, -1) if y > 0 else (0, 1))
    return list(islice(starmap((lambda a, b: grid[x + a][y + b]), product(xi, yi)), 1, None))

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
