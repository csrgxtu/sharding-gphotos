import json
from typing import List, Union
import time
import uuid
import webbrowser

from httpx import AsyncClient
from aioconsole import aprint
from config import *
from http_util import HttpProxy
from errors import Exceptions


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
    # ref https://developers.google.com/identity/protocols/oauth2/web-server#httprest_1
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
        self.http_client = AsyncClient(
            proxies={
                'http://': 'socks5://127.0.0.1:1080',
                'https://': 'socks5://127.0.0.1:1080',
            }
        )
        self.token = None
    
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
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_config.client_id,
            'client_secret': self.client_config.client_secret,
            'code': self.code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.client_config.redirect_uris[0]
        }
        err, data = await HttpProxy.post(
            self.http_client, GOOGLE_OAUTH_TOKEN, headers=headers, data=data
        )
        if err == Exceptions.DependencyError:
            return None
        
        res = json.loads(data)
        self.token = Token(
            access_token=res.get('access_token'),
            refresh_token=res.get('refresh_token'),
            token_type=res.get('token_type'),
            expires_at=res.get('expires_at'),
            scopes=res.get('scopes')
        )
        return self.token

    async def refresh(self) -> Token:
        """nomarlly oauth token will expire in 1 hour, thus need refresh this token

        Returns:
            Token: _description_
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_config.client_id,
            'client_secret': self.client_config.client_secret,
            'refresh_token': self.token.refresh_token,
            'grant_type': 'refresh_token'
        }
        err, data = await HttpProxy.post(
            self.http_client, GOOGLE_OAUTH_TOKEN, headers=headers, data=data
        )
        if err == Exceptions.DependencyError:
            return None
        
        res = json.loads(data)
        self.token = Token(
            access_token=res.get('access_token'),
            refresh_token=self.token.refresh_token,
            token_type=res.get('token_type'),
            expires_at=time.time() + res.get('expires_in'),
            scopes=res.get('scopes')
        )
        return self.token

class MediaItem:
    def __init__(self) -> None:
        pass
class GPhoto:
    def __init__(self, client: AsyncClient, token: str) -> None:
        self.http_client = client
        self.token = token

    async def search_images(self, nextPageToken: str, filters: dict={}) -> Union[str, str, List[MediaItem]]:
        """_summary_

        Args:
            nextPageToken (str): _description_
            filters (dict, optional): _description_. Defaults to {}.

        Returns:
            Union[str, str, List[MediaItem]]: _description_
        """
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        json_data = {
            'pageSize': 1,
            'pageToken': nextPageToken,
            'filters': filters
        }
        nextPageToken, mediaItems = '', []

        err, data = await HttpProxy.post(
            self.http_client, GOOGLE_PHOTO_SEARCH, headers=headers, json=json_data
        )
        if err == Exceptions.DependencyError:
            return err,  nextPageToken, mediaItems
        
        res = json.loads(data)
        await aprint(f'Debug: {res.get("mediaItems")[0]}')
        await aprint(f'Fuck d d    ')
        nextPageToken = res.get('nextPageToken')
        for mi in res.get('mediaItems'):
            mediaItems.append(MediaItem(

            ))

        return Exceptions.OK, nextPageToken, mediaItems