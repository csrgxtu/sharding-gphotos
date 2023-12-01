from google_auth_oauthlib.flow import Flow


scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
flow = Flow.from_client_secrets_file('./client_secret.json', scopes=scopes, redirect_uri='http://localhost')

# Tell the user to go to the authorization URL.
auth_url, _ = flow.authorization_url(prompt='consent')

print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
flow.fetch_token(code=code, proxies=proxies)
print(f'Debug: fetch-token done: {flow.credentials}')

# You can use flow.credentials, or you can just get a requests session
# using flow.authorized_session.
session = flow.authorized_session()
print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
