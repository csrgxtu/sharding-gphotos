from google_auth_oauthlib.flow import Flow
import requests


scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
flow = Flow.from_client_secrets_file('./client_secret.json', scopes=scopes, redirect_uri='http://localhost')

# Tell the user to go to the authorization URL.
auth_url, _ = flow.authorization_url(prompt='consent')

print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
creds = flow.fetch_token(code=code, proxies=proxies)
print(f'Debug: fetch-token done: {flow.credentials}, {creds}')

res = requests.post(
    'https://photoslibrary.googleapis.com/v1/mediaItems:search',
    headers={
        'content-type': 'application/json',
        'Authorization': f'Bearer {creds.get("access_token")}'
    },
    proxies=proxies,
    json={
        'pageSize': 1,
        'pageToken': None,
        'filters': {
            'dateFilter': {
                'ranges': [{
                    'startDate': {
                        'year': 2023,
                        'month': 10,
                        'day': 1
                    },
                    'endDate': {
                        'year': 2023,
                        'month': 10,
                        'day': 31
                    }
                }]
            }
        }
    }
)
print(f'Debug {res.status_code} -> {res.content}')

# # You can use flow.credentials, or you can just get a requests session
# # using flow.authorized_session.
# session = flow.authorized_session()
# # print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
# print(f'Debug authorized session')


# nextPageToken = None
# media_items = []
# while True:
#     response = session.post(
#         'https://photoslibrary.googleapis.com/v1/mediaItems:search', 
#         headers = { 'content-type': 'application/json' },
#         proxies=proxies,
#         json={ 
#             "pageSize": 100,
#             "pageToken": nextPageToken,
#             "filters": {
#                 "dateFilter": {
#                     "ranges": [{ 
#                         "startDate": {
#                             "year": 2023,
#                             "month": 10,
#                             "day": 1,
#                         },
#                         "endDate": {
#                             "year": 2023,
#                             "month": 10,
#                             "day": 31,
#                         }
#                     }]
#                 }
#             }
#         })
    
#     response_json = response.json()
#     media_items += response_json["mediaItems"]
#     # print(f'Debug mediaItems:search {response_json}')
    
#     if not "nextPageToken" in response_json:
#         break
        
#     nextPageToken = response_json["nextPageToken"]
