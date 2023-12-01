from google_auth_oauthlib.flow import Flow
from httpx import AsyncClient
from aioconsole import aprint


class GAuth:
    def __init__(self, client_json: str) -> None:
        self.client_json = client_json
        self.scopes = [
            'https://www.googleapis.com/auth/photoslibrary.readonly'
        ]

    async def __generate_auth_url(self) -> str:
        """generate auth url

        Returns:
            str: _description_
        """
        flow = Flow.from_client_secrets_file(
            self.client_json, scopes=self.scopes
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url

    async def oauth(self) -> AsyncClient:
        """do the oauth and return the authorized client that will be used
        in following request

        Returns:
            AsyncClient: _description_
        """
        auth_url = await self.__generate_auth_url()
        await aprint('Please go to this URL: {}'.format(auth_url))
        pass

    async def refresh(self) -> AsyncClient:
        """nomarlly oauth token will expire in 1 hour, thus need refresh this token

        Returns:
            AsyncClient: _description_
        """
        pass
