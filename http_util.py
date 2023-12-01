import httpx
from typing import Union
from errors import Exceptions

class HttpProxy:
    @classmethod
    async def get(self, url: str, headers: dict, cookies: dict) -> Union[str, bytes]:
        """get method, download url source code

        Args:
            url (str): _description_
            headers (dict): _description_
            cookies (dict): _description_

        Returns:
            Union[str, bytes]: err-msg, content
        """
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers, cookies=cookies)
            if res.status_code == 200:
                return Exceptions.OK, res.content
            
            return Exceptions.DependencyError, ""
