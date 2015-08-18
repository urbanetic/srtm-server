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

A greyscale png image height map of the area specified is returned. Each pixels value represents height above sea level in meters.


E,g, 

![Example output image.](http://i.imgur.com/0PQI9M8.png "Example output.")
