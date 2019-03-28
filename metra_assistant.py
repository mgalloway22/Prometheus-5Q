from assistant import Assistant
from errors import (AssistantError,
                    ConnectionFailedError,
                    NoInternetError,
                    StateNotFoundError,
                    ValueNotFoundError)
from json import loads
from requests import exceptions as requests_exceptions, Session, Response
from settings import COLORS, IS_DEBUG_MODE
from typing import Dict
from urllib3 import exceptions as url_exceptions


class MetraAssistant(Assistant):
    """An assistant designed to notify if there are alerts for a given route_id

    NOTE: For more information: https://metrarail.com/developers/metra-gtfs-api

    NOTE: This assistant uses Metra's API and requires that an `access_key` and
    `secret_key` be generated from them

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        access_key (str): access key granted by Metra
        secret_key (str): secret key granted by Metra
        route_id (str): id of the route to track
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 access_key: str,
                 secret_key: str,
                 route_id: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.access_key: str = access_key
        self.secret_key: str = secret_key
        self.route_id: str = route_id
        self.num_alerts: int = 0
        self.READ_ALERT: str = 'read alert'
        self.UNREAD_ALERT: str = 'unread alert'

    def _get_amount_of_alerts(self, response_content: str) -> int:
        total: int = 0
        try:
            for data in loads(response_content):
                is_deleted: bool = data['is_deleted']
                if not is_deleted:
                    for informed_entity in data['alert']['informed_entity']:
                        if ('route_id' in informed_entity
                           and informed_entity['route_id'] is not None
                           and informed_entity['route_id'] == self.route_id):
                            total += 1
                        elif ('trip' in informed_entity
                              and informed_entity['trip'] is not None
                              and informed_entity['trip']['route_id'] ==
                              self.route_id):
                            total += 1
            return total
        except KeyError:
            raise MetraAPIResponseError(self.name)

    def _set_amount_of_alerts(self):
        url = 'https://gtfsapi.metrarail.com/gtfs/alerts'
        session: Session = Session()
        session.auth = (self.access_key, self.secret_key)
        try:
            response: Response = session.get(url)
            if response.ok:
                self.num_alerts = self._get_amount_of_alerts(response.content)
            else:
                raise ConnectionFailedError(self.name,
                                            'GET',
                                            response.status_code)
        except (requests_exceptions.ConnectionError,
                url_exceptions.NewConnectionError):
            raise NoInternetError(self.name)

    def state_identifier(self) -> str:
        try:
            self._set_amount_of_alerts()
            if self.num_alerts > 0:
                return self.UNREAD_ALERT
            else:
                return self.READ_ALERT
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.READ_ALERT: COLORS['light blue'],
            self.UNREAD_ALERT: COLORS['yellow']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.READ_ALERT: ('There are no new alerts on ' + self.route_id),
            self.UNREAD_ALERT: (
                ('There is 1 new alert on  ' + self.route_id)
                if self.num_alerts == 1 else
                ('There are ' + str(self.num_alerts) +
                 ' new alerts on ' + self.route_id))
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')


class MetraAPIResponseError(AssistantError):
    """Raised when json response from the MetraAPI was not as expected

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The json response from the MetraAPI was ' +
                  'not as expected')
