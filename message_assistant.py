from assistant import Assistant
from sqlite3 import connect, Connection, Cursor, OperationalError
from errors import AssistantError, StateNotFoundError, ValueNotFoundError
from re import sub
from settings import COLORS, IS_DEBUG_MODE
from typing import Dict, List, Optional


class Message:
    """A class for text message objects

    NOTE: Direct messages will have `None` as thier `group_name`
    """
    def __init__(self, sender: str, text: str, group_name: Optional[str]):
        self.sender: str = sender
        self.text: str = text
        self.group_name: Optional[str] = group_name


class MessageAssistant(Assistant):
    """An assistant desgined to monitor the current state of a given vagrant VM

    This assistant is designed to filter all unread texts into desired groups
    depending on the sender and the groupchat name. Sender names and groupchat
    names are case insensitive

    NOTE: None is the groupchat_names_critera value for a direct message

    NOTE: If multiple contacts are found corresponding to a phone number, the
    first will be chosen. If no contacts are found, the phone number will be
    used as the name

    NOTE: If there is no name for a groupchat, it will be treated as a direct
    message

    NOTE: If a message fails the groupchat or names filter, it is not included

    NOTE: If a groupchat’s name is changed, it must be updated in the
    configuration

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): bool to have the assistant deliver with no message
        names_criteria (List[Optional[str]]): Criteria of names
        is_names_include (bool): Bool to in/ex-clude the names
        groupchat_names_criteria (List[Optional[str]]): criteria of group names
        is_groupchat_names_include (bool): Bool to in/ex-clude the group names

    EXAMPLES:
        No messages
            = (..., [], True, [], True)
            = (..., [], True, [], False)

        All messages
            = (..., [], False, [], False)

        All direct messages
            = (..., [], False, [None], True)

        All groupchat messages
            = (..., [], False, [None], False)

        All messages that are either direct messages or in the ‘Book Club’
        group
            = (..., [], False, [None, ‘Book Club’], True)

        All groupchat messages that are not in the ‘Book Club’ group
            = (..., [], False, [None, ‘Book Club’], False)

        All messages from John Smith or Jane Smith (including those in a
        groupchat)
            = (..., [‘John Smith’, ‘Jane Smith’], True, [], False)

        All direct messages from John Smith or Jane Smith =
            = (..., [‘John Smith’, ‘Jane Smith’], True, [None], True)

        All groupchat messages from John Smith or Jane Smith =
            = (..., [‘John Smith’, ‘Jane Smith’], True, [None], False )

        All direct messages not from John Smith or Jane Smith
            = (..., [‘John Smith’, ‘Jane Smith’], False, [None], True)

        All messages that are not from John Smith and are not in the ‘Book
        Club’ groupchat
            = (..., [‘John Smith’], False, [‘Book Club’], False)

        All messages that are not from John Smith and are groupchat messages
        that are not in the ‘Book Club’ group
            = (..., [‘John Smith’], False, [‘Book Club’, None], False)

        All messages that are not from John Smith and are direct messages or
        in the ‘Book Club’ group
            = (..., [‘John Smith’], False, [‘Book Club’, None], True)

        All messages that are from John Smith and are in the ‘Book Club’ group
            = (..., [‘John Smith’], True, [‘Book Club’], True)

        All groupchat messages from the ‘Book Club’ group
            = (..., [], False, [‘Book Club’], True)
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 chat_db_path: str,
                 addressbook_db_path: str,
                 names_criteria: List[Optional[str]],
                 is_names_include: bool,
                 groupchat_names_criteria: List[Optional[str]],
                 is_groupchat_names_include: bool):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.chat_db_path: str = chat_db_path
        self.addressbook_db_path: str = addressbook_db_path
        self.names_criteria: List[Optional[str]] = list(
            map(lambda s: s if s is None else s.lower(), names_criteria))
        self.is_names_include: bool = is_names_include
        self.groupchat_names_criteria: List[Optional[str]] = list(
            map(lambda s: s if s is None else s.lower(),
                groupchat_names_criteria))
        self.is_groupchat_names_include: bool = is_groupchat_names_include
        self._desired_messages: List[Message] = []
        self.READ_MESSAGES: str = 'read messages'
        self.UNREAD_MESSAGES: str = 'unread messages'

    def _convert_phone_number_to_sql(self, phone_number: str) -> str:
        filtered_phone_number: str = sub(r'\D', '', phone_number)
        if len(filtered_phone_number) == 0:
            raise InvalidPhoneNumberError(self.name, phone_number)
        wild_carded_phone_number: str = '%'
        for char in filtered_phone_number:
            wild_carded_phone_number += char
            wild_carded_phone_number += '%'
        wild_carded_phone_number += '%'
        return wild_carded_phone_number

    def _query_all_unread_messages(self) -> List[Message]:
        all_unread_messages: List[Message] = []
        try:
            connection: Connection = connect(self.chat_db_path)
        except OperationalError:
            raise DatabaseConnectionError(self.name,
                                          'Chat',
                                          self.chat_db_path)
        cursor: Cursor = connection.cursor()
        cmd: str = ('SELECT id, text, display_name FROM message ' +
                    'LEFT JOIN chat_message_join ON message.ROWID = ' +
                    'message_id LEFT JOIN chat ON chat.ROWID = chat_id ' +
                    'LEFT JOIN handle ON handle_id = handle.ROWID WHERE ' +
                    'NOT is_from_me AND NOT is_read AND item_type = 0;')
        for value in cursor.execute(cmd):
            if len(value) == 3:
                if value[2] == '':
                    all_unread_messages.append(Message(value[0],
                                                       value[1],
                                                       None))
                else:
                    all_unread_messages.append(Message(value[0],
                                                       value[1],
                                                       value[2]))
            else:
                raise UnexpectedDBResponseError(self.name,
                                                'Chat',
                                                self.chat_db_path)
        return all_unread_messages

    def _query_contact_info_for_phone_number(self, phone_number: str) -> str:
        sql_phone_number: str = self._convert_phone_number_to_sql(phone_number)
        try:
            connection: Connection = connect(self.addressbook_db_path)
        except OperationalError:
            raise DatabaseConnectionError(self.name,
                                          'AddressBook',
                                          self.addressbook_db_path)
        cursor: Cursor = connection.cursor()
        cmd: str = ('SELECT ZFIRSTNAME, ZLASTNAME FROM ZABCDPHONENUMBER ' +
                    'LEFT JOIN ZABCDRECORD ON ZABCDPHONENUMBER.ZOWNER = '
                    'ZABCDRECORD.Z_PK WHERE ZFULLNUMBER LIKE ' + "'" +
                    sql_phone_number + "'" + ';')
        for value in cursor.execute(cmd):
            # Default to use the first result
            if len(value) == 2:
                return value[0] + ' ' + value[1]
            else:
                raise UnexpectedDBResponseError(self.name,
                                                'AddressBook',
                                                self.addressbook_db_path)
        return phone_number

    def _populate_all_contact_info(self, messages: List[Message]):
        for message in messages:
            message.sender = self._query_contact_info_for_phone_number(
                message.sender)

    def _names_filter(self, message: Message) -> bool:
        if len(self.names_criteria) == 0:
            return not self.is_names_include
        sender_name_lower: str = message.sender.lower()
        if self.is_names_include:
            return sender_name_lower in self.names_criteria
        else:
            return sender_name_lower not in self.names_criteria

    def _groupchat_names_filter(self, message: Message) -> bool:
        if len(self.groupchat_names_criteria) == 0:
            return not self.is_groupchat_names_include
        groupchat_name: Optional[str] = message.group_name
        groupchat_name_lower: Optional[str] = (
            None if groupchat_name is None
            else str(groupchat_name).lower())
        if self.is_groupchat_names_include:
            return groupchat_name_lower in self.groupchat_names_criteria
        else:
            return groupchat_name_lower not in self.groupchat_names_criteria

    def _combined_filter(self, message: Message) -> bool:
        return (self._names_filter(message)
                and self._groupchat_names_filter(message))

    def _filter_messages(self, messages: List[Message]) -> List[Message]:
        return list(filter(self._combined_filter, messages))

    def _query_all_desired_messages(self):
        messages: List[Message] = self._query_all_unread_messages()
        self._populate_all_contact_info(messages)
        self._desired_messages = self._filter_messages(messages)

    def state_identifier(self) -> str:
        try:
            self._query_all_desired_messages()
            if len(self._desired_messages) > 0:
                return self.UNREAD_MESSAGES
            else:
                return self.READ_MESSAGES
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.READ_MESSAGES: COLORS['light blue'],
            self.UNREAD_MESSAGES: COLORS['light green']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.UNREAD_MESSAGES: (str(len(self._desired_messages)) +
                                   ' new message(s) found from ' + self.name),
            self.READ_MESSAGES: 'No new message(s) found from ' + self.name
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')


class InvalidPhoneNumberError(AssistantError):
    """Raised when a phone number is found with unexpected values

    Attributes:
        name (str): name of the assistant
        phone_number (str): phone number unable to be parsed
    """

    def __init__(self,
                 name: str,
                 phone_number: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.phone_number: str = phone_number

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The phone number of ' + self.phone_number +
                  ' was unable to parsed')


class UnexpectedDBResponseError(AssistantError):
    """Raised when an unexpected response is recieved from a db

    Attributes:
        name (str): name of the assistant
        db_type (str): the type of db (Chat or AddressBook)
        db_path (str): path to the db that failed
    """

    def __init__(self, name: str, db_type: str, db_path: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.db_type: str = db_type
        self.db_path: str = db_path

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The ' + self.db_type + ' db at the path of ' +
                  self.db_path + ' is not operating as expected')


class DatabaseConnectionError(AssistantError):
    """Raised the assistant is unable to connect to a db at the given path

    Attributes:
        name (str): name of the assistant
        db_type (str): the type of db (Chat or AddressBook)
        db_path (str): path to the db that failed
    """

    def __init__(self, name: str, db_type: str, db_path: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.db_type: str = db_type
        self.db_path: str = db_path

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The ' + self.db_type + ' db at the path of ' +
                  self.db_path + ' is unable to connect. Please double-' +
                  'check the path and permissions')
