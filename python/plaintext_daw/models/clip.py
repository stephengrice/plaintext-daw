import numpy as np


class Clip:

    def __init__(
        self,
        data: np.ndarray,
        channels: int,
        sample_rate: int,
    ):
        self.data = data
        self.channels = channels
        self.sample_rate = sample_rate
