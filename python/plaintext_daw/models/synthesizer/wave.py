# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 16:09
# @Author  : LTstrange

import numpy as np
from enum import Enum
from typing import List


class WaveType(Enum):
    sine = 1


class PrimitiveWave:
    def __init__(self, wave_type: WaveType, amplitude: float):
        self.wave_type = wave_type
        self.amplitude = amplitude

    def render(self, duration: float, sample_length: int) -> np.ndarray:
        raise NotImplementedError


class Wave:
    def __init__(self, primitive_waves: List[PrimitiveWave]):
        self.primitive_waves = primitive_waves

    def render(self, duration: float, sample_length: int):
        wave = np.zeros(sample_length)
        for primitive in self.primitive_waves:
            wave += primitive.render(duration, sample_length)

        return wave


class Sine(PrimitiveWave):
    def __init__(self, base_freq: float, amplitude: float):
        super().__init__(WaveType.sine, amplitude)
        self.base_freq = base_freq

    def render(self, duration: float, sample_length: int):
        t = np.linspace(0, duration, sample_length)
        return np.sin(2 * np.pi * self.base_freq * t)
