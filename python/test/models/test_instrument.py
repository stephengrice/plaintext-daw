from plaintext_daw.models import Instrument
from plaintext_daw.models.instrument import InstrumentSource


class TestInstrument:
    def test_init(self):
        obj = Instrument()
        assert isinstance(obj, Instrument)
        assert obj.source == InstrumentSource.IN_PLACE
