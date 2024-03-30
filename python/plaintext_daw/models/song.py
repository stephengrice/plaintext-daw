from typing import Dict

import numpy as np

from ..lib import np_to_wav
from .instrument import Instrument
from .pattern import Pattern
from .clip import Clip


class Song:

    def __init__(
        self,
        bpm: int,
        sample_rate: int,
    ):
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.instruments: Dict[str, Instrument] = {}
        self.patterns: Dict[str, Pattern] = {}
        self.clips: Dict[str, Clip] = {}

    def render(self, out_filename: str):
        # Aggregate notes into a single list
        # Eventually, this approach will need to be upgraded when patterns have an offset too
        # For now, it works
        all_notes = []
        for pattern_name, pattern in self.patterns.items():
            for note in pattern.notes:
                all_notes.append(note)
        
        # Figure out how many samples the final render will be
        # end_sample = max([n.get_end_sample(self.sample_rate, self.bpm) for n in all_notes])
        
        # Allocate an np array for the entire song
        song_data = np.zeros(1)
        
        # TODO support more options than just these defaults
        channels = 1
        sample_width = 2
        sample_rate = self.sample_rate
        
        for note in all_notes:
            # Get the raw audio data for this note
            instrument = self.instruments[pattern.instrument]
            clip = instrument.get_clip(note, self.bpm)
            if clip is not None: # only render note if found
                # Compute sample start/end
                start = note.get_start_sample(self.bpm, self.sample_rate)
                end = note.get_end_sample(self.bpm, self.sample_rate)
                # If end is past clip end, then make end at the clip end
                if end-start > len(clip.data):
                    end = start + len(clip.data)
                # If end is past the song end, pad out the rest of the song with zeros
                num_new_samples = end - len(song_data)
                if num_new_samples > 0:
                    song_data = np.pad(song_data, (0, num_new_samples))
                # Put it in the song at the right place
                song_data[start:end] += clip.data[0:end-start]
        np_to_wav(song_data, channels, sample_width, sample_rate, out_filename)
