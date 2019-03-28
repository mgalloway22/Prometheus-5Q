from assistant import Assistant
from datetime import datetime, timedelta
from errors import (AssistantError,
                    ConnectionFailedError,
                    NoInternetError,
                    StateNotFoundError,
                    ValueNotFoundError)
from requests import exceptions as requests_exceptions, get, Response
from settings import COLORS, IS_DEBUG_MODE
from typing import Dict, List
from urllib3 import exceptions as url_exceptions
from yaml import load


class YamlAssistant(Assistant):
    """An assistant designed to monitor a yaml file at a given URL

    This assistant will parse a yaml file at a given URL and determine if the
    value for the given arguments has changed since the assistant began. For
    example, this can be useful for checking if a version number on a hosted
    pubspec.txt file

    NOTE: The arguments must match the yaml file exactly to work correctly.
    Additionally, the list of arguments must lead to a single value. For
    example:
    ```
    arguments: List[str] = ['packages', 'product_b', 'version']
    ```
    would match this yaml file:
    ```
    packages:
        product_a:
            description:
                name: name_a
                url: url_a
            version: version_a
        product_b:
            description:
                name: name_b
                url: url_b
            version: version_b
        product_c:
            description:
                name: name_c
                url: url_c
            version: version_c
    ```
    and return `version_b` as the current value

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        yaml_url (str): url where the yaml file can be found
        arguments (List[str]): List of arguments for the yaml file
        notification_duration (int): minutes the notification should persist
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 yaml_url: str,
                 arguments: List[str],
                 notification_duration: int):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.yaml_url: str = yaml_url
        self.arguments: List[str] = arguments
        self.notification_duration: int = notification_duration
        self._most_recent_version: str = ''
        self._most_recent_version_time: datetime
        self.UNREAD_VERSION: str = 'unread version'
        self.READ_VERSION: str = 'read version'

    def state_identifier(self) -> str:
        try:
            current_version: str = self._get_current_version()
            if self._most_recent_version == '':
                # if no version was found before this version, we are going to
                # assume the first version found is NOT new
                self._most_recent_version = current_version
                self._most_recent_version_time = (
                        datetime.utcnow() -
                        timedelta(minutes=self.notification_duration)
                    )
                return self.READ_VERSION
            else:
                if current_version == self._most_recent_version:
                    now: datetime = datetime.utcnow()
                    diff: timedelta = now - self._most_recent_version_time
                    diff_in_minutes: float = diff / timedelta(minutes=1)
                    if diff_in_minutes > self.notification_duration:
                        return self.READ_VERSION
                    else:
                        return self.UNREAD_VERSION
                else:
                    self._most_recent_version = current_version
                    self._most_recent_version_time = datetime.utcnow()
                    return self.UNREAD_VERSION
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.READ_VERSION: COLORS['light blue'],
            self.UNREAD_VERSION: COLORS['purple']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.READ_VERSION: ('Value at ' + str(self.yaml_url) +
                                ' remains at ' +
                                str(self._most_recent_version)),
            self.UNREAD_VERSION: ('Value at ' + str(self.yaml_url) + ' has ' +
                                  'changed to ' +
                                  str(self._most_recent_version))
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')

    def _get_current_version(self) -> str:
        try:
            response: Response = get(self.yaml_url)
            if not response.ok:
                raise ConnectionFailedError(self.name,
                                            'GET',
                                            response.status_code)
            value: Dict[str, str] = load(response.text)
            for argument in self.arguments:
                next = value[argument]
                if (isinstance(next, str)):
                    return next
                elif (isinstance(next, Dict)):
                    value = next
                else:
                    break
            raise YamlArgumentError(self.name)
        except (requests_exceptions.ConnectionError,
                url_exceptions.NewConnectionError):
            raise NoInternetError(self.name)


class YamlArgumentError(AssistantError):
    """Raised when a the provided arguemnts did not match the provided yaml file

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The arguments provided did not match the ' +
                  'provided yaml file')
