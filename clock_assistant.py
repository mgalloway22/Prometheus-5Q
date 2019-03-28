from assistant import Assistant
from datetime import datetime, timedelta
from dateutil import tz
from errors import AssistantError, StateNotFoundError, ValueNotFoundError
from settings import COLORS
from typing import Dict, List


class ClockAssistant(Assistant):
    """An assistant desgined to produce a signal at a given time on certain days

    NOTE: the `weekday_indexes` are the days of the week that the notification
    should be active. This is a zero base index starting where Monday is 0,
    Tuesday is 1, etc.

    NOTE: the 'tz_abbrev' is the timezone abbreviation passed into
    `dateutil.tz.gettz(..)` this must be a valid time zone abbreviation
    (example: 'CST')

    NOTE: the `loc_hour` is on the 24 hour scale (0-23)

    NOTE: if the `notification_duration` carrys over into a date that is not
    desired, the notification will not display

    Attributes:
        name (str): name of the assistant
        delay (str): the delay between evaluations
        zone_id (str): the zone_id to bind the color to
        is_muted (bool): flag to deliver with no message
        weekday_indexes (List[str]): the indexes of the weekday
        tz_abbrev (str): abbreviation for the desired timezone
        loc_hours (int): hour at which to notify in the desired timezone
        loc_minutes (int): minute at which to notify in the desired timezone
        notification_duration (int): minutes the notification should persist
    """

    def __init__(self,
                 name: str,
                 delay: int,
                 zone_id: str,
                 is_muted: bool,
                 weekday_indexes: List[int],
                 tz_abbrev: str,
                 loc_hours: int,
                 loc_minutes: int,
                 notification_duration: int):
        Assistant.__init__(self, name, delay, zone_id, is_muted)
        self.weekday_indexes: List[int] = weekday_indexes
        self.tz_abbrev: str = tz_abbrev
        self.loc_hours: int = loc_hours
        self.loc_minutes: int = loc_minutes
        self.notification_duration: int = notification_duration
        self.NOTIFY = 'notify'
        self.SLEEP = 'sleep'

    def state_identifier(self) -> str:
        try:
            time_string: str = (str(self.loc_hours) + " " +
                                str(self.loc_minutes) + " " +
                                self.tz_abbrev)
            start: datetime = datetime.strptime(time_string, "%H %M %Z")
            end: datetime = start + timedelta(
                minutes=self.notification_duration)
            now: datetime = datetime.now(tz.gettz(self.tz_abbrev))
            if now.weekday() not in self.weekday_indexes:
                return self.SLEEP
            if start.time() < now.time() < end.time():
                return self.NOTIFY
            else:
                return self.SLEEP
        except AssistantError as e:
            e.elaborate()
            raise StateNotFoundError(self.name)

    def color_identifier(self, state: str) -> str:
        color_switcher: Dict[str, str] = {
            self.NOTIFY: COLORS['orange'],
            self.SLEEP: COLORS['light blue']
        }
        if state in color_switcher:
            return color_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'color')

    def message_identifier(self, state: str) -> str:
        message_switcher: Dict[str, str] = {
            self.NOTIFY: self.name + ' is within the desired time range',
            self.SLEEP: self.name + ' is not within the desired time range'
        }
        if state in message_switcher:
            return message_switcher[state]
        else:
            raise ValueNotFoundError(self.name, state, 'message')
