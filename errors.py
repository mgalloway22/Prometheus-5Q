from settings import IS_DEBUG_MODE


class AssistantError(Exception):
    """Base class for an error caused by a Das Keyboard Assistant

    When an `AssistantError` is raised and subsequently caught, it should
    have `elaborate()` called as shown in the example below

    NOTE: Do not elaborate an error and re-raise it; this will likely cause
    it to be elaborated twice

    NOTE: `AssistantError`'s should only be elaborated in one of the three
    abstract methods that the assistant needs to override: `state_identifier`,
    `color_identifier`, and `message_identifier` as shown in the example below

    NOTE: If an error is being caught and resulting in a different error being
    raised, then the first error should be elaborated as shown in the exaple
    below

    ```
    try:
        dummy_assistant.do_something()
    except DummyAssistantError as e
        e.elaborate()
        raise StateNotFoundError(self.name)
    ```
    """
    def __init__(self):
        Exception.__init__(self)

    def elaborate(self):
        """Method for printing a standard error message in a certain situation

        Error message is only printed if `IS_DEBUG_MODE` is set to true
        """
        print('This Error has not overriden elaborate()')


class OverrideError(AssistantError):
    """Raised when an assistant failed to override a necessary method

    Attributes:
        name (str): name of the assistant
        method (str): name of the method (state, color, or message)
    """
    def __init__(self, name: str, method: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.method: str = method

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': the method for identifying ' + self.method +
                  ' was never overriden')


class ValueNotFoundError(AssistantError):
    """Raised when color or message is unable to be evaluated for the current state

    Attributes:
        name (str): name of the assistant
        state (str): name of the current state
        value (str): name of the value (color or message)
    """
    def __init__(self, name: str, state: str, value: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.state: str = state
        self.value: str = value

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The value of ' + self.value + ' could not be '
                  + 'found for the state of ' + self.state)


class StateNotFoundError(AssistantError):
    """Raised when state is unable to be evaluated for the assistant

    Attributes:
        name (str): name of the assistant
    """
    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': Failed to identify state')


class NoSignalError(AssistantError):
    """Raised when a signal is not found for the given zone_id

    Attributes:
        name (str): name of the assistant
        zone_id (str): the zone_id of the signal
    """
    def __init__(self, name: str, zone_id: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.zone_id: str = zone_id

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': No signal found for zone_id ' + self.zone_id)


class ConnectionFailedError(AssistantError):
    """Raised when a connection attempt receives a status code that is not 200

    Attributes:
        name (str): name of the assistant
        request_type (str): type of the request (GET, POST, etc.)
        status_code (int): the status code of the failed request
    """
    def __init__(self, name: str, request_type: str, status_code: int):
        AssistantError.__init__(self)
        self.name: str = name
        self.request_type: str = request_type
        self.status_code: int = status_code

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': Connection type of ' + self.request_type +
                  ' failed with a status code of ' + str(self.status_code))


class CommandFailedError(AssistantError):
    """Raised when a shell command fails

    Attributes:
        name (str): name of the assistant
        cmd (str): command that failed
    """

    def __init__(self, name: str, cmd: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.cmd: str = cmd

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': Command of ' + self.cmd + ' failed ')


class NoInternetError(AssistantError):
    """Raised when the internet seems to not be functioning properly

    Attributes:
        name (str): name of the assistant
    """

    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': There seems to be no internet connection ' +
                  'available, please verify that the internet connection is ' +
                  'functioning properly')


class DasApplicationNotRunningError(AssistantError):
    """Raised when it is noticed that the Das Application is not open

    NOTE: This will error means that the assistant will not be able to
    communicate with the Das Keyboard, and therefore should be immediately be
    elaborated and then `exit()` which is not handled in the `elaborate()`:
    ```
    from requests import exceptions as requests_exceptions
    from urllib3 import exceptions as url_exceptions

    except (requests_exceptions.ConnectionError,
            url_exceptions.NewConnectionError):
        e: DasApplicationNotRunningError = (
            DasApplicationNotRunningError(self.name))
        e.elaborate()
        exit()
    ```
    """
    def __init__(self, name: str):
        AssistantError.__init__(self)
        self.name: str = name

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The connection to the Das Keyboard was ' +
                  'refused, please verify that the client application ' +
                  'is running')


class InvalidPathToGitRepoError(AssistantError):
    """Raised when the path to the git repo is invalid

    Attributes:
        name (str): name of the assistant
        path (str): the path provided to the git repo
    """

    def __init__(self, name: str, path: str):
        AssistantError.__init__(self)
        self.name: str = name
        self.path: str = path

    def elaborate(self):
        if IS_DEBUG_MODE:
            print(self.name + ': The path to the git repo ' + self.path +
                  ' was invalid')
