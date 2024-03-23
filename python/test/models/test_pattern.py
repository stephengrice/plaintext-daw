from plaintext_daw.models import Instrument, Note, Pattern
from plaintext_daw.models.instrument import InstrumentSource


class TestPattern:
    def test_init(self):
        obj = Pattern(instrument='hi', start=1, repeat=3)
        assert isinstance(obj, Pattern)
        assert obj.instrument == 'hi'
        assert obj.start == 1
        assert obj.repeat == 3
