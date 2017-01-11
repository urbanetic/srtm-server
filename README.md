# SRTM Server

A Flask based python REST API for the srtm module to get elevations for an area described by a lat/lon bounding box.

### To run:

    pip install -r requirements.txt
    python ./srtm_server.py

Starts on port 5000



### Heroku deployment

Get toolbet from here:
    https://devcenter.heroku.com/articles/getting-started-with-python#set-up

Run the following commands:

    heroku login
    virtualenv venv

Just on Windows:

    venv\Scripts\activate.bat


Just on *NIX:

```source venv/bin/activate```



    pip install -r requirements.txt --allow-all-external
    heroku create
    git push heroku master
    heroku ps:scale web=1
    heroku open


Browser should open displaying ```"Hello World!"```


#### To make a request

Form a URL as follows:

    APP_URL/api/getElevations?north=TOP_LAT&south=BOTTOM_LAT&east=RIGHT_LON&west=LEFT_LON&resolution=RES

E.g.

https://shielded-ridge-5272.herokuapp.com/api/getElevations?north=-37.7&south=-38&east=145.2&west=144.9&resolution=256


or


<localhost:5000/api/getElevations?north=-37.7&south=-38&east=145.2&west=144.9&resolution=256>


#### Return type

An 8 bit RBG png image height map of the area specified is returned. Each pixels value represents height above sea level in meters encoded as follows;

Height(m) = R\*255 + G + B\*100


E.g.

![Example output image.](http://i.imgur.com/FQZ8nKf.png "Example output.")


#### Get elevation from one coordinate pair

Form a URL as follows:

    APP_URL/api/getElevation?lat=LAT&lon=LON

E.g.

http://localhost:5000/api/getElevation?lat=43.6168&lon=6.95063
 79

#### Get country code from one coordinate pair

Form a URL as follows:

    APP_URL/api/getCountry?lat=LAT&lon=LON

E.g.

http://localhost:5000/api/getCountry?lat=43.6168&lon=6.95063
 FR

### Licence

The data file `polygons.properties` is available under a [Creative Commons Attribution-Share Alike License](http://creativecommons.org/licenses/by-sa/3.0/) in accordance with the license from https://github.com/bencampion/reverse-country-code. It was copied and fixed from [daveross/offline-country-reverse-geocoder](https://github.com/daveross/offline-country-reverse-geocoder)
