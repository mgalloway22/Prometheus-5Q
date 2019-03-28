from assistant import Assistant
from errors import AssistantError, StateNotFoundError, ValueNotFoundError
from settings import COLORS
from typing import Dict


class TemplateAssistant(Assistant):
    """An assistant desgined to ... (one-line summary)

    Optional more lines for summary of assistant...

    NOTE: Anything important that a user should be aware of

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        ...
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.example_state: str = 'example state'

    def state_identifier(self) -> str:
        try:
            # TODO: perform any logic to find the state
            return self.example_state
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.example_state: COLORS['red']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.example_state: 'example state message'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
