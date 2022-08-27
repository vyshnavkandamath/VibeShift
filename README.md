Music project
=============
A music platform/app which recommends and generates spotify playlists based off geographical weather data

# Install steps
1. Use Ubuntu 20.04
2. sudo apt-get install python3-pip
3. sudo apt install python3.8-venv
4. source env/bin/activate
5. pip install wheel
6. python3 -m pip install -r requirements.txt
7. export FLASK_APP=application.py
8. set FLASK_APP=application.py
9. export SPOTIFY_CLIENT_ID=<Spotify API client id>
10. export SPOTIFY_CLIENT_SECRET=<Spitfy API client secret>
11. export WEATHER_API_KEY=<Weather API key>
12. python3 -m flask run

Now point your browser to http://127.0.0.1:5000 to invoke the web application
