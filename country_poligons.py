#!/usr/bin/env python

from shapely.geometry import Polygon, Point

class CountryPoligons:

  country_data = None

  def __init__(self, filename='polygons.properties'):
    self.filename = filename
    self._load_polygon()
  
  def _load_polygon(self):
    self.country_data = {}
  
    with open(self.filename, 'r') as f:
      for line in f:
        line = line.strip()
        if len(line) == 0:
          continue
  
        (country_code, data) = line.split('=', 1)
        (polygon_type, data) = data.split(' ', 1)
        data = data[3:-3]
  
        if country_code not in self.country_data:
          self.country_data[country_code] = []
        if 'POLYGON' == polygon_type:
          self.country_data[country_code].append(self._split_coord(data))
        elif 'MULTIPOLYGON' == polygon_type:
          for polygon in data.split(')),(('):
            self.country_data[country_code].append(self._split_coord(polygon))
  
  
  def _split_coord(self, coords):
    res = []
    for pair in coords.split(','):
      (lat, lon) = pair.split(' ')
      res.append((float(lat), float(lon)))
    return Polygon(res)

  def get_country(self, lat, lon):
    p = Point(lon, lat)

    for country in self.country_data.keys():
      for poly in self.country_data[country]:
        if poly.contains(p):
          return country
    return ''
