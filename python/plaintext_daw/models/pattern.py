from typing import List

from .note import Note


class Pattern:
    
    def __init__(
        self,
        instrument: str,
        start: int,
        repeat: int,
    ):
        self.instrument = instrument
        self.start = start
        self.repeat = repeat
        self.notes: List[Note] = []
