from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import RedirectResponse
from aioconsole import aprint
from gauth import GAuth

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
    pass
