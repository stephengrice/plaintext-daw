# -*- coding: utf-8 -*-
# @Time    : 2023/2/15 14:19
# @Author  : LTstrange
from plaintext_daw.models import Note
from plaintext_daw.models.synthesizer import Synthesizer


def test_synth_init():
    synth = Synthesizer(44100)
    assert synth.sample_rate == 44100


def test_synth_set_clips():
    synth = Synthesizer(44100)
    clips = {"a": "b"}
    synth.set_clips(clips)

    assert synth._Synthesizer__clips == {"a": "b"}


def test_synth_set_pipeline():
    synth = Synthesizer(44100)
    pipeline = ["sin(frequency)", "ADSR(0.1, 0.1, 0.7, 0.1)"]
    synth.set_pipeline(pipeline)

    assert synth._Synthesizer__effects == ["sin(frequency)", "ADSR(0.1, 0.1, 0.7, 0.1)"]


def test_synth_get_clip():
    synth = Synthesizer(44100)
    synth.set_clips({"a": {"frequency": 0}})
    synth.set_pipeline(["sin(frequency)", "ADSR(0.1, 0.1, 0.7, 0.1)"])
    clip = synth.get_clip(Note("a"), 100)

    assert clip.sample_rate == 44100
    assert clip.channels == 1
    assert all(clip.data) == 0
