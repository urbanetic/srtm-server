# SRTM Server

A Flask based python REST API for the srtm module to get elevations for a list of lat/lon points.

To run:

    pip install -r requirements.txt
    python ./srtm_server.py

Starts on port 5000



Heroku deployment:

Get toolbet from here:
https://devcenter.heroku.com/articles/getting-started-with-python#set-up

heroku login
virtualenv venv
WINDOWS:
venv\Scripts\activate.bat
*NIX
source venv/bin/activate
pip install -r requirements.txt --allow-all-external
heroku create
git push heroku master
heroku ps:scale web=1
heroku open
ROOT_URL/api/getElevations?north=-37.7&south=-38&east=145.2&west=144.9&resolution=512
e.g.
https://shielded-ridge-5272.herokuapp.com/api/getElevations?north=-37.7&south=-38&east=145.2&west=144.9&resolution=512
