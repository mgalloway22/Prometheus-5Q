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
        self.LOW: str = 'low'
        self.MEDIUM: str = 'medium'
        self.HIGH: str = 'high'

    def state_identifier(self) -> str:
        try:
            for process in process_iter():
                if self.process_name.lower() in process.name().lower():
                    cpu_pct: float = process.cpu_percent(interval=self.delay)
                    if cpu_pct is None or  0.0 < cpu_pct <= 50.0:
                        return self.LOW
                    elif 50.0 < cpu_pct <= 100.0:
                        return self.MEDIUM
                    elif 100.0 < cpu_pct:
                        return self.HIGH
            return self.OFF
        except (AccessDenied, NoSuchProcess):
            return self.OFF

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.OFF: COLORS['red'],
            self.LOW: COLORS['orange'],
            self.MEDIUM: COLORS['yellow'],
            self.HIGH: COLORS['light green']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.OFF: self.name + ' has turned off',
            self.LOW: self.name + ' is running (low)',
            self.MEDIUM: self.name + ' is running (medium)',
            self.HIGH: self.name + ' is running (high)'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
