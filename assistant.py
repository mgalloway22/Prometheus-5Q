from errors import (AssistantError,
                    ConnectionFailedError,
                    NoSignalError,
                    OverrideError,
                    DasApplicationNotRunningError)
from json import dumps, loads
from requests import (exceptions as requests_exceptions,
                      get,
                      post,
                      Response)
from settings import BASE_URL, COLORS, HEADERS, PID
from threading import Thread
from time import sleep
from typing import Dict
from urllib3 import exceptions as url_exceptions


class Assistant:
    """An abstract base class for a Das Keyboard 5Q assistant

    NOTE: The following three methods must be overridden for the assistant to
    function correctly:
    ```
    state_identifier() -> str
    message_identifier(state: str) -> str
    color_identifier(state: str) -> str
    ```

    NOTE: Additionally, is a public method for initiating the binding
    `create_binding()` Otherwise, all other methods are considered private and
    should NOT be used externally

    NOTE: Only use `__init__` to set variables, do not delay the driver by
    evaluating any complex logic

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message

    TODO: When DAS API implements `isMuted`, have the `isMuted` variable use
    the DAS API isMuted
    """
    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool):
        self.name: str = name
        self.delay: int = delay
        self.zone_id: str = zone_id
        self.is_muted: bool = is_muted
        self._ERROR_MESSAGE: str = name + ' is in an unknown state'
        self._ERROR_COLOR: str = COLORS['error']

    def state_identifier(self) -> str:
        """Identify the state that will then be used to identify color and message

        This method should take no arguments, any additional information
        needed by the assistant should be passed into the constructor

        NOTE: If this method is not overriden, an `OverrideError` will be
        raised

        """
        raise OverrideError(self.name, 'state')

    def message_identifier(self, state: str) -> str:
        """Using only the state, manufacture the message that will display

        This method should take only this one argument, any additional
        information needed by the assistant should be passed into the
        constructor

        NOTE: If this method is not overriden, an `OverrideError` will be
        raised

        Arguments:
            state (str): the current state of the assistant
        """
        raise OverrideError(self.name, 'message')

    def color_identifier(self, state: str) -> str:
        """Using only the state, identify the color that will illuminate

        This method should take only this one argument, any additional
        information needed by the assistant should be passed into the
        constructor

        NOTE: If this method is not overriden, an `OverrideError` will be
        raised

        Arguments:
            state (str): the current state of the assistant
        """
        raise OverrideError(self.name, 'color')

    def create_binding(self):
        """Binds the assistant to `self.zone_id` and set every `self.delay`

        NOTE: A value evaluator thread is spawned and then the assistant calls
        `sleep(self.delay)`
        """
        while 1:
            try:
                Thread(target=self._evaluate_values).start()
                sleep(self.delay)
            except KeyboardInterrupt:
                return

    def _get_all_signals(self) -> Dict[str, str]:
        """
        NOTE: The following commented implementation seems to have an issue
        since the Das API sometimes responds with the incorrect zone info

        url = BASE_URL + '/pid/'+ PID + '/zoneId/' + self.zone_id
        response = get(url, headers=HEADERS)
        """
        url: str = BASE_URL + '/shadows'
        try:
            response: Response = get(url, headers=HEADERS)
        except (requests_exceptions.ConnectionError,
                url_exceptions.NewConnectionError):
            e: DasApplicationNotRunningError = (
                DasApplicationNotRunningError(self.name))
            e.elaborate()
            exit()
        if response.ok:
            for signal in loads(response.content):
                if signal['zoneId'] == self.zone_id:
                    return signal
            raise NoSignalError(self.name, self.zone_id)
        else:
            raise ConnectionFailedError(self.name,
                                        'GET',
                                        response.status_code)

    def _set_values_if_changed(self,
                               color: str,
                               message: str,
                               is_blinking: bool = False):
        all_values: Dict[str, str]
        try:
            all_values = self._get_all_signals()
        except ConnectionFailedError:
            raise
        except NoSignalError as e:
            e.elaborate()
            self._set_values(color, message, is_blinking)
            return
        current_color: str = all_values['color']
        current_message: str = all_values['message']
        if current_color != color or current_message != message:
            self._set_values(color, message, is_blinking)

    def _set_values(self,
                    color: str,
                    message: str,
                    is_blinking: bool = False):
        set_color_request: Dict[str, str] = {
            'pid': PID,
            'zoneId': self.zone_id,
            'color': color,
            'message': message,
            'name': self.name,
            'effect': 'BLINK' if is_blinking else 'SET_COLOR'
        }
        try:
            response: Response = post(BASE_URL,
                                      data=dumps(set_color_request),
                                      headers=HEADERS)
        except (requests_exceptions.ConnectionError,
                url_exceptions.NewConnectionError):
            e: DasApplicationNotRunningError = (
                DasApplicationNotRunningError(self.name))
            e.elaborate()
            exit()
        if not response.ok:
            raise ConnectionFailedError(self.name,
                                        'POST',
                                        response.status_code)

    def _set_error_if_changed(self):
        self._set_values_if_changed(self._ERROR_COLOR,
                                    self._ERROR_MESSAGE,
                                    True)

    def _evaluate_values(self):
        try:
            state: str = self.state_identifier()
            color: str = self.color_identifier(state)
            message: str = self.message_identifier(state)
        except AssistantError as e:
            e.elaborate()
            self._set_error_if_changed()
            return
        self._set_values_if_changed(color,
                                    '' if self.is_muted else message,
                                    False)
