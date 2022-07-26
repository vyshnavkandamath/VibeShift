from flask import Flask, redirect, render_template, url_for, request, session
import spotipy, json
from spotipy.oauth2 import SpotifyOAuth
import time







app = Flask(__name__, static_folder='static', template_folder='template')


#------------------------------------------------------------------------SPOTIFY API TOKEN SETUP-----------------------------------------------------------------------------------#


app.secret_key = "TBD key value"
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
        client_id = 'TBD Spotify client id',
        client_secret = 'TBD Spotify client secret',
        redirect_uri = url_for('redirectPage', _external=True),
        scope='user-library-read')

#------------------------------------------------------------------------PROJECT PAGES AND ROUTES-----------------------------------------------------------------------------------#

@app.route('/home')
def home():
   return render_template('index.html')






#------------------------------------------------------------------------API FUNCTIONS AND ENDPOINTS-----------------------------------------------------------------------------------#

# @app.route("/location")
# def getLocation():

    







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


