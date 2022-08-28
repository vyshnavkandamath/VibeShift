Music project
=============
A music platform/app which recommends and generates spotify playlists based off geographical weather data

# Install steps
1. Use Ubuntu 20.04
2. git clone https://github.com/vyshnavkandamath/VibeShift.git
3. sudo apt-get install python3-pip
4. sudo apt install python3.8-venv
5. python3 -m venv env
6. source env/bin/activate
7. pip install wheel
8. pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz --no-deps
9. python3 -m pip install -r requirements.txt
10. export FLASK_APP=application.py
11. set FLASK_APP=application.py
12. export SPOTIFY_CLIENT_ID=<Spotify API client id>
13. export SPOTIFY_CLIENT_SECRET=<Spitfy API client secret>
14. export WEATHER_API_KEY=<Weather API key>
15. export export APP_KEY=<APP key here>
16. python3 -m flask run

Now point your browser to http://127.0.0.1:5000 to invoke the web application
