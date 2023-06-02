import json
import logging
import os
import requests

from dotenv import load_dotenv
from json.decoder import JSONDecodeError

class Prefecture():
    def __init__(self, code: int, name: str):
        self.code: int = code
        self.name: str = name

class City():
    def __init__(self, code: int, name: str):
        self.code: int = code
        self.name: str = name

def set_notion_headers():
    return {
        'Authorization': f"Bearer {os.getenv(key = 'NOTION_API_KEY')}",
        'accept': 'application/json',
        'content-type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

def check_prefecture_page(prefecture: Prefecture) -> int:
    response = requests.post(
        url = f"https://api.notion.com/v1/databases/{os.getenv(key = 'NOTION_PREFECTURE_DB')}/query",
        headers = set_notion_headers(),
        json = {
            'page_size': 100,
            'filter': {
                'and': [
                    {
                        'property': '都道府県コード',
                        'number': {'equals': prefecture.code}
                    },
                    {
                        'property': '都道府県名',
                        'rich_text': {'equals': prefecture.name}
                    }
                ]
            }
        },
    )

    if response.status_code != 200:
        response = json.loads(response.text)
        logging.warning(msg = f'［{prefecture.code} × {prefecture.name}］のレコード検索時にエラーが発生しました。')
        logging.warning(msg = f"ステータスコード: {response['status']}，メッセージ: {response['message']}")

    return len(json.loads(response.text)['results'])

def check_city_page(city: City) -> int:
    response = requests.post(
        url = f"https://api.notion.com/v1/databases/{os.getenv(key = 'NOTION_CITY_DB')}/query",
        headers = set_notion_headers(),
        json = {
            'page_size': 100,
            'filter': {
                'and': [
                    {
                        'property': '市区町村コード',
                        'number': {'equals': int(city.code)}
                    },
                    {
                        'property': '市区町村名',
                        'rich_text': {'equals': city.name}
                    }
                ]
            }
        },
    )

    if response.status_code != 200:
        try:
            response = json.loads(response.text)
            logging.warning(msg = f'［{city.code} × {city.name}］のレコード検索時にエラーが発生しました。')
            logging.warning(msg = f"ステータスコード: {response['status']}，メッセージ: {response['message']}")
        except JSONDecodeError:
            # TODO: JSONDecodeError 対応
            logging.warning(msg = response.text)

    return len(json.loads(response.text)['results'])

def get_notion_prefecture_page_id(prefecture):
    response = requests.post(
        url = f"https://api.notion.com/v1/databases/{os.getenv(key = 'NOTION_PREFECTURE_DB')}/query",
        headers = set_notion_headers(),
        json = {
            'page_size': 100,
            'filter': {
                'and': [
                    {
                        'property': '都道府県コード',
                        'number': {'equals': prefecture.code}
                    },
                    {
                        'property': '都道府県名',
                        'rich_text': {'equals': prefecture.name}
                    }
                ]
            }
        },
    )

    if response.status_code != 200:
        response = json.loads(response.text)
        logging.warning(msg = f'［{prefecture.code} × {prefecture.name}］のレコード検索時にエラーが発生しました。')
        logging.warning(msg = f"ステータスコード: {response['status']}，メッセージ: {response['message']}")

    return len(json.loads(response.text)['results'])

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(
        level = logging.INFO,
        format = '[{levelname}]: {message}',
        style = '{'
    )

    prefecture_list: list = json.loads(
        requests.get(
            url = 'https://opendata.resas-portal.go.jp/api/v1/prefectures',
            headers = {
                'content-type': 'application/json;charset=UTF-8',
                'X-API-KEY': os.getenv(key = 'RESAS_API_KEY')
            }
        ).text
    )['result']

    for prefecture in prefecture_list:
        prefecture_object: Prefecture = Prefecture(code = prefecture['prefCode'], name = prefecture['prefName'])

        if check_prefecture_page(prefecture_object) == 0:
            response = requests.post(
                url = 'https://api.notion.com/v1/pages',
                headers = set_notion_headers(),
                json = {
                    'parent': {'database_id': os.getenv(key = 'NOTION_PREFECTURE_DB')},
                    'properties': {
                        '都道府県コード': {'number': prefecture_object.code},
                        '都道府県名': {
                            'title': [{
                                'text': {'content': prefecture_object.name}
                            }]
                        }
                    }
                }
            )

            if response.status_code != 200:
                response = json.loads(response.text)
                logging.warning(msg = f'［{prefecture_object.code} × {prefecture_object.name}］のレコード作成時にエラーが発生しました。')
                    # TODO: 市区町村コード（05463，14111，22301）エラー対応
                logging.warning(msg = f"ステータスコード: {response['status']}，メッセージ: {response['message']}")

            prefecture_page_id: str = get_notion_prefecture_page_id(prefecture_object)
        elif check_prefecture_page(prefecture_object) == 1:
            prefecture_page_id: str = get_notion_prefecture_page_id(prefecture_object)

        city_list: list = json.loads(
            requests.get(
                url = 'https://opendata.resas-portal.go.jp/api/v1/cities',
                params = {'prefCode': prefecture_object.code},
                headers = {
                    'content-type': 'application/json;charset=UTF-8',
                    'X-API-KEY': os.getenv(key = 'RESAS_API_KEY')
                }
            ).text
        )['result']

        index: int = 1
        for city in city_list:
            city_object: City = City(code = city['cityCode'], name = city['cityName'])

            if check_city_page(city_object) == 0:
                response = requests.post(
                    url = 'https://api.notion.com/v1/pages',
                    headers = set_notion_headers(),
                    json = {
                        'parent': {'database_id': os.getenv(key = 'NOTION_CITY_DB')},
                        'properties': {
                            '市区町村コード': {'number': int(city_object.code)},
                            '市区町村名': {
                                'title': [{
                                    'text': {'content': city_object.name}
                                }]
                            },
                            '都道府県コード':{
                                'relation': [{'id': prefecture_page_id}]
                            }
                        }
                    }
                )

                if response.status_code != 200:
                    response = json.loads(response.text)
                    logging.warning(msg = f'［{city_object.code} × {city_object.name}］のレコード作成時にエラーが発生しました。')
                    logging.warning(msg = f"ステータスコード: {response['status']}，メッセージ: {response['message']}")

            index += 1

        logging.info(msg = f'▲ 処理完了: {prefecture_object.name} の処理が終了しました。▲')

    logging.info(msg = '処理が正常に終了しました。')
