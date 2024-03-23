from plaintext_daw.models import Instrument, Pattern, Clip, Song


class TestSong:
    def test_init(self):
        song = Song(100, 44100)
        assert isinstance(song, Song)
        assert song.bpm == 100
        assert song.sample_rate == 44100
