from assistant import Assistant
from psutil import AccessDenied, NoSuchProcess, process_iter
from errors import ValueNotFoundError
from settings import COLORS
from typing import Dict


class CPUAssistant(Assistant):
    """An assistant designed calculate the total CPU percent of a process

    Between each `delay`, the assistant records how much total usage across all
    processes that CONTAIN the `process_name` (case insensitve) If this amount
    is greater than 0, the state is set to `ON`. If this amount across all
    processes is 0, the state is set to `OFF`

    NOTE: If no processes are found to match the given `process_name`, the
    state wiill be set to `OFF`
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 process_name: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.process_name: str = process_name
        self.OFF: str = 'off'
        self.ON: str = 'on'

    def state_identifier(self) -> str:
        try:
            for process in process_iter():
                if (self.process_name.lower() in process.name().lower() and
                   process.cpu_percent(interval=self.delay) > 0):
                    return self.ON
            return self.OFF
        except (AccessDenied, NoSuchProcess):
            return self.OFF

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.OFF: COLORS['red'],
            self.ON: COLORS['light green']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.OFF: self.name + ' has turned off',
            self.ON: self.name + ' has turned on'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
