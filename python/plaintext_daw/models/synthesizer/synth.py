from typing import Dict, List, Tuple, Union
import re
import numpy as np
import yaml

from .wave import Sine, Wave
from .rawclip import RawClip
from .envelope import ADSR

from plaintext_daw.models import Clip, Note


class Synthesizer:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.__effects: list = []
        self.__clips: Dict[str, Dict[str, float]] = dict()

    def set_pipeline(self, config):
        self.__effects = config

    def set_clips(self, config: dict):
        self.__clips = config

    def get_clip(self, note: Note, bpm: int) -> Union[Clip, None]:
        if note.value not in self.__clips:
            return None
        clip = self.__pipeline(self.__clips[note.value])
        seconds = note.length * 60 / bpm
        clip.set_duration(seconds)
        rawdata = clip.render(self.sample_rate)
        return Clip(rawdata, 1, self.sample_rate)

    def __pipeline(self, actual_param: Dict[str, float]) -> RawClip:
        result = None
        for effect in self.__effects:
            effect, form_param = re.match(r"(\w+)(?:\((.+)\))?", effect).groups()
            form_param = form_param.split(',')
            if effect == 'sin' and form_param[0] == 'frequency':
                result = Wave([Sine(actual_param[form_param[0]], 1)])
            elif effect == "ADSR" and len(form_param) == 4:
                form_param = [float(p) for p in form_param]
                result = RawClip(result, ADSR(*form_param))
        return result
