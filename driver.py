#!/usr/bin/env python3
from assistant import Assistant
from config import init_assistants
from errors import DasApplicationNotRunningError
from json import loads
from multiprocessing import Process
from requests import delete, exceptions as requests_exceptions, get, Response
from settings import BASE_URL, HEADERS, PID
from typing import List
from urllib3 import exceptions as url_exceptions


all_bindings: List[Process] = []


def kill_all_bindings():
    for binding in all_bindings:
        binding.terminate()
    url: str = BASE_URL + '/shadows'
    try:
        response: Response = get(url, headers=HEADERS)
    except (requests_exceptions.ConnectionError,
            url_exceptions.NewConnectionError):
        e: DasApplicationNotRunningError = (
            DasApplicationNotRunningError('Keyboard Driver'))
        e.elaborate()
        exit()
    for signal in loads(response.content):
        zone_id: str = signal['zoneId']
        delete(BASE_URL + '/pid/' + PID + '/zoneId/' + zone_id,
               headers=HEADERS)


def initiate_binding(binding: Process):
    binding.start()
    all_bindings.append(binding)


def main():
    """The Driver of the application that spawns a thread for each binding

    The Driver will fork once for each assistant, giving each assistant thier
    own thread. The main thread of the driver will continually parse the input
    from the user listening for the shutdown command

    NOTE: The driver can simply be run by navigating to this directory and
    running `./driver.py`

    NOTE: All assistants should be created in `init_assistants()` in
    `config.py`

    NOTE: Every assistant returned in the List from `init_assistants()` has
    thier binding managed by the driver - once an assistant is added to that
    list, there is nothing more needed to orchestrate an additional assistant
    """

    all_assistants: List[Assistant] = init_assistants()
    for assistant in all_assistants:
        initiate_binding(Process(target=assistant.create_binding))

    # infinte loop while the child processes run
    while 1:
        try:
            key = input('Press Q + <ENTER> to kill the driver:\n')
            if key == 'Q':
                raise KeyboardInterrupt
                return
        except KeyboardInterrupt:
            print('Shutting down...')
            kill_all_bindings()
            return
        else:
            print('Unexpected Input')


if __name__ == '__main__':
    main()
