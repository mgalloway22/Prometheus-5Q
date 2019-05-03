from assistant import Assistant
from errors import (AssistantError,
                    NoInternetError,
                    StateNotFoundError,
                    ValueNotFoundError)
from jenkins import Jenkins, JenkinsException
from requests import exceptions as requests_exceptions
from settings import COLORS, IS_DEBUG_MODE
from typing import Dict
from urllib3 import exceptions as url_exceptions


class JenkinsAssistant(Assistant):
    """An assistant desgined to check the most recent build status of a Jenkins job

    NOTE: Make sure to specify a port in the server url if needed, ex.
    https://server.example.com/jenkins:8080

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        job_name (str): the name of the desired jenkins job to check
        server_url (str): the url of the jenkins server (including port)
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 job_name: str,
                 server_url: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.job_name: str = job_name
        self.server_url: str = server_url

    def _contact_jenkins_server(self) -> str:
        try:
            server: Jenkins = Jenkins(self.server_url)
            last_build_number: int = (server.get_job_info(self.job_name)
                                      ['lastBuild']['number'])
            return (server.get_build_info(self.job_name, last_build_number)
                    ['result'])
        except JenkinsException:
            raise StateNotFoundError(self.name)
        except (requests_exceptions.ConnectionError,
                url_exceptions.NewConnectionError):
            raise NoInternetError(self.name)

    def state_identifier(self) -> str:
        try:
            return self._contact_jenkins_server()
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            'SUCCESS': COLORS['light green'],
            'FAILURE': COLORS['red'],
            'UNSTABLE': COLORS['yellow']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            'SUCCESS': 'was successful',
            'FAILURE': 'failed',
            'UNSTABLE': 'was unstable'
        }
        if state in message_switcher:
            return (self.name + ': the last build ' +
                    message_switcher[state])
        else:
            raise ValueNotFoundError(self.name, state, 'message')


class JenkinsError(AssistantError):
    """Raised when the desired jenkins last build info cannot be found

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The build info for the jenkins job cannot ' +
                  'be found, please verify the server url and job name are ' +
                  'correct')
