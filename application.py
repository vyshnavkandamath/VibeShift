from flask import Flask, jsonify, redirect, render_template, url_for, request, session
import requests
import spotipy, json
from spotipy.oauth2 import SpotifyOAuth
import time
from sqlalchemy import null


app = Flask(__name__, static_folder='static', template_folder='template')


#------------------------------------------------------------------------APP TOKEN SETUP-----------------------------------------------------------------------------------#


app.secret_key = "TBD key value"
app.config['SESSION_COOKIE_NAME'] = 'User'
TOKEN_INFO = "token_info"
WEATHER_API_KEY = 'Weather API secret key value'


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
        client_id = 'TBD Spotify client id',
        client_secret = 'TBD Spotify client secret',
        redirect_uri = url_for('redirectPage', _external=True),
        scope='user-library-read')

#------------------------------------------------------------------------PROJECT PAGES AND ROUTES-----------------------------------------------------------------------------------#

@app.route('/home')
def home():
   return render_template('index.html')


@app.route('/musicrec')
def musicRecommendation():
    return render_template('musicrec.html')

    
    
    


#------------------------------------------------------------------------ WEATHER API FUNCTIONS AND ENDPOINTS-----------------------------------------------------------------------------------#
   
#This function retrieves the data from the form
@app.route('/locationData', methods=['GET', 'POST'])
def locationData():
    if request.method == 'POST':
        try:
            location = request.form.get('q')
            #print(location)
            locationAPIStatus = getWeatherAPIStatus(location) #Gets
            #print(locationAPIStatus)
            locationCurrent = getWeatherTemperature(location)
            print(locationCurrent)

            if((location != '') and (locationAPIStatus != 400)):
                return jsonify({"response" : "Success" }), 202
            else:
                return  jsonify(message='Location Does Not Exist or Input Not Entered Correctly. Try Again'),500
        except:
            return 'request.method is not POST. Check JavaScript Route'
        


#Gets the Weather Data JSON based on the location the user has passed and returns the Status
# @app.route('/getWeather', methods=['GET', 'POST'])
def getWeatherAPIStatusCode(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {
	     "key": "Weather API secret key value"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text)
    return response.status_code
        
#Gets Weather Data as a JSON
def getWeatherJSONData(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {
	     "key": "Weather API secret key value"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text)
    return response.text


#Parses the JSON to find the temperature in Fahrenheit and returns the value as a string
def getWeatherTemperature(locationInfo):
    url = "http://api.weatherapi.com/v1/current.json"
    querystring = {"q": locationInfo}
    headers = {
	     "key": "Weather API secret key value"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if(response.status_code == 200):
        jsonResponse = response.json()
        return jsonResponse['current']['temp_f']
    else:
        return 'could not find temperature since status code is invalid'

#------------------------------------------------------------------------ SPOTIFY API FUNCTIONS AND ENDPOINTS-----------------------------------------------------------------------------------#
   





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


