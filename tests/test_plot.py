import unittest
import datetime
from channelarchiver import Archiver, utils
from tests.mock_archiver import MockArchiver
import pytest

utc = utils.UTC()
local_tz = utils.local_tz

class TestArchiverPlot(unittest.TestCase):

    def setUp(self):
        self.archiver = Archiver('https://xf23id-ca/cgi-bin/ArchiveDataServer.cgi')
        self.archiver.archiver = MockArchiver()

    def test_plot(self):
        try:
            import matplotlib
        except ImportError:
            pytest.skip("This test requires matplotlib.")
        from channelarchiver import plot_channels
        start = datetime.datetime(2012, 1, 1, tzinfo=utc)
        end = datetime.datetime(2013, 1, 1, tzinfo=utc)
        plot_channels.plot(self.archiver,'EXAMPLE:DOUBLE_SCALAR{TD:1}', 'EXAMPLE:INT_WAVEFORM', start, end)





if __name__ == '__main__':
    unittest.main()
