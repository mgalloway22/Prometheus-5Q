from typing import Dict

"""General class for commonly used variables
"""

IS_DEBUG_MODE: bool = False
BASE_URL: str = 'http://localhost:27301/api/1.0/signals'
PID: str = 'DK5QPID'
HEADERS: Dict[str, str] = {'Content-type': 'application/json'}
COLORS: Dict[str, str] = {
    'red': '#CC0000',
    'orange': '#FF8000',
    'yellow': '#FFFF00',
    'light green': '#00CC00',
    'dark green': '#00FF00',
    'light blue': '#0000CC',
    'dark blue': '#0000FF',
    'purple': '#330033',
    'pink': '#FF0066',
    'error': '#FFFFFF',
}
