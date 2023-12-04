
# ref https://developers.google.com/identity/protocols/oauth2/web-server#httprest_1
GOOGLE_OAUTH_BASE = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_OAUTH_API = '{GOOGLE_OAUTH_BASE}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&prompt=consent&access_type=offline'
GOOGLE_OAUTH_TOKEN = 'https://oauth2.googleapis.com/token'

GOOGLE_PHOTO_SEARCH = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
GOOGLE_USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}'
