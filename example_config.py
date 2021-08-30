from assistant import Assistant
from clock_assistant import ClockAssistant
from cpu_assistant import CPUAssistant
from git_branch_assistant import GitBranchAssistant
from git_fetch_assistant import GitFetchAssistant
from git_status_assistant import GitStatusAssistant
from message_assistant import MessageAssistant
from metra_assistant import MetraAssistant
from typing import List, Optional
from vagrant_assistant import VagrantAssistant
from yaml_assistant import YamlAssistant

"""Example Configuration class for the keyboard driver

Here is where the variables that are fed to assistants are stored

NOTE: can also point to a global config with the following code
```
from assistant import Assistant
from typing import List
import sys

sys.path.append("/path/to/global_config/folder")

from global_config import init_global_assistants


def init_assistants() -> List[Assistant]:
    return init_global_assistants()
```
"""


def init_assistants() -> List[Assistant]:
    all_assistants: List[Assistant] = []

    # NCS metra_assistant
    NCS_METRA_NAME: str = 'NCS Status'
    NCS_METRA_DELAY: int = 600
    NCS_METRA_ZONE_ID: str = '1,0'
    NCS_METRA_IS_MUTED: bool = False
    NCS_METRA_ACCESS_KEY: str = 'access-key'
    NCS_METRA_SECRET_KEY: str = 'secret-key'
    NCS_METRA_ROUTE_ID: str = 'NCS'
    NCS_METRA: MetraAssistant = MetraAssistant(
        NCS_METRA_NAME,
        NCS_METRA_DELAY,
        NCS_METRA_ZONE_ID,
        NCS_METRA_IS_MUTED,
        NCS_METRA_ACCESS_KEY,
        NCS_METRA_SECRET_KEY,
        NCS_METRA_ROUTE_ID
    )
    all_assistants.append(NCS_METRA)

    # general message_assistant variables
    MESSAGE_CHAT_DB_PATH: str = '/path/to/chat.db'
    MESSAGE_ADDRESSBOOK_DB_PATH: str = '/path/to/AddressBook-v22.abcddb'

    # john message_assistant (only direct messages from john)
    JOHN_MESSAGE_NAME: str = 'John'
    JOHN_MESSAGE_DELAY: int = 10
    JOHN_MESSAGE_ZONE_ID: str = '3,0'
    JOHN_MESSAGE_IS_MUTED: bool = False
    JOHN_MESSAGE_NAMES_CRITERIA: List[Optional[str]] = ['john smith']
    JOHN_MESSAGE_IS_NAMES_INCLUDE: bool = True
    JOHN_MESSAGE_GROUPCHAT_NAMES_CRITERIA: List[Optional[str]] = [None]
    JOHN_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE: bool = True
    JOHN_MESSAGE: MessageAssistant = MessageAssistant(
        JOHN_MESSAGE_NAME,
        JOHN_MESSAGE_DELAY,
        JOHN_MESSAGE_ZONE_ID,
        JOHN_MESSAGE_IS_MUTED,
        MESSAGE_CHAT_DB_PATH,
        MESSAGE_ADDRESSBOOK_DB_PATH,
        JOHN_MESSAGE_NAMES_CRITERIA,
        JOHN_MESSAGE_IS_NAMES_INCLUDE,
        JOHN_MESSAGE_GROUPCHAT_NAMES_CRITERIA,
        JOHN_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE
    )
    all_assistants.append(JOHN_MESSAGE)

    # family message_assistant (only direct messages from family)
    FAMILY_MESSAGE_NAME: str = 'Family'
    FAMILY_MESSAGE_DELAY: int = 10
    FAMILY_MESSAGE_ZONE_ID: str = '4,0'
    FAMILY_MESSAGE_IS_MUTED: bool = False
    FAMILY_MESSAGE_NAMES_CRITERIA: List[Optional[str]] = ['mom',
                                                          'dad',
                                                          'sister',
                                                          'brother']
    FAMILY_MESSAGE_IS_NAMES_INCLUDE: bool = True
    FAMILY_MESSAGE_GROUPCHAT_NAMES_CRITERIA: List[Optional[str]] = [None]
    FAMILY_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE: bool = True
    FAMILY_MESSAGE: MessageAssistant = MessageAssistant(
        FAMILY_MESSAGE_NAME,
        FAMILY_MESSAGE_DELAY,
        FAMILY_MESSAGE_ZONE_ID,
        FAMILY_MESSAGE_IS_MUTED,
        MESSAGE_CHAT_DB_PATH,
        MESSAGE_ADDRESSBOOK_DB_PATH,
        FAMILY_MESSAGE_NAMES_CRITERIA,
        FAMILY_MESSAGE_IS_NAMES_INCLUDE,
        FAMILY_MESSAGE_GROUPCHAT_NAMES_CRITERIA,
        FAMILY_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE
    )
    all_assistants.append(FAMILY_MESSAGE)

    # groups message_assistant (all groupchat messages)
    GROUPS_MESSAGE_NAME: str = 'Groups'
    GROUPS_MESSAGE_DELAY: int = 10
    GROUPS_MESSAGE_ZONE_ID: str = '5,0'
    GROUPS_MESSAGE_IS_MUTED: bool = False
    GROUPS_MESSAGE_NAMES_CRITERIA: List[Optional[str]] = []
    GROUPS_MESSAGE_IS_NAMES_INCLUDE: bool = False
    GROUPS_MESSAGE_GROUPCHAT_NAMES_CRITERIA: List[Optional[str]] = [None]
    GROUPS_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE: bool = False
    GROUPS_MESSAGE: MessageAssistant = MessageAssistant(
        GROUPS_MESSAGE_NAME,
        GROUPS_MESSAGE_DELAY,
        GROUPS_MESSAGE_ZONE_ID,
        GROUPS_MESSAGE_IS_MUTED,
        MESSAGE_CHAT_DB_PATH,
        MESSAGE_ADDRESSBOOK_DB_PATH,
        GROUPS_MESSAGE_NAMES_CRITERIA,
        GROUPS_MESSAGE_IS_NAMES_INCLUDE,
        GROUPS_MESSAGE_GROUPCHAT_NAMES_CRITERIA,
        GROUPS_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE
    )
    all_assistants.append(GROUPS_MESSAGE)

    # other message_assistant (all other messages)
    OTHER_MESSAGE_NAME: str = 'Other'
    OTHER_MESSAGE_DELAY: int = 10
    OTHER_MESSAGE_ZONE_ID: str = '6,0'
    OTHER_MESSAGE_IS_MUTED: bool = False
    OTHER_MESSAGE_NAMES_CRITERIA: List[Optional[str]] = ['john smith',
                                                         'mom',
                                                         'dad',
                                                         'sister',
                                                         'brother']
    OTHER_MESSAGE_IS_NAMES_INCLUDE: bool = False
    OTHER_MESSAGE_GROUPCHAT_NAMES_CRITERIA: List[Optional[str]] = [None]
    OTHER_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE: bool = True
    OTHER_MESSAGE: MessageAssistant = MessageAssistant(
        OTHER_MESSAGE_NAME,
        OTHER_MESSAGE_DELAY,
        OTHER_MESSAGE_ZONE_ID,
        OTHER_MESSAGE_IS_MUTED,
        MESSAGE_CHAT_DB_PATH,
        MESSAGE_ADDRESSBOOK_DB_PATH,
        OTHER_MESSAGE_NAMES_CRITERIA,
        OTHER_MESSAGE_IS_NAMES_INCLUDE,
        OTHER_MESSAGE_GROUPCHAT_NAMES_CRITERIA,
        OTHER_MESSAGE_IS_GROUPCHAT_NAMES_INCLUDE
    )
    all_assistants.append(OTHER_MESSAGE)

    # python cpu_assistant
    PYTHON_CPU_NAME: str = 'Python CPU'
    PYTHON_CPU_DELAY: int = 5
    PYTHON_CPU_ZONE_ID: str = '8,0'
    PYTHON_CPU_IS_MUTED: bool = True
    PYTHON_CPU_PROCESS_NAME: str = 'python'
    PYTHON_CPU: CPUAssistant = CPUAssistant(
        PYTHON_CPU_NAME,
        PYTHON_CPU_DELAY,
        PYTHON_CPU_ZONE_ID,
        PYTHON_CPU_IS_MUTED,
        PYTHON_CPU_PROCESS_NAME
    )
    all_assistants.append(PYTHON_CPU)

    # teams cpu_assistant (for Microsoft Teams)
    TEAMS_CPU_NAME: str = 'Teams CPU'
    TEAMS_CPU_DELAY: int = 5
    TEAMS_CPU_ZONE_ID: str = '9,0'
    TEAMS_CPU_IS_MUTED: bool = True
    TEAMS_CPU_PROCESS_NAME: str = 'teams'
    TEAMS_CPU: CPUAssistant = CPUAssistant(
        TEAMS_CPU_NAME,
        TEAMS_CPU_DELAY,
        TEAMS_CPU_ZONE_ID,
        TEAMS_CPU_IS_MUTED,
        TEAMS_CPU_PROCESS_NAME
    )
    all_assistants.append(TEAMS_CPU)

    # default vagrant_assistant
    DEFAULT_VAGRANT_NAME: str = 'Vagrant Status'
    DEFAULT_VAGRANT_DELAY: int = 60
    DEFAULT_VAGRANT_ZONE_ID: str = '10,0'
    DEFAULT_VAGRANT_IS_MUTED: bool = False
    DEFAULT_VAGRANT_VM_NAME: str = 'default'
    DEFAULT_VAGRANT_VM_ID: str = 'default-vagrant-id'
    DEFAULT_VAGRANT: VagrantAssistant = VagrantAssistant(
        DEFAULT_VAGRANT_NAME,
        DEFAULT_VAGRANT_DELAY,
        DEFAULT_VAGRANT_ZONE_ID,
        DEFAULT_VAGRANT_IS_MUTED,
        DEFAULT_VAGRANT_VM_NAME,
        DEFAULT_VAGRANT_VM_ID
    )
    all_assistants.append(DEFAULT_VAGRANT)

    # ui yaml_assistant
    UI_YAML_NAME: str = 'UI Pubspec'
    UI_YAML_DELAY: int = 120
    UI_YAML_ZONE_ID: str = '11,0'
    UI_YAML_IS_MUTED: bool = False
    UI_YAML_URL: str = 'https://pubspec-url.com/pubspec.txt'
    UI_YAML_ARGUMENTS: List[str] = ['packages', 'product_name', 'version']
    UI_YAML_NOTIFICATION_DURATION: int = 60
    UI_YAML: YamlAssistant = YamlAssistant(
        UI_YAML_NAME,
        UI_YAML_DELAY,
        UI_YAML_ZONE_ID,
        UI_YAML_IS_MUTED,
        UI_YAML_URL,
        UI_YAML_ARGUMENTS,
        UI_YAML_NOTIFICATION_DURATION
    )
    all_assistants.append(UI_YAML)

    # timezone abbreviation
    CLOCK_TZ_ABBREV: str = 'GMT'

    # standup clock assistant (9:30)
    STANDUP_CLOCK_NAME: str = 'Morning Standup'
    STANDUP_CLOCK_DELAY: int = 30
    STANDUP_CLOCK_ZONE_ID: str = '16,0'
    STANDUP_CLOCK_IS_MUTED: bool = False
    STANDUP_CLOCK_WEEKDAY_INDEXES: List[int] = [0, 1, 2, 3, 4]
    STANDUP_CLOCK_LOC_HOURS: int = 9
    STANDUP_CLOCK_LOC_MINUTES: int = 25
    STANDUP_CLOCK_NOTIFICATION_DURATION: int = 5
    STANDUP_CLOCK: ClockAssistant = ClockAssistant(
        STANDUP_CLOCK_NAME,
        STANDUP_CLOCK_DELAY,
        STANDUP_CLOCK_ZONE_ID,
        STANDUP_CLOCK_IS_MUTED,
        STANDUP_CLOCK_WEEKDAY_INDEXES,
        CLOCK_TZ_ABBREV,
        STANDUP_CLOCK_LOC_HOURS,
        STANDUP_CLOCK_LOC_MINUTES,
        STANDUP_CLOCK_NOTIFICATION_DURATION
    )
    all_assistants.append(STANDUP_CLOCK)

    # workout clock assistant (1:30)
    WORKOUT_CLOCK_NAME: str = 'Workout Reminder'
    WORKOUT_CLOCK_DELAY: int = 30
    WORKOUT_CLOCK_ZONE_ID: str = '17,0'
    WORKOUT_CLOCK_IS_MUTED: bool = False
    WORKOUT_CLOCK_WEEKDAY_INDEXES: List[int] = [0, 2, 4]
    WORKOUT_CLOCK_LOC_HOURS: int = 13
    WORKOUT_CLOCK_LOC_MINUTES: int = 00
    WORKOUT_CLOCK_NOTIFICATION_DURATION: int = 30
    WORKOUT_CLOCK: ClockAssistant = ClockAssistant(
        WORKOUT_CLOCK_NAME,
        WORKOUT_CLOCK_DELAY,
        WORKOUT_CLOCK_ZONE_ID,
        WORKOUT_CLOCK_IS_MUTED,
        WORKOUT_CLOCK_WEEKDAY_INDEXES,
        CLOCK_TZ_ABBREV,
        WORKOUT_CLOCK_LOC_HOURS,
        WORKOUT_CLOCK_LOC_MINUTES,
        WORKOUT_CLOCK_NOTIFICATION_DURATION
    )
    all_assistants.append(WORKOUT_CLOCK)

    # train clock assistant (5:45)
    TRAIN_CLOCK_NAME: str = '5:45 Train'
    TRAIN_CLOCK_DELAY: int = 30
    TRAIN_CLOCK_ZONE_ID: str = '18,0'
    TRAIN_CLOCK_IS_MUTED: bool = False
    TRAIN_CLOCK_WEEKDAY_INDEXES: List[int] = [0, 1, 2, 3]
    TRAIN_CLOCK_LOC_HOURS: int = 17
    TRAIN_CLOCK_LOC_MINUTES: int = 15
    TRAIN_CLOCK_NOTIFICATION_DURATION: int = 30
    TRAIN_CLOCK: ClockAssistant = ClockAssistant(
        TRAIN_CLOCK_NAME,
        TRAIN_CLOCK_DELAY,
        TRAIN_CLOCK_ZONE_ID,
        TRAIN_CLOCK_IS_MUTED,
        TRAIN_CLOCK_WEEKDAY_INDEXES,
        CLOCK_TZ_ABBREV,
        TRAIN_CLOCK_LOC_HOURS,
        TRAIN_CLOCK_LOC_MINUTES,
        TRAIN_CLOCK_NOTIFICATION_DURATION
    )
    all_assistants.append(TRAIN_CLOCK)

    # server-side git repo path
    SS_PATH: str = '/path/to/server/side/repo'

    # server-side git_branch_assistant
    SS_BRANCH_NAME: str = 'Server-Side Branch'
    SS_BRANCH_DELAY: int = 5
    SS_BRANCH_ZONE_ID: str = '16,1'
    SS_BRANCH_IS_MUTED: bool = False
    SS_BRANCH_MAIN_BRANCH_NAME = 'master'
    SS_BRANCH: GitBranchAssistant = GitBranchAssistant(
        SS_BRANCH_NAME,
        SS_BRANCH_DELAY,
        SS_BRANCH_ZONE_ID,
        SS_BRANCH_IS_MUTED,
        SS_PATH,
        SS_BRANCH_MAIN_BRANCH_NAME
    )
    all_assistants.append(SS_BRANCH)

    # server-side git_status_assistant
    SS_STATUS_NAME: str = 'Server-Side Status'
    SS_STATUS_DELAY: int = 5
    SS_STATUS_ZONE_ID: str = '17,1'
    SS_STATUS_IS_MUTED: bool = False
    SS_STATUS: GitStatusAssistant = GitStatusAssistant(
        SS_STATUS_NAME,
        SS_STATUS_DELAY,
        SS_STATUS_ZONE_ID,
        SS_STATUS_IS_MUTED,
        SS_PATH
    )
    all_assistants.append(SS_STATUS)

    # server-side git_fetch_assistant
    SS_FETCH_NAME: str = 'Server-Side Fetch'
    SS_FETCH_DELAY: int = 300
    SS_FETCH_ZONE_ID: str = '18,1'
    SS_FETCH_IS_MUTED: bool = False
    SS_FETCH: GitFetchAssistant = GitFetchAssistant(
        SS_FETCH_NAME,
        SS_FETCH_DELAY,
        SS_FETCH_ZONE_ID,
        SS_FETCH_IS_MUTED,
        SS_PATH
    )
    all_assistants.append(SS_FETCH)

    # client-side git repo path
    CS_PATH: str = '/path/to/client/side/repo'

    # client-side git_branch_assistant
    CS_BRANCH_NAME: str = 'Client-Side Branch'
    CS_BRANCH_DELAY: int = 5
    CS_BRANCH_ZONE_ID: str = '16,2'
    CS_BRANCH_IS_MUTED: bool = False
    CS_BRANCH_MAIN_BRANCH_NAME = 'master'
    CS_BRANCH: GitBranchAssistant = GitBranchAssistant(
        CS_BRANCH_NAME,
        CS_BRANCH_DELAY,
        CS_BRANCH_ZONE_ID,
        CS_BRANCH_IS_MUTED,
        CS_PATH,
        CS_BRANCH_MAIN_BRANCH_NAME
    )
    all_assistants.append(CS_BRANCH)

    # client-side git_status_assistant
    CS_STATUS_NAME: str = 'Client-Side Status'
    CS_STATUS_DELAY: int = 5
    CS_STATUS_ZONE_ID: str = '17,2'
    CS_STATUS_IS_MUTED: bool = False
    CS_STATUS: GitStatusAssistant = GitStatusAssistant(
        CS_STATUS_NAME,
        CS_STATUS_DELAY,
        CS_STATUS_ZONE_ID,
        CS_STATUS_IS_MUTED,
        CS_PATH
    )
    all_assistants.append(CS_STATUS)

    # client-side git_fetch_assistant
    CS_FETCH_NAME: str = 'Client-Side Fetch'
    CS_FETCH_DELAY: int = 300
    CS_FETCH_ZONE_ID: str = '18,2'
    CS_FETCH_IS_MUTED: bool = False
    CS_FETCH: GitFetchAssistant = GitFetchAssistant(
        CS_FETCH_NAME,
        CS_FETCH_DELAY,
        CS_FETCH_ZONE_ID,
        CS_FETCH_IS_MUTED,
        CS_PATH
    )
    all_assistants.append(CS_FETCH)

    # == ADD CUSTOM ASSISTANTS HERE! ==

    return all_assistants
