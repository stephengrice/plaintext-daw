# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 15:14
# @Author  : LTstrange

from .envelope import Envelope
from .wave import Wave


class RawClip:
    def __init__(self, source: Wave, envelope: Envelope, duration: float = None):
        self.source = source
        self.envelope = envelope
        self.duration = duration

    def set_duration(self, duration: float):
        self.duration = duration

    def render(self, sample_rate: float):
        if self.duration is None:
            raise "No duration defined. use `Clip.set_duration()`"
        return self.envelope(self.source, self.duration, sample_rate)
