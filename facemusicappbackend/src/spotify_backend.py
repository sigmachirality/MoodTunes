import requests

client_id = 'd1c6d4ce29344d8781fc4965d067f203'
client_secret = '739bfdda44c84fd882a54e6d994ea28f'

together = client_id + ':' + client_secret

"""
'Tunable' attributes for a song, as defined by Spotify, range 0..1
"""
tunable_attributes = [
    'danceability',
    'energy',
    'loudness',
    'mode',
    'tempo',
    'valence'
]

"""
Gets an access token from spotify based on our registered app
"""
def get_access_token():
    #r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': 'Basic ' + 'ZDFjNmQ0Y2UyOTM0NGQ4NzgxZmM0OTY1ZDA2N2YyMDM6NzM5YmZkZGE0NGM4NGZkODgyYTU0ZTZkOTk0ZWEyOGYK'}, data={'grant_type': 'client_credentials'})
    r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret})
    access_token = (r.json())["access_token"]
    headers_data = {'Authorization' : 'Bearer ' + access_token}
    return access_token, headers_data

access_token, headers_data = get_access_token()

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
Returns an array of tracks.
"""
def get_tracks_by_attributes(seed_track_id, **kwargs):
    kwargs_list = []
    for key, value in kwargs.items():
        kwargs_list.append(str(key) + '=' + str(value))
    req = 'https://api.spotify.com/v1/recommendations?'
    for a in kwargs_list[:-1]:
        req = req + a + '&'
    req = req + kwargs_list[-1]
    req = req + seed_track_id
    global headers_data
    req = requests.get(req, headers=(headers_data))
    tracks = req["tracks"]
    return tracks


"""
Gets a tracks 'tunable attributes' provided a list of attributes 
"""
def get_attributes(track_id, attributes):
    global headers_data
    req = requests.get('https://api.spotify.com/v1/audio-features/' + track_id, headers=headers_data)
    req = req.json()
    res = {}
    for attr in attributes:
        res[attr] = req[attr]
    return res



"""
Scans an array of tracks, calulating deviations from target values of tunable attributes
"""
def get_dev(tracks, target_values):
    out = {}
    for track in tracks:
        track_id = track["id"]
        print('Calculating deviations for track: ' + track_id)
        values = get_attributes(track_id, list(target_values.keys()))
        deviations = []
        for attr, val in values.items():
            print(attr + ' target value is: ' + str(target_values[attr]))
            print(attr + ' actual value is: ' + str(val))
            dev = target_values[attr] - val
            deviations.append(dev)
        sum_dev = 0
        for dev in deviations:
            sum_dev = sum_dev = abs(dev)
        out[track_id] = sum_dev
    return out
        


"""
Scans an array of tracks, looking for the song that best matches target attributes
"""
def scan_playlist(tracks, target_values):
    devs = get_dev(tracks, target_values)
    return min(devs, key=devs.get)


"""
Gets a users top tracks and stores them in a list
"""
def get_top_tracks():
    pass



tracks = [{"id": '06AKEBrKUckW0KREUWRnvT'}, {"id": "6rqhFgbbKwnb9MLmUQDhG6"}]
target_values = {'valence' : 0, 'energy': 0.8}
b = scan_playlist(tracks, target_values)
print(b)





    