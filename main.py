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
