
import json
from typing import List

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

    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )

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

    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )


class MediaMetaDataPhoto:
    def __init__(
            self, camera_make: str, camera_model: str, focal_length: float,
            aperture_fnumber: float, iso_equivalent: int, exposure_time: str 
    ) -> None:
        self.camera_make = camera_make
        self.camera_model = camera_model
        self.focal_length = focal_length
        self.aperture_fnumber = aperture_fnumber
        self.iso_equivalent = iso_equivalent
        self.exposure_time = exposure_time
    
    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )

class MediaMetaDataVideo:
    def __init__(
            self, fps: int, status: str
    ) -> None:
        self.fps = fps
        self.status = status

    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )

class MediaMetaData:
    def __init__(
            self, create_time: str, width: str, height: str,
            photo: MediaMetaDataPhoto=None, video: MediaMetaDataVideo=None
    ) -> None:
        self.create_time = create_time
        self.width = width
        self.height = height
        self.photo = photo
        self.video = video

    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )

class MediaItem:
    def __init__(
            self, media_id: str, product_url: str, base_url: str,
            mime_type: str, media_meta_data: MediaMetaData, filename: str
    ) -> None:
        self.media_id = media_id
        self.product_url = product_url
        self.base_url = base_url
        self.mime_type = mime_type
        self.media_meta_data = media_meta_data
        self.filename = filename

    def __repr__(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )