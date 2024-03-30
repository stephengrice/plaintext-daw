import os

import numpy as np

from plaintext_daw.cli import cli_entry_point
from plaintext_daw.lib import np_to_wav
from plaintext_daw.models.synthesizer import Synthesizer


def test_song1_render_local():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song1/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')

def test_song2_render_git():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song2/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')

def test_song3_synth():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song3/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')
