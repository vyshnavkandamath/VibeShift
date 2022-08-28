from crypt import methods
from flask import Flask, jsonify, redirect, render_template, url_for, request, session
from httplib2 import Authentication
import requests
import spotipy, json
from spotipy.oauth2 import SpotifyOAuth
import time
from sqlalchemy import null
from stripe import client_id
from spotipy.oauth2 import SpotifyClientCredentials
import os

app = Flask(__name__, static_folder='static', template_folder='template')


#------------------------------------------------------------------------APP TOKEN SETUP-----------------------------------------------------------------------------------#

app.secret_key = os.environ['APP_KEY']
app.config['SESSION_COOKIE_NAME'] = 'User'
TOKEN_INFO = "token_info"

#------------------------------------------------------------------------SPOTIFY API AUTHENTICATION-----------------------------------------------------------------------------------#

#Home Route Shows Authorize Page for Spotify, Where user must log in to use. 
@app.route("/")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("tokenAuthPage", _external=True))


@app.route('/tokenauth')
def tokenAuthPage():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login"), external= True)

    sp = spotipy.Spotify(auth=token_info['access_token'])
    return redirect(url_for('home'))


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


#OAuth function
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id =  os.environ['SPOTIFY_CLIENT_ID'],
        client_secret = os.environ['SPOTIFY_CLIENT_SECRET'],
        redirect_uri = url_for('redirectPage', _external=True),
        scope='user-read-private')

# API_BASE = 'https://accounts.spotify.com'
# SCOPE = 'user-library-read' 
# REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
# SHOW_DIALOG = True
# CLI_ID = 'Spotify client id'
# CLI_SEC = 'Spotify client secret'

# @app.route("/")
# def verify():
#     auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
#     print(auth_url)
#     return redirect(auth_url)

# @app.route("/api_callback")
# def api_callback():
#     session.clear()
#     code = request.args.get('code')

#     auth_token_url = f"{API_BASE}/api/token"
#     res = requests.post(auth_token_url, data={
#         "grant_type":"authorization_code",
#         "code":code,
#         "redirect_uri":"http://127.0.0.1:5000/api_callback",
#         "client_id":CLI_ID,
#         "client_secret":CLI_SEC
#         })

#     res_body = res.json()
#     print(res.json())
#     session["toke"] = res_body.get("access_token")

#     return redirect(url_for("home"))

# @app.route("/go", methods=['POST'])
# def go():
#     data = request.form    
#     sp = spotipy.Spotify(auth=session['toke'])
#     response = sp.current_user()
#     return render_template("results.html", data=data)




#Using the sessions, it retrieves the data and profile of the current_user
@app.route('/userProfile', methods=['GET','POST'])
def getUserProfile():
    tokenResponse = get_token()
    print(tokenResponse)
    
    accessToken = tokenResponse['access_token']

    base_url = 'https://api.spotify.com/v1/'

        
    headers = {
        'Authorization': 'Bearer {token}'.format(token=accessToken)
    }
    response = requests.get(base_url + "me", headers=headers)
    responseJson = response.json()
    return responseJson


#------------------------------------------------------------------------PROJECT PAGES AND ROUTES-----------------------------------------------------------------------------------#

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/musicrec')
def musicRecommendation():
    return render_template('musicrec.html')

#------------------------------------------------------------------------ WEATHER API FUNCTIONS AND ENDPOINTS-----------------------------------------------------------------------------------#
#This function retrieves the data from the form -- ****POST route Endpoint****
@app.route('/locationData', methods=['GET', 'POST'])
def locationData():
    
    if request.method == 'POST':
        try:
            location = request.form.get('q')
            #print(location)
            locationAPIStatus = getWeatherAPIStatusCode(location) #Gets
            #print(locationAPIStatus)
            locationCurrent = getWeatherTemperature(location)
            print(locationCurrent)

            locationCondition = getWeatherCondition(location)
            print(locationCondition)


            if((location != '') and (locationAPIStatus != 400)):
                return jsonify({"response" : "Success" }), 202
            else:
                return  jsonify(message='Location Does Not Exist or Input Not Entered Correctly. Try Again'),500
        except:
            return 'request.method is not POST. Check JavaScript Route'

# @app.route('/storeLocation', methods=['GET', 'POST'])
# def storeLocation():
#     if request.method == 'POST':
#         try:
#             location = request.form.get('q')
#             print(location)
#             return jsonify(location)
#         except:
#             return 'Could not return the location'


#Gets the Weather Data JSON based on the location the user has passed and returns the Status
# @app.route('/getWeather', methods=['GET', 'POST'])
def getWeatherAPIStatusCode(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {}
    headers['key'] = os.environ['WEATHER_API_KEY']
    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text)
    return response.status_code
        
#Gets Weather Data as a JSON
def getWeatherJSONData(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {}
    headers['key'] = os.environ['WEATHER_API_KEY']

    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text)
    return response.text


#Parses the JSON to find the temperature in Fahrenheit and returns the value as a string
def getWeatherTemperature(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {}
    headers['key'] = os.environ['WEATHER_API_KEY']
    response = requests.request("GET", url, headers=headers, params=querystring)

    if(response.status_code == 200):
        jsonResponse = response.json()
        return jsonResponse['current']['temp_f']
    else:
        return 'could not find temperature since status code is invalid'


def getWeatherCondition(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {}
    headers['key'] = os.environ['WEATHER_API_KEY']
    response = requests.request("GET", url, headers=headers, params=querystring)

    if(response.status_code == 200):
        jsonResponse = response.json()
        return jsonResponse['current']['condition']['text']
    else:
        return 'could not find condition since status code is invalid'
    

#------------------------------------------------------------------------ SPOTIFY API FUNCTIONS AND ENDPOINTS FOR PLAYLISTS-----------------------------------------------------------------------------------#

AUTH_URL = 'https://accounts.spotify.com/api/token' #Spotiy Auth URL
CLIENT_ID =  os.environ['SPOTIFY_CLIENT_ID'],
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET'],

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})


# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

# @app.route('/current_user' , methods=['GET'])
# def current_user():
#     cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user()
#Retrieves the Playlist Info based on location's weather
@app.route('/playlistInfo', methods=['POST'])
def getPlaylistName():
    print('going in')
    if request.method == 'POST':
        locationD = request.form.get('location')
        print(locationD)
        place = locationD
        result = getWeatherPlaylist(place)
        # return jsonify({"response" : "Success" }), 202
        return jsonify(result)
    
    # if request.method == 'GET':
        
    #     place = locationD
    #     result = getWeatherPlaylist(place) 
    #     return jsonify(result)

# @app.route('/playlistImage', method=['GET', 'POST'])
def getPlaylistImage(playlistID):
    base_url = 'https://api.spotify.com/v1/'
        
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    response = requests.get(base_url + "playlists/" + playlistID + "/images", headers=headers)
    responseJson = response.json()
    return responseJson['url']

#This is the main route for retrieving playlist based on weather
def getWeatherPlaylist(locationInfo):
    rain = 'rain'
    shower = 'shower'
    thunder = 'thunder'
    patches = 'patches'
    snow = 'snow'
    if(getWeatherCondition(locationInfo) == 'Sunny' or getWeatherCondition(locationInfo) == 'Clear'):
        return sunnyWeatherPlaylists()
    elif(getWeatherCondition(locationInfo) == 'Overcast' or getWeatherCondition(locationInfo) == 'Rain'):
        return overcastWeatherPlaylists() 
    elif(getWeatherCondition(locationInfo) == 'Partly cloudy' or getWeatherCondition(locationInfo) == 'Partly clear' or getWeatherCondition(locationInfo) == 'Mostly clear'):
        return partlyCloudyPlaylists()
    elif(getWeatherCondition(locationInfo) == 'Showers' or getWeatherCondition(locationInfo) == 'Mist' or getWeatherCondition(locationInfo) == 'Light rain'):
        return showerWeatherPlaylists() 
    elif(rain in getWeatherCondition(locationInfo) or shower in getWeatherCondition(locationInfo) or thunder in getWeatherCondition(locationInfo)  or patches in getWeatherCondition(locationInfo)  or snow in getWeatherCondition(locationInfo) ):
        return showerWeatherPlaylists()
    else:
        return 'Some Random Playlist Decided Later'

##### Sunny Playlist: Soak Up The Sun
##### Party Cloudy Playlist: just hits.
##### Overcast Cloudy Playlist: Are n Be?
##### Showers Playlist: Chilled RnB

# Returns Playlist Name of Sunny Weather Linked Playlist
def sunnyWeatherPlaylists():
    try:
        
        base_url = 'https://api.spotify.com/v1/'
        playlist_id = '37i9dQZF1DX6ALfRKlHn1t'
    
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        response = requests.get(base_url + "playlists/" + playlist_id, headers=headers)
        responseJson = response.json()
        #return responseJson['name']
        return responseJson
           
        
    except:
        return "Didn't Get Playlist Data"


# Returns Playlist Name of Overcast Weather Linked Playlist
def overcastWeatherPlaylists():
    try:
        
        base_url = 'https://api.spotify.com/v1/'
        playlist_id = '37i9dQZF1DXa9xHlDa5fc6'

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        response = requests.get(base_url + "playlists/" + playlist_id, headers=headers)
        responseJson = response.json()
        #return responseJson['name']
        return responseJson
           
    except:
        return "Didn't Get Playlist Data"


def partlyCloudyPlaylists():
    try:
        base_url = 'https://api.spotify.com/v1/'
        playlist_id = '37i9dQZF1DXcRXFNfZr7Tp'

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        response = requests.get(base_url + "playlists/" + playlist_id, headers=headers)
        responseJson = response.json()
        #return responseJson['name']
        return responseJson
           

    except:
        return "Didn't Get Playlist Data"


def showerWeatherPlaylists():
    try:
        
        base_url = 'https://api.spotify.com/v1/'
        playlist_id = '37i9dQZF1DX2UgsUIg75Vg'
       

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        response = requests.get(base_url + "playlists/" + playlist_id, headers=headers)
        responseJson = response.json()
        #return responseJson['name']
        return responseJson
           
        

    except:
        return "Didn't Get Playlist Data"


    # location = request.get_data('q')
    # print(location)
    # if(location != None):
    #     return jsonify({"response" : "Success" }), 202
    # else:
    #      return  jsonify(message='invalid input error'),500
    
# @app.route('/gettracks')
# def getTracks():
#     try:
#         token_info = get_token()
#     except:
#         print("user not logged in")
#         return redirect(url_for("login"), _external=True)

#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     all_songs= []
#     iter = 0
#     while True:
#         items = sp.current_user_saved_tracks(limit=50, offset=iter*50)['items']
#         iter += 1
#         all_songs += items
#         if(len(items) < 50):
#             break

#     return str(len(all_songs))

#gets the current users token 

if __name__ == "__main__":
    app.run()
