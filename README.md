# SRTM Server

A Flask based python REST API for the srtm module to get elevations for a list of lat/lon points.

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

    ROOT_URL/api/getElevations?north=TOP_LAT&south=BOTTOM_LAT&east=RIGHT_LON&west=LEFT_LON&resolution=RES

E.g.

https://shielded-ridge-5272.herokuapp.com/api/getElevations?north=-37.7&south=-38&east=145.2&west=144.9&resolution=512


#### Return type

Data returns a string sepearated by ```|``` each substring (between ```|```) represents a horizontal row of heights.

Heights are seperated by commas.

Heights are in metres above sea level. 
