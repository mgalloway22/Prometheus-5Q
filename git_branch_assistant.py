from assistant import Assistant
from errors import (AssistantError,
                    StateNotFoundError,
                    InvalidPathToGitRepoError,
                    ValueNotFoundError)
from git import Repo, NoSuchPathError
from settings import COLORS
from typing import Dict


class GitBranchAssistant(Assistant):
    """An assistant desinged to track the current branch of a git repo

    The purpose of this assistant is to track if git repo is on the main
    branch or on a feature branch. Since this main branch could be named
    something unconventional (ex. 'develop'), the `main_branch_name` is
    required as an attribute.

    NOTE: The path to the repo should be the full absolute path to the repo
    without the home symbol (~/)

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        path_to_repo (str): path to the git repo
        main_branch_name (str): name of the main branch
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 path_to_repo: str,
                 main_branch_name: str):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.path_to_repo: str = path_to_repo
        self.main_branch_name: str = main_branch_name
        self.current_branch_name: str = ''
        self.MAIN_BRANCH: str = 'main branch'
        self.FEATURE_BRANCH: str = 'feature branch'

    def _set_current_branch_name(self):
        try:
            repo: Repo = Repo(self.path_to_repo)
            if repo.head.is_detached:
                self.current_branch_name = "detached HEAD"
            else:
                self.current_branch_name = (Repo(self.path_to_repo)
                                            .active_branch
                                            .name)
        except NoSuchPathError:
            raise InvalidPathToGitRepoError(self.name, self.path_to_repo)

    def state_identifier(self) -> str:
        try:
            self._set_current_branch_name()
            return (self.MAIN_BRANCH if self.current_branch_name ==
                    self.main_branch_name else self.FEATURE_BRANCH)
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.MAIN_BRANCH: COLORS['light blue'],
            self.FEATURE_BRANCH: COLORS['purple']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.MAIN_BRANCH: (self.name + ' is on the main branch: ' +
                               self.current_branch_name),
            self.FEATURE_BRANCH: (self.name + ' is on the feature branch: ' +
                                  self.current_branch_name)
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
