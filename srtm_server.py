from flask import *
import srtm

elevation_data = srtm.get_data()
app = Flask(__name__)

@app.route('/api/getElevations', methods=['POST'])
def create_task():
    return_array = []
    if not request.json:
        abort(400)
    # TODO (gbcowan) check if json has all the right bits
    points =  request.json['points']
    for point in points:
        lat = point['lat']
        lon = point['lon']
        ele = elevation_data.get_elevation(lat, lon)
        return_array.append({'lat': lat, 'lon': lon, 'elevation': ele})
    return jsonify(points = return_array), 200

if __name__ == '__main__':
    app.run(debug=True)
