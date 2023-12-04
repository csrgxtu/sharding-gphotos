import uuid
from fastapi import FastAPI, BackgroundTasks, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from aioconsole import aprint
from gauth import GAuth, GPhoto

app = FastAPI()
# app.mount("/site", StaticFiles(directory="html", html=True), name="static")
templates = Jinja2Templates(directory="html")

@app.get('/')
async def index(request: Request, response: Response):
    response = templates.TemplateResponse('index.html', {"request": request})
    response.set_cookie(key='session_id', value=uuid.uuid4().hex)
    return response

@app.get('/login')
async def google_auth(request: Request):
    auth = GAuth('./client_secret.json', state=request.cookies.get('session_id'))
    auth_url = await auth.oauth()
    return RedirectResponse(
        auth_url, status_code=302
    )

@app.get('/callback')
async def oauth_callback(request: Request, state: str, code: str, background_tasks: BackgroundTasks):
    auth = GAuth('./client_secret.json', code=code, state=state)
    await auth.get_token()
    user_info = await auth.get_user_info()
    await aprint(f'Debug: user-info {user_info}')

    return templates.TemplateResponse('oauth_ok.html', {"request": request})

async def google_photos_manager(state: str, code: str) -> None:
    """_summary_

    Args:
        state (str): _description_
        code (str): _description_
    """
    await aprint(f'Debug: google-photos-manager {state}, {code}')
    auth = GAuth('./client_secret.json', code=code, state=state)
    token = await auth.get_token()
    await aprint(f'Debug: token -> {token.access_token}')
    # refresh_token = await auth.refresh()
    # await aprint(f'Debug: refreshed token -> {refresh_token.access_token}')
    user_info = await auth.get_user_info()
    await aprint(f'Debug: get user info: {user_info}')

    # filters = {
    #     'dateFilter': {
    #         'ranges': [{
    #             'startDate': {
    #                 'year': 2023,
    #                 'month': 10,
    #                 'day': 1
    #             },
    #             'endDate': {
    #                 'year': 2023,
    #                 'month': 10,
    #                 'day': 31
    #             }
    #         }]
    #     }
    # }
    # photo = GPhoto(auth.http_client, auth.token.access_token)
    # nextPageToken = ''
    # while True:
    #     err, nextPageToken, mediaItems = await photo.search_images(nextPageToken, filters)
    #     await aprint(f'Debug search-images result: {err} {nextPageToken}')
    #     for mi in mediaItems:
    #         await aprint(mi)

    #         url = mi.base_url
    #         if 'video' in mi.mime_type:
    #             url = f'{url}=dv'
    #         else:
    #             # original size with all the Exif metadata except the location metadata
    #             url = f'{url}=w{mi.media_meta_data.width}-h{mi.media_meta_data.height}-d'
            
    #         err, data = await photo.download(url)
    #         if err:
    #             await aprint(f'Error download: {err} {url}')
    #         else:
    #             await aprint(f'Downloaded {mi.filename} {len(data)}')
    #             with open(f'/Users/minyakonga/Downloads/gphotos/{mi.filename}', 'wb') as f:
    #                 f.write(data)

    #     if not nextPageToken:
    #         break

