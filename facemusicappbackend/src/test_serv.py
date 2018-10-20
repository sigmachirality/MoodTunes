import requests

client_id = 'd1c6d4ce29344d8781fc4965d067f203'
client_secret = '739bfdda44c84fd882a54e6d994ea28f'

together = client_id + ':' + client_secret

tunable_attributes = [
    'danceability',
    'energy',
    'loudness',
    'mode',
    'tempo',
    'valence'
]

def get_access_token():
    #r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': 'Basic ' + 'ZDFjNmQ0Y2UyOTM0NGQ4NzgxZmM0OTY1ZDA2N2YyMDM6NzM5YmZkZGE0NGM4NGZkODgyYTU0ZTZkOTk0ZWEyOGYK'}, data={'grant_type': 'client_credentials'})
    r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret})
    access_token = (r.json())["access_token"]
    headers_data = {'Authorization' : 'Bearer ' + access_token}
    return access_token, headers_data

"""
Gets the text version of a spotify track from its track id.
"""
def get_track(track_id):
    req = requests.get('https://api.spotify.com/v1/tracks/' + track_id, headers={'Authorization' : 'Bearer ' + access_token})
    return req.text

"""
Gets a list of avaliable Spotify genres
"""
def get_genres():
    req = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds', headers={'Authorization' : 'Bearer ' + access_token})
    return req.text

"""
Gets recommendations of Spotify tracks based on 'tunable track attributes' (as defined by Spotify)
"""
def get_tracks_by_attributes(**kwargs):
    kwargs_list = []
    for key, value in kwargs.items():
        kwargs_list.append(str(key) + '=' + str(value))
    req = 'https://api.spotify.com/v1/recommendations?'
    for a in kwargs_list[:-1]:
        req = req + a + '&'
    req = req + kwargs_list[-1]
    req = req + "&seed_tracks=0c6xIDDpzE81m2q797ordA" # Hard-coded favorite track. Personalization will be implemented later.
    global headers_data
    req = requests.get(req, headers=(headers_data))
    return req.text

"""
Scans a playlist, and chooses tracks based on 'tunable track attributes'
"""
def find_in_playlist(**kwargs):
    pass

access_token, headers_data = get_access_token()
print(get_tracks_by_attributes(target_valence=0.5))


    