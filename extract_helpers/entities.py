from typing import Dict
from glom import glom, PathAccessError

from helpers import Logger


logger = Logger()


def get_entities(data: Dict) -> Dict:
    paths = [
        "data.user.result.timeline.timeline.instructions.0.entries",
        "data.user.result.timeline.timeline.instructions.3.entries"
    ]
    
    for path in paths:
        try:
            return glom(data, path)
        except PathAccessError:
            continue
