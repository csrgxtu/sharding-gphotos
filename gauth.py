import json
from typing import List, Union
import time
import uuid
import webbrowser

import aiohttp
from aiohttp_socks import ProxyConnector
from aioconsole import aprint
from config import *
from http_util import HttpProxy
from errors import Exceptions
from model import *


class GAuth:
    # ref https://developers.google.com/identity/protocols/oauth2/web-server#httprest_1
    def __init__(
            self, client_json: str,  code: str='',
            state: str=uuid.uuid4().hex
        ) -> None:
        self.client_json = client_json
        self.scopes = [
            'https://www.googleapis.com/auth/photoslibrary.readonly',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
        self.client_config = self.__load_client_config()
        self.state = state
        self.code = code

        self.http_client = aiohttp.ClientSession(
            connector=ProxyConnector.from_url('socks5://127.0.0.1:1080')
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
        await aprint('Please finish the oauth2.0 verification in the browser')
        return auth_url

    async def get_user_info(self) -> GmailUserInfo:
        """get user basic info

        Returns:
            GmailUserInfo: _description_
        """
        headers = {}
        url = GOOGLE_USER_INFO.format(access_token=self.token.access_token)
        err, data = await HttpProxy.get(
            self.http_client, url, headers=headers
        )
        if err == Exceptions.DependencyError:
            return None
        
        res = json.loads(data)
        return GmailUserInfo(
            email=res.get('email'),
            pic=res.get('picture'),
            verified=res.get('verified_email'),
            uid=res.get('id')
        )

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

class GPhoto:
    def __init__(self, client: aiohttp.ClientSession, token: str) -> None:
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
            'pageSize': 16,
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
        nextPageToken = res.get('nextPageToken')
        for mi in res.get('mediaItems'):
            photo, video = None, None
            if 'video' in mi.get('mimeType'):
                video = MediaMetaDataVideo(
                    fps=mi.get('mediaMetadata').get('video').get('fps'),
                    status=mi.get('mediaMetadata').get('video').get('status')
                )
            else:
                photo = MediaMetaDataPhoto(
                    camera_make=mi.get('mediaMetadata').get('photo').get('cameraMake'),
                    camera_model=mi.get('mediaMetadata').get('photo').get('cameraModel'),
                    focal_length=mi.get('mediaMetadata').get('photo').get('focalLength'),
                    aperture_fnumber=mi.get('mediaMetadata').get('photo').get('apertureFNumber'),
                    iso_equivalent=mi.get('mediaMetadata').get('photo').get('isoEquivalent'),
                    exposure_time=mi.get('mediaMetadata').get('photo').get('exposureTime')
                )
            mediaItems.append(MediaItem(
                media_id=mi.get('id'),
                product_url=mi.get('productUrl'),
                base_url=mi.get('baseUrl'),
                mime_type=mi.get('mimeType'),
                filename=mi.get('filename'),
                media_meta_data=MediaMetaData(
                    create_time=mi.get('mediaMetadata').get('creationTime'),
                    width=mi.get('mediaMetadata').get('width'),
                    height=mi.get('mediaMetadata').get('height'),
                    photo=photo,
                    video=video
                )
            ))

        return Exceptions.OK, nextPageToken, mediaItems

    async def download(self, url: str) -> Union[str, bytes]:
        """download image/video from google

        Args:
            url (str): _description_

        Returns:
            Union[str, bytes]: _description_
        """
        # headers = {"Connection": "close"}
        return await HttpProxy.get(
            self.http_client, url, headers={}
        )
