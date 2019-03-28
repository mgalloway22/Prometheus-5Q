from assistant import Assistant
from errors import (AssistantError,
                    CommandFailedError,
                    StateNotFoundError,
                    ValueNotFoundError)
from settings import COLORS, IS_DEBUG_MODE
from subprocess import check_output, CalledProcessError, STDOUT
from typing import Dict


class VagrantAssistant(Assistant):
    """An assistant desgined to monitor the current state of a given vagrant VM

    NOTE: The ID of any vagrant vm can easily be found by using the command
    `vagrant global status`

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        vagrant_vm_name (str): name of the vagrant
        vagrant_vm_id (str): id of the vm
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 vagrant_vm_name: str,
                 vagrant_vm_id: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.vagrant_vm_name: str = vagrant_vm_name
        self.vagrant_vm_id: str = vagrant_vm_id
        self.POWEROFF: str = 'poweroff'
        self.RUNNING: str = 'running'
        self.SAVED: str = 'saved'
        self.SAVING: str = 'saving'
        self.RESTORING: str = 'restoring'
        self.ABORTED: str = 'aborted'

    def _get_vagrant_output(self) -> str:
        cmd: str = 'vagrant status ' + self.vagrant_vm_id
        try:
            return check_output(cmd,
                                stderr=STDOUT,
                                shell=True,
                                text=True)
        except CalledProcessError:
            raise CommandFailedError(self.name, cmd)

    def state_identifier(self) -> str:
        try:
            output: str = self._get_vagrant_output()
            is_correct_name: bool = False
            for value in output.split():
                if is_correct_name:
                    return value
                if value == self.vagrant_vm_name:
                    is_correct_name = True
            raise VagrantNotFoundError(self.name, self.vagrant_vm_name)
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.POWEROFF: COLORS['red'],
            self.ABORTED: COLORS['red'],
            self.RUNNING: COLORS['light green'],
            self.RESTORING: COLORS['light green'],
            self.SAVED: COLORS['light blue'],
            self.SAVING: COLORS['light blue']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.POWEROFF: 'Your vagrant is off',
            self.ABORTED: 'Your vagrant is aborted',
            self.RUNNING: 'Your vagrant is running',
            self.RESTORING: 'Your vagrant is running',
            self.SAVED: 'Your vagrant is suspended',
            self.SAVING: 'Your vagrant is suspended'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')


class VagrantNotFoundError(AssistantError):
    """Raised when a vagrant vm by the specified name was unable to be found

    Attributes:
        name (str): name of the assistant
        vm_name (str): name of the vagrant vm
    """

    def __init__(self, name: str, vm_name: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.vm_name: str = vm_name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The status of ' + self.vm_name +
                  ' could not be found')
