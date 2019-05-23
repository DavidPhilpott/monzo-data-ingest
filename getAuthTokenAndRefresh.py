
# importing the requests library
import requests

# defining the api-endpoint
API_ENDPOINT = "https://api.monzo.com/oauth2/token"

# data to be sent to api
params = {'grant_type': 'authorization_code',
          'client_id': 'oauth2client_00009cXMOQ2R1xCVY5BIwr',
          'client_secret': 'mnzconf.FC4A0cAyD6ooTvKIXSws45jb5U3N5H7UInlExx2NmE7WmHOa3WCTvH5SMNF9AYZyhJ/lv85ibEFe3NyfvWCn',
          'redirect_uri': 'http://localhost:2020',
          'code': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IjlaZG5UYWRIMHlVOXJPSytrMGlYIiwianRpIjoiYXV0aHpjb2RlXzAwMDA5ajZlcDdyelo0c044QU91bFYiLCJ0eXAiOiJhemMiLCJ2IjoiNSJ9.0JLPvKy1_JAUn4Z0YMl-crIJ5NS4iMRT2R4jFDJwbd2X98oHZhG6gVT6-xGgrY6_ef48jKaV2IwP6mR2JxOuLQ'}

r = requests.post(url=API_ENDPOINT, data=params)
result_text = r.text
print(result_text)