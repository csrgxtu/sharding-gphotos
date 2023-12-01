from typing import Union
from httpx import AsyncClient
from aioconsole import aprint
from errors import Exceptions

class HttpProxy:
    @classmethod
    async def post(cls, client: AsyncClient, url: str, headers: dict, data: dict={}, json: dict={}) -> Union[str, bytes]:
        """_summary_

        Args:
            client (AsyncClient): _description_
            url (str): _description_
            headers (dict): _description_

        Returns:
            Union[str, bytes]: _description_
        """
        res = await client.post(url, headers=headers, data=data, json=json)
        await aprint(f'POST {url} with Headers->{headers} data->{data} json->{json} {res.status_code} {res.content}')
        if res.status_code == 200:
            return Exceptions.OK, res.content

        return Exceptions.DependencyError, ""
