class Note:
    
    def __init__(
        self,
        value: str = '',
        start: float = 0,
        length: float = 1,
    ):
        self.value = value
        self.start = start
        self.length = length

    @staticmethod
    def beats_to_samples(beats, bpm, sample_rate):
        return int(beats*(60/bpm)*sample_rate)

    def get_start_sample(self, bpm, sample_rate):
        return Note.beats_to_samples(self.start, bpm, sample_rate)

    def get_end_sample(self, bpm, sample_rate):
        beat = self.start + self.length
        return Note.beats_to_samples(beat, bpm, sample_rate)
