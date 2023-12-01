import json
from typing import List
import uuid
import webbrowser

from httpx import AsyncClient
from aioconsole import aprint
from config import GOOGLE_OAUTH_API, GOOGLE_OAUTH_BASE
from http_util import HttpProxy


class ClientConfig:
    def __init__(
            self, client_id: str, project_id: str, auth_uri: str,
            token_uri: str, auth_provider_x509_cert_url: str,
            client_secret: str, redirect_uris: List[str],
    ) -> None:
        self.client_id = client_id
        self.project_id = project_id
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        self.auth_provider_x509_cert_url = auth_provider_x509_cert_url
        self.client_secret = client_secret
        self.redirect_uris = redirect_uris

class Token:
    def __init__(
            self, access_token: str, refresh_token: str, token_type: str,
            expires_at: int, scopes: List[str]
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expire_at = expires_at
        self.token_type = token_type
        self.scopes = scopes

class GAuth:
    def __init__(
            self, client_json: str,  code: str='',
            state: str=uuid.uuid4().hex
        ) -> None:
        self.client_json = client_json
        self.scopes = [
            'https://www.googleapis.com/auth/photoslibrary.readonly'
        ]
        self.client_config = self.__load_client_config()
        self.state = state
        self.code = code
    
    def __load_client_config(self) -> ClientConfig:
        """_summary_

        Returns:
            ClientConfig: _description_
        """
        with open(self.client_json, 'r') as f:
            cc_dict = json.load(f).get('installed', {})
            return ClientConfig(
                client_id=cc_dict.get('client_id', ''),
                project_id=cc_dict.get('project_id', ''),
                auth_uri=cc_dict.get('auth_uri', ''),
                token_uri=cc_dict.get('token_uri', ''),
                auth_provider_x509_cert_url=cc_dict.get('auth_provider_x509_cert_url', ''),
                client_secret=cc_dict.get('client_secret', ''),
                redirect_uris=cc_dict.get('redirect_uris', [])
            )

    async def __generate_auth_url(self) -> str:
        """generate auth url

        Returns:
            str: _description_
        """
        return GOOGLE_OAUTH_API.format(
            GOOGLE_OAUTH_BASE=GOOGLE_OAUTH_BASE,
            client_id=self.client_config.client_id,
            redirect_uri=self.client_config.redirect_uris[0],
            scope=' '.join(self.scopes),
            state=self.state,
        )

    async def oauth(self) -> str:
        """do the oauth and return the authorized client that will be used
        in following request

        Returns:
            str: _description_
        """
        auth_url = await self.__generate_auth_url()
        webbrowser.open(auth_url, new=0, autoraise=True)
        await aprint('Please finish the oauth2.0 verification in the browser')
        return auth_url

    async def get_token(self) -> Token:
        """_summary_

        Returns:
            Token: _description_
        """
        await HttpProxy.get()
        pass

    async def refresh(self) -> AsyncClient:
        """nomarlly oauth token will expire in 1 hour, thus need refresh this token

        Returns:
            AsyncClient: _description_
        """
        pass
