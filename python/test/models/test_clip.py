import numpy as np

from plaintext_daw.models import Clip


class TestClip:
    def test_init(self):
        obj = Clip(np.array([1]), 1, 3)
        assert isinstance(obj, Clip)
        assert obj.data == np.array([1])
        assert obj.channels == 1
        assert obj.sample_rate == 3
