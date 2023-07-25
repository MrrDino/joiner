import requests

from loguru import logger
from requests.adapters import HTTPAdapter, Retry


def send_request(url: str, token: str, proxy: str = None, proxy_type: str = "http") -> bool:
    """Функция отправки запроса"""

    _exit = False
    result = False
    attempts = 1
    client = requests.Session()

    client.headers = generate_headers(token=token)
    retries = Retry(
        total=15,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    client.mount('http://', HTTPAdapter(max_retries=retries))

    if proxy:
        proxies = dict(http=f"{proxy_type}://{proxy}", https=f"{proxy_type}://{proxy}")
        client.proxies = proxies

    request = client.prepare_request(
        requests.Request(method="POST", url=url, json={})
    )

    while not _exit:
        try:
            response = client.send(request=request)

            if response.status_code == 200:
                result, _exit = True, True
            else:
                raise Exception
        except Exception as err:
            logger.error(err)
            attempts += 1

            if attempts > 5:
                _exit = True

    return result


def generate_headers(token: str) -> dict:
    """Функция создания HEADERS"""

    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijk4OTkxOTY0NTY4MTE4ODk1N'
                                'CIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5OTAzMTc0ODgxNzg4NjgyMjQiLCJsb2NhdGlvbl9jaGFubmVsX3'
                                'R5cGUiOjB9',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJ'
                              'mciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4Nj'
                              'Q7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyL'
                              'jAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJl'
                              'cl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3R'
                              'hYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM2MjQwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com',
        'Cookie': '__dcfduid=21183630021f11edb7e89582009dfd5e; __sdcfduid=21183631021f11edb7e89582009dfd5ee4936758ec8'
                  'c8a248427f80a1732a58e4e71502891b76ca0584dc6fafa653638; locale=en-US',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    return headers


