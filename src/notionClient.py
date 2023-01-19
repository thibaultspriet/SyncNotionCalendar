import requests
from typing import Dict, List, Tuple
from datetime import datetime
import logging


class Card:
    """This class represents a Notion card as a dict thanks to the `to_dict` method
    """

    def __init__(self, page: Dict) -> None:
        """Constructor
        Data stored :
        - page id
        - page title
        - datetime of last edit
        - start datetime
        - end datetime : if not provided set to start datetime

        Args:
            page (Dict): dict from API call result
        """
        self._id = page['id']
        self.title = page.get('properties').get('Name').get('title')[0].get('plain_text')
        self.last_edited_time = self._convert_datetime(page.get('last_edited_time'))
        (self.start_date, self.start_time) = self._convert_datetime(page.get('properties').get('date').get('date').get('start'))
        (self.end_date, self.end_time) = self._convert_datetime(page.get('properties').get('date').get('date').get('end'))

    def to_dict(self) -> Dict:
        """Returns a representation of the card object as a Dict

        Returns:
            Dict: dict
        """
        _dict = {
            'id': self._id,
            'last_edit': self.last_edited_time,
            'start_date': self.start_date,
            'start_time': self.start_time,
            'end_date': self.end_date,
            'end_time': self.end_time,
            'title': self.title
        }
        return _dict

    def __repr__(self) -> str:
        return f"id : {self._id}\ntitle : {self.title}\nstart : {self.start_date}\nend : {self.end_date}\nlast edit : {self.last_edited_time}"

    def _convert_datetime(self, notion_datetime: str) -> Tuple:
        """Helpher function to normalize datetimes

        Args:
            notion_datetime (str): datetime

        Returns:
            (date, time): (datetime.date, datetime.time)
        """
        if notion_datetime is None:
            return (notion_datetime, notion_datetime)
        tmp = notion_datetime.split('T')
        if len(tmp) == 1:
            fulldt = datetime.strptime(f'{tmp[0]} 00:00:00', '%Y-%m-%d %H:%M:%S')
            return (fulldt.date(), None)
        else:
            time = tmp[1][:8]
            fulldt = datetime.strptime(f'{tmp[0]} {time}', '%Y-%m-%d %H:%M:%S')
            return (fulldt.date(), fulldt.time())


class NotionClient:
    """This class handles calls to the notion API
    """

    def __init__(self, token) -> None:
        """Constructor of the NotionClient object
        It stores the API key as well as some constant parameters needed in API calls
        """
        self._key = token
        self._headers = {
            'Authorization': f'Bearer {self._key}',
            'Notion-Version': '2021-08-16',
        }
        self._base_url = "https://api.notion.com/v1/"

    def get_live_cards(self, database_id: str) -> List[Card]:
        """API call that returns a list of card where the property date is specified.
        Outdated cards are not returned

        Args:
            database_id (str): id of notion database

        Raises:
            Exception: if the API call failed

        Returns:
            List[Card]: list of cards
        """
        has_more = True
        _list_page = []
        start_cursor = None
        _url = f"{self._base_url}databases/{database_id}/query"
        payload = {
            "filter": {
                "property": "date",
                "date": {
                    "on_or_after": datetime.now().strftime("%Y-%m-%d")
                }
            },
        }
        while has_more:
            if start_cursor:
                payload['start_cursor'] = start_cursor
            q = requests.post(_url, headers=self._headers, json=payload)
            try:
                _list_page += q.json()['results']
            except:
                logging.error('while fetching cards on Notion : {q.text}')
                raise Exception(q.text)
            has_more = q.json()['has_more']
            start_cursor = q.json()['next_cursor']
        _list_card = [Card(page) for page in _list_page]
        return _list_card
