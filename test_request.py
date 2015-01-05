import json
import requests
import numpy as np

url = 'http://localhost:5000/api/getElevations'

points = []
for lat in np.linspace(-38.2,-37.2,1025):
  for lon in np.linspace(144.5,145.5,103):
    points.append({"lat": lat, "lon": lon})

data = {"points": points}
data_json = json.dumps(data)
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=data_json, headers=headers)

elevations = [point['elevation'] for point in (response.json())['points']]
print len(elevations)