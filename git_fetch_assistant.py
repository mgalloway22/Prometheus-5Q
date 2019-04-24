from assistant import Assistant
from errors import (AssistantError,
                    StateNotFoundError,
                    InvalidPathToGitRepoError,
                    ValueNotFoundError)
from git import CommandError, Head, NoSuchPathError, Repo
from settings import COLORS, IS_DEBUG_MODE
from typing import Dict


class GitFetchAssistant(Assistant):
    """An assistant desinged to track if the active branch is ahead or behind

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
        self.number_away: int = 0
        self.repo: Repo
        self.UP_TO_DATE: str = 'up to date'
        self.BEHIND: str = 'behind'
        self.AHEAD: str = 'ahead'
        self.DETACHED: str = 'detached'

    def _set_current_number_away(self):
        active_branch: Head = self.repo.active_branch
        tracking_branch = active_branch.tracking_branch()
        if tracking_branch is None:
            raise NoUpstreamError(self.name)
        behind_cmp: str = (active_branch.name + '..' +
                           tracking_branch.name)
        amount_behind: int = sum(1 for c in self.repo.iter_commits(behind_cmp))
        ahead_cmp: str = (active_branch.tracking_branch().name + '..' +
                          active_branch.name)
        amount_ahead: int = sum(1 for c in self.repo.iter_commits(ahead_cmp))
        self.number_away = amount_ahead - amount_behind

    def _set_current_repo_and_fetch(self):
        try:
            self.repo = Repo(self.path_to_repo)
        except NoSuchPathError:
            raise InvalidPathToGitRepoError(self.name, self.path_to_repo)
        try:
            if not self.repo.head.is_detached:
                self.repo.remote().fetch()
        except CommandError:
            raise GitFetchError(self.name)

    def state_identifier(self) -> str:
        try:
            self._set_current_repo_and_fetch()
            if self.repo.head.is_detached:
                return self.DETACHED
            self._set_current_number_away()
            if self.number_away == 0:
                return self.UP_TO_DATE
            elif self.number_away > 0:
                return self.AHEAD
            else:
                return self.BEHIND
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.UP_TO_DATE: COLORS['light blue'],
            self.BEHIND: COLORS['purple'],
            self.AHEAD: COLORS['orange'],
            self.DETACHED: COLORS['red']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.UP_TO_DATE: (self.name +
                              ' is up to date on the current branch'),
            self.AHEAD: (self.name + ' is ahead by ' + str(self.number_away) +
                         ' commits on the current branch'),
            self.BEHIND: (self.name + ' is behind by '
                          + str(0 - self.number_away) +
                          ' commits on the current branch'),
            self.DETACHED: self.name + ' has a detached head'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')


class GitFetchError(AssistantError):
    """Raised when the `git fetch` command fails

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The `git fetch` command failed, please ' +
                  'make sure that you are able to access the desired ' +
                  'repository')


class NoUpstreamError(AssistantError):
    """Raised when the the current branch does not have an upstream branch set

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': the active branch does not have a remote ' +
                  'branch set - cannot deduce the amount of commits ahead ' +
                  'or behind')
