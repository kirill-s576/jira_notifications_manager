import aiohttp
from typing import Optional, List
import urllib.parse


class JiraOAuthAsyncApi:

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scope: List[str]
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scope = scope

    def get_scope_list(self):
        return self._scope

    def get_scope_string(self):
        return "%20".join(self.get_scope_list())

    def get_redirect_uri(self):
        return self._redirect_uri#urllib.parse.quote(self._redirect_uri)

    def get_client_id(self):
        return str(self._client_id)

    def get_client_secret(self):
        return str(self._client_secret)

    def get_auth_uri(self, user_state: str):
        url = f"https://auth.atlassian.com" \
              f"/authorize" \
              f"?" \
              f"audience=api.atlassian.com" \
              f"&client_id={self.get_client_id()}" \
              f"&scope={self.get_scope_string()}" \
              f"&redirect_uri={self.get_redirect_uri()}" \
              f"&state={user_state}" \
              f"&response_type=code" \
              f"&prompt=consent"
        return url

    async def exchange_code_to_jwt(self, code: str):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            payload = {
                "code": code,
                "grant_type": "authorization_code",
                "client_id": self.get_client_id(),
                "client_secret": self.get_client_secret(),
                "redirect_uri": self.get_redirect_uri()
            }
            headers = {
                "Content-Type": "application/json"
            }
            async with session.post(
                    'https://auth.atlassian.com/oauth/token',
                    json=payload,
                    headers=headers
            ) as resp:
                return await resp.json()


class BaseAsyncApi:

    @staticmethod
    async def send_get_request(**kwargs):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(**kwargs) as resp:
                return await resp.json()

    @staticmethod
    async def send_post_request(**kwargs):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(**kwargs) as resp:
                return await resp.json()


class JiraAsyncApi(BaseAsyncApi):

    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        self._access_token = access_token
        self._refresh_token = refresh_token

    def get_auth_header(self) -> dict:
        return {
            "Authorization": f"Bearer {self._access_token}"
        }

    def get_accessible_resources(self) -> List[dict]:
        url = "https://api.atlassian.com/oauth/token/accessible-resources"
        result = await self.send_get_request(
            url=url,
            headers=self.get_auth_header(),
        )
        return result

    @classmethod
    def get_base_url(cls, resource_id: str):
        base_url = f"https://api.atlassian.com/ex/jira/{resource_id}/rest/api/3/"
        return base_url
