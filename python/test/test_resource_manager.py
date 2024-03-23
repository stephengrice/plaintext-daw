from unittest import mock
from unittest.mock import call, patch

import numpy as np
import pytest
from plaintext_daw.models.clip import Clip

from plaintext_daw.models.instrument import Instrument, InstrumentSource
from plaintext_daw.models.note import Note
from plaintext_daw.models.pattern import Pattern
from plaintext_daw.models.song import Song

from plaintext_daw.resource_manager import ResourceManager


class TestResourceManager:

    def setup_method(self, test_method):
        self.rm = ResourceManager('.')

    def test_working_dir(self):
        assert self.rm.working_dir == '.'

    def test_check_types(self):
        config = {
            'foo': 'val1',
            'bar': 'val2',
        }
        ResourceManager.check_types(config, ['foo', 'bar'])
        with pytest.raises(ValueError, match='baz'):
            ResourceManager.check_types(config, ['foo', 'bar', 'baz'])

    @patch.object(ResourceManager, 'get_clip')
    @patch.object(ResourceManager, 'get_instrument')
    @patch.object(ResourceManager, 'get_pattern')
    def test_get_song(self, mock_get_pattern, mock_get_instrument, mock_get_clip):
        with pytest.raises(ValueError):
            self.rm.get_song({'bpm': 100})

        clip_dict = {
            'costco': {'pancake': 'wait'},
            'walmart': {'no': 'free samples'},
        }
        ins_dict = {
            'myins': {'field': 'hello'},
            'yourins': {'name': 'insurance??'},
        }
        pattern_dict = {
            'pattern': {'hey': 'there'},
            'other': {'angle': 'momentum'},
        }
        song = self.rm.get_song({
            'bpm': 100,
            'sample_rate': 44100,
            'clips': clip_dict,
            'instruments': ins_dict,
            'patterns': pattern_dict,
        })
        assert isinstance(song, Song)
        assert song.bpm == 100
        assert song.sample_rate == 44100
        mock_get_clip.assert_has_calls([
            call(clip_dict['costco']),
            call(clip_dict['walmart']),
        ])
        mock_get_instrument.assert_has_calls([
            call(ins_dict['myins']),
            call(ins_dict['yourins']),
        ])
        mock_get_pattern.assert_has_calls([
            call(pattern_dict['pattern']),
            call(pattern_dict['other']),
        ])

    def test_get_clip_no_type(self):
        with pytest.raises(ValueError):
            self.rm.get_clip({})
        with pytest.raises(ValueError):
            self.rm.get_clip({'type': 'something crazy'})

    def test_get_clip_wav(self):
        # Good config
        wav_path = 'test/data/song1/piano/Piano-A0.ogg.wav'
        config = {
            'type': 'wav',
            'path': wav_path,
        }
        clip = self.rm.get_clip(config)
        assert isinstance(clip, Clip)
        assert isinstance(clip.data, np.ndarray)
        assert clip.channels == 1
        assert clip.sample_rate == 44100

        # Missing fields

    @patch.object(ResourceManager, 'get_clip')
    def test_get_instrument(self, mock_get_clip):
        clips_dict = {
            'A0': {'path': 'path/to/A0.wav'},
            'C5': {'path': 'path/to/C5.wav'},
        }
        instrument = self.rm.get_instrument({
            'clips': clips_dict,
            'type': 'wav'
        })
        assert isinstance(instrument, Instrument)
        assert instrument.source == InstrumentSource.IN_PLACE
        assert instrument.type == 'wav'
        mock_get_clip.assert_has_calls([
            call(clips_dict['A0']),
            call(clips_dict['C5']),
        ])

    @patch.object(ResourceManager, 'clone_repo')
    @patch.object(ResourceManager, 'get_config_from_file', return_value={
        'clips': {
            'A4': {
                'path': 'samples/A4.wav',
            },
            'A#4': {
                'path': 'samples/A#4.wav',
            },
        },
    })
    @patch.object(ResourceManager, 'get_clip')
    def test_get_instrument_git(self, mock_get_clip, mock_get_config_from_file, mock_clone_repo):
        the_repo = 'git@gitub.com:pagekeytech/plaintext-daw-instruments'
        instrument = self.rm.get_instrument({
            'source': 'GIT',
            'repo': the_repo,
            'ref': 'master',
            'path': 'piano/instrument.yml',
        })
        assert instrument.source == InstrumentSource.GIT
        assert instrument.repo == the_repo
        assert instrument.ref == 'master'
        assert instrument.path == 'piano/instrument.yml'
        mock_clone_repo.assert_called_with(the_repo, 'master')
        mock_get_config_from_file.assert_called_with('.ptd-cache/plaintext-daw-instruments/piano/instrument.yml')
        mock_get_clip.assert_has_calls([
            call({'path': '.ptd-cache/plaintext-daw-instruments/piano/samples/A4.wav'}),
            call({'path': '.ptd-cache/plaintext-daw-instruments/piano/samples/A#4.wav'}),
        ])

    @patch.object(ResourceManager, 'get_note')
    def test_get_pattern(self, mock_get_note):
        notes = [
            {'value': 'A0', 'start': 0, 'length': 1},
            {'value': 'A1', 'start': 1, 'length': 2},
        ]
        pattern = self.rm.get_pattern({
            'instrument': 'piano',
            'start': 12,
            'repeat': 0,
            'notes': notes,
        })
        assert isinstance(pattern, Pattern)
        assert pattern.start == 12
        assert pattern.repeat == 0
        mock_get_note.assert_has_calls([call(n) for n in notes])

    def test_get_pattern(self):
        note = self.rm.get_note({
            'value': 'C5',
            'start': 7,
            'length': 3,
        })
        assert isinstance(note, Note)
        assert note.value == 'C5'
        assert note.start == 7
        assert note.length == 3

    @patch('plaintext_daw.resource_manager.os.makedirs')
    @patch('plaintext_daw.resource_manager.os.path.exists', return_value=False)
    @patch('plaintext_daw.resource_manager.subprocess.check_call')
    def test_clone_repo(self, mock_check_call, mock_exists, mock_makedirs):
        the_repo = 'git@gitub.com:pagekeytech/plaintext-daw-instruments'
        self.rm.working_dir = 'wdir'
        self.rm.clone_repo(the_repo, 'master')
        mock_makedirs.assert_called_with('wdir/.ptd-cache', exist_ok=True)
        mock_exists.assert_called_with('wdir/.ptd-cache/plaintext-daw-instruments')
        mock_check_call.assert_has_calls([
            call(['git', 'clone', the_repo], cwd='wdir/.ptd-cache'),
            call(['git', 'checkout', 'master'], cwd='wdir/.ptd-cache/plaintext-daw-instruments'),
        ])
        self.rm.working_dir = '.'

    @patch('plaintext_daw.resource_manager.yaml.safe_load')
    def test_get_config_from_file(self, mock_safe_load):
        mock_open = mock.mock_open(read_data='file data')
        with mock.patch('builtins.open', mock_open):
            self.rm.get_config_from_file('file.yml')
            mock_open.assert_called_with('./file.yml')
            self.rm.working_dir = 'hello'
            self.rm.get_config_from_file('file.yml')
            mock_open.assert_called_with('hello/file.yml')
            self.rm.working_dir = '.'
