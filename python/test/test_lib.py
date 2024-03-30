from plaintext_daw.lib import np_to_mp3, minmax_mapping
from plaintext_daw.models.synthesizer.envelope import ADSR
from plaintext_daw.models.synthesizer.rawclip import RawClip

import os

from plaintext_daw.models.synthesizer.wave import Wave, Sine


def test_min_max_mapping():
    sample_rate = 44100
    signal = RawClip(Wave([Sine(65.406, 2)]), ADSR(0.1, 0, 1, 0.1), duration=2).render(sample_rate)
    # assert signal.max() > 1 and signal.min() < -1
    signal = minmax_mapping(signal)
    assert signal.max() < 1 and signal.min() > -1


def test_convert_mp3():
    if os.path.exists("song.mp3"): os.remove("song.mp3")
    sample_rate = 44100
    signal = RawClip(Wave([Sine(65.406, 1)]), ADSR(0.1, 0, 1, 0.1), duration=2).render(sample_rate)
    np_to_mp3(signal, sample_rate, "song.mp3")

    assert os.path.exists("song.mp3")
    if os.path.exists("song.mp3"): os.remove("song.mp3")
