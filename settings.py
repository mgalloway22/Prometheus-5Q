from typing import Dict

"""General class for commonly used variables
"""

IS_DEBUG_MODE: bool = True
BASE_URL: str = 'http://localhost:27301/api/1.0/signals'
PID: str = 'DK5QPID'
HEADERS: Dict[str, str] = {'Content-type': 'application/json'}
COLORS: Dict[str, str] = {
    'red': '#CC0000',
    'orange': '#E67E22',
    'yellow': '#F1C40F',
    'light green': '#00CC00',
    'dark green': '#186A3B',
    'light blue': '#3498DB',
    'dark blue': '#1B4F72',
    'purple': '#9900CC',
    'pink': '#EC7063',
    'error': '#FFFFFF',
}
