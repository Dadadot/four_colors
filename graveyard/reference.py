from typing import Optional
from enum import Enum, auto

class GVStates(Enum):
    NEW = auto()
    SELECT = auto()


class RefGVStates:
    clear_text = {GVStates.NEW: "New", GVStates.SELECT: "Edit"}

    @staticmethod
    def by_clear_text(clear_text: str) -> Optional[GVStates]:
        #perfection
        try:
            state = [k for k, v in RefGVStates.clear_text.items() if v == clear_text][0]
            return state
        except:
            return None
