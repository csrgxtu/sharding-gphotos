from typing import Union
import time
import aiohttp
# from httpx import AsyncClient
from aioconsole import aprint
from errors import Exceptions

class HttpProxy:
    @classmethod
    async def post(cls, client: aiohttp.ClientSession, url: str, headers: dict, data: dict={}, json: dict={}) -> Union[str, bytes]:
        """_summary_

        Args:
            client (aiohttp.ClientSession): _description_
            url (str): _description_
            headers (dict): _description_
            data (dict, optional): _description_. Defaults to {}.
            json (dict, optional): _description_. Defaults to {}.

        Returns:
            Union[str, bytes]: _description_
        """
        ts = int(time.time() * 1000)
        if data:
            post = client.post(url, headers=headers, data=data)
        else:
            post = client.post(url, headers=headers, json=json)
        
        async with post as res:
            content = await res.read()
            await aprint(f'POST {url} with {headers} {data} {json} -> {int(time.time() * 1000) - ts}ms {res.status} {content[0:32]}...')
            if res.status == 200:
                return Exceptions.OK, content

        return Exceptions.DependencyError, ""

    @classmethod
    async def get(cls, client: aiohttp.ClientSession, url: str, headers: dict) -> Union[str, bytes]:
        """_summary_

        Args:
            client (aiohttp.ClientSession): _description_
            url (str): _description_
            headers (dict): _description_

        Returns:
            Union[str, bytes]: _description_
        """
        ts = int(time.time() * 1000)
        try:
            async with client.get(url, headers=headers, allow_redirects=True) as res:
                content = await res.read()
                await aprint(f'GET {url[0:32]}... with {headers} -> {int(time.time() * 1000) - ts}ms {res.status} {content[0:32]}...')
                if res.status == 200:
                    return Exceptions.OK, content
        except TimeoutError as ex:
            await aprint(f'timeout {int(time.time() * 1000) - ts} ms')
            raise ex
        
        return Exceptions.DependencyError, ""


    # @classmethod
    # async def post(cls, client: AsyncClient, url: str, headers: dict, data: dict={}, json: dict={}) -> Union[str, bytes]:
    #     """_summary_

    #     Args:
    #         client (AsyncClient): _description_
    #         url (str): _description_
    #         headers (dict): _description_

    #     Returns:
    #         Union[str, bytes]: _description_
    #     """
    #     ts = int(time.time() * 1000)
    #     res = await client.post(url, headers=headers, data=data, json=json)
    #     await aprint(f'POST {url} with {headers} {data} {json} -> {int(time.time() * 1000) - ts}ms {res.status_code} {res.content[0:32]}...')
    #     if res.status_code == 200:
    #         return Exceptions.OK, res.content

    #     return Exceptions.DependencyError, ""

    # @classmethod
    # async def get(cls, client: AsyncClient, url: str, headers: dict, timeout: int) -> Union[str, bytes]:
    #     """_summary_

    #     Args:
    #         client (AsyncClient): _description_
    #         url (str): _description_
    #         headers (dict): _description_
    #         timeout (int): _description_


    #     Returns:
    #         Union[str, bytes]: _description_
    #     """
    #     ts = int(time.time() * 1000)
    #     res = await client.get(url, headers=headers, follow_redirects=True, timeout=timeout)
    #     await aprint(f'GET {url[0:32]}... with {headers} -> {int(time.time() * 1000) - ts}ms {res.status_code} {res.content[0:32]}...')
    #     if res.status_code == 200:
    #         return Exceptions.OK, res.content
    #     return Exceptions.DependencyError, ""
