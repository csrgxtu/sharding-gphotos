from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import RedirectResponse
from aioconsole import aprint
from gauth import GAuth, GPhoto

app = FastAPI()

@app.get('/')
async def google_auth():
    auth = GAuth('./client_secret.json')
    auth_url = await auth.oauth()
    return RedirectResponse(
        auth_url, status_code=301
    )

@app.get('/callback')
async def oauth_callback(state: str, code: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(google_photos_manager, state, code)
    return {'ok': True}

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
    filters = {
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
    photo = GPhoto(auth.http_client, auth.token.access_token)
    nextPageToken = ''
    while True:
        err, nextPageToken, mediaItems = await photo.search_images(nextPageToken, filters)
        await aprint(f'Debug search-images result: {err} {nextPageToken}')
        for mi in mediaItems:
            await aprint(mi)
        if not nextPageToken:
            break

