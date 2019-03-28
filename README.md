# Prometheus-5Q

Simple application to elegantly handle illuminating a [Das Keyboard 5Q](https://www.daskeyboard.io) via the available API in a configurable way. This project is intended to provide the user with a litteny of useful `Assistant`s that can be bound to Das Keyboard 5Q keys, but also make it effortless to create additional custom `Assistant`s that integrate seamlessly with `Assistant`s provided here.

## Getting Started

To get started, all you need to do is clone the project and create a configuration file (config.py). There is an example configuration file provided (example_config.py) that can be used. If you wish to used the example configuration, you may copy the contents over to a config.py, but the values will need some tweaking to have the correct values for your enviornment. Next, ensure that you have the [Das Keyboard Dashboard](https://www.daskeyboard.io/get-started/software/) running. Once your configuration file is all set and your Das Keyboard Dashboard is running, you simply need to launch the driver by running `./driver.py` inside the project directory.

## Prerequisites

You should probably own a [Das Keyboard 5Q](https://www.daskeyboard.io), but you don't necessarily need to. You can still use this without the keyboard as long as you have the free [Das Keyboard Dashboard](https://www.daskeyboard.io/get-started/software/) downloaded and running.

This project requires Python 3.7+ along with the following libraries:

* psutil (5.5.1)
* GitPython (2.1.11)
* typing (3.6.6)

You can install these libraries by simply running `pip3 install -r requirements.txt` inside the project directory.

## The `Assistant` abstract class

### Overview

This project is built around the `Assistant` class. An `Assistant` is what creates a binding to a key and orchestrates what color is illuminated and what message is displayed. The `Assistant` identifies what state it is currently in, and then that state is used to determine what color and message is displayed. This color and message are only sent to the keyboard if the message/color are different from the current color/message that is displayed on the keyboard.

The `driver` handles binding each `Assistant` to their configured keys. When the `driver` is launched, it spawns a thread for each `Assistant`. Each of these threads calls the `Assistant`'s `create_binding()` method. This method will continually spawn new threads to evaluate the message and color and publish them if needed. The `Assistant` will wait a configured amount of seconds between spawning each thread. Meanwhile, the driver will then continually wait for the 'Q' keystroke to quit or the `KeyboardInterrupt` (CTRL + C): which will cause the driver to kill all spawned child threads and clear all active signals displaying on the keyboard.

Each `Assistant` requires the following inputs at least to operate:

```python
name (str)      # name of the `Assistant`
delay (str)     # the delay between evaluations
zone_id (str)   # the zone_id to bind the color to
is_muted (bool) # flag to deliver with no message
```

The `zone_id` can be created using the [Das Keyboard ZoneId Guide](https://www.daskeyboard.io/q-zone-id-explanation/). Any form of `zone_id` is valid since the `zone_id` is passed directly into the API. Each `Assistant` should bound to a unique `zone_id`.

This project includes an `Assistant` abstract class that all other `Assistant`s extend. This abstract class includes all the internals required for an `Assistant` to handle binding itself to a key with the given configuration.

### Making a Custom `Assistant`

Creating an additional custom `Assistant` is surprisingly easy in this architecture. All one needs to do is extend the `Assistant` abstract class and override the following methods:

```python
def state_identifier(self) -> str:
    raise OverrideError(self.name, 'state')

def message_identifier(self, state: str) -> str:
    raise OverrideError(self.name, 'message')

def color_identifier(self, state: str) -> str:
    raise OverrideError(self.name, 'color')
```

The `state_identifier` should accomplish the majority of the work for the `Assistant`. The `Assistant` base class handles passing the state that is returned from `state_identifier` directly to `message_identifier` and  `color_identifier` and publish those values to the keyboard if needed. The color returned from `color_identifier` should in hexidecimal form.

This project includes a template assistant (template_assistant.py) that provides an example template for creating a new custom `Assistant` that follows the same structure as all other `Assistant`s in this project.

It should be clear to the user which keys are bound to an `Assistant` at all times. Each `Assistant` is designed to keep the binded key illuminated no matter what state the `Assistant` is in (as long as the application is running). This architecture was built on this premise. If a notification is dismissed from the Das Keyboard Dashboard, the `Assistant` is programmed to republish it the next time it evaluates its own color and message.

### Binding a Custom `Assistant`

Once the `Assistant` has been created by overwriting the neccessary methods, binding it to a key is fairly simple if you know which key you would like it bound to. See the Das [Das Keyboard ZoneId Guide](https://www.daskeyboard.io/q-zone-id-explanation/) for selecting the desired `zone_id`. Add all the required values for your `Assistant` to config.py inside `init_assistants()`. Then, instantiate the assistant and append it to `all_assistants` before the list is returned. This is an example of the structure of adding assistants to config.py:

```python
from dummy_assistant import DummyAssistant

...

def init_assistants() -> List[Assistant]:
    all_assistants: List[Assistant] = []

    ...

    # example dummy_assistant
    EXAMPLE_DUMMY_NAME: str = 'Example Assistant'
    EXAMPLE_DUMMY_DELAY: int = 10
    EXAMPLE_DUMMY_ZONE_ID: str = '0,0'
    EXAMPLE_DUMMY_IS_MUTED: bool = False
    EXAMPLE_DUMMY_EXTRA_VARIABLE_1: bool = True
    EXAMPLE_DUMMY_EXTRA_VARIABLE_2: str = 'example'
    EXAMPLE_DUMMY: DummyAssistant = DummyAssistant(
        EXAMPLE_DUMMY_NAME,
        EXAMPLE_DUMMY_DELAY,
        EXAMPLE_DUMMY_ZONE_ID,
        EXAMPLE_DUMMY_IS_MUTED,
        EXAMPLE_DUMMY_EXTRA_VARIABLE_1,
        EXAMPLE_DUMMY_EXTRA_VARIABLE_2
    )
    all_assistants.append(EXAMPLE_DUMMY)

    ...
```

That's it! As long as the new assistant is included in the list returned from `init_assistants()`, then the Assistant will be successfuly handed over to the driver without any additional work. The `driver` will handle initiating the binding from there and will also handle killing the binding when the application is shutdown. I hope you enjoy using this as much as I have! Have fun!

## Authors

* **Matt Galloway** - 2019

## Acknowledgments

* [Das Keyboard 5Q](https://www.daskeyboard.io)
* [pipreqs](https://github.com/bndr/pipreqs)