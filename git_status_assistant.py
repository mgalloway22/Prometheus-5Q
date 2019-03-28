from assistant import Assistant
from errors import (AssistantError,
                    StateNotFoundError,
                    InvalidPathToGitRepoError,
                    ValueNotFoundError)
from git import Repo, NoSuchPathError
from settings import COLORS
from typing import Dict


class GitStatusAssistant(Assistant):
    """An assistant desgined to check if a git repo has uncommitted changes

    NOTE: The path to the repo should be the full absolute path to the repo
    without the home symbol (~/)

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        path_to_repo (str): path to the git repo
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 path_to_repo: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.path_to_repo: str = path_to_repo
        self.BRANCH_CLEAN: str = 'branch clean'
        self.BRANCH_DIRTY: str = 'branch dirty'

    def _is_current_branch_dirty(self) -> bool:
        try:
            return Repo(self.path_to_repo).is_dirty()
        except NoSuchPathError:
            raise InvalidPathToGitRepoError(self.name, self.path_to_repo)

    def state_identifier(self) -> str:
        try:
            return (self.BRANCH_DIRTY
                    if self._is_current_branch_dirty()
                    else self.BRANCH_CLEAN)
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.BRANCH_CLEAN: COLORS['light blue'],
            self.BRANCH_DIRTY: COLORS['purple']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.BRANCH_CLEAN: self.name + ' is clean',
            self.BRANCH_DIRTY: self.name + ' is dirty'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
