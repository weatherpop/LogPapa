import unittest
import logging
import datetime
import sys
from StringIO import StringIO

from mock import Mock, patch, mock_open, MagicMock

sys.path.append("../..")

from LogPapa.base import LogProcessor

logging.basicConfig(level = logging.DEBUG)

class TestLogProcessor(unittest.TestCase):
    """unittest for TestLogProcessor"""

    def _mock_file_open(self):
        s_io = StringIO("FILE LINE 0")
        m = mock_open(read_data=s_io)
        def write(data):
            s_io.write(data)
        def read():
            return s_io.read()
        def readline():
            return s_io.readline()
        def seek(pos):
            s_io.seek(pos)
        def truncate(size=None):
            s_io.truncate(size=size)
        def s_io_iter(self):
            yield readline()
        m.return_value.write = write
        m.return_value.read = read
        m.return_value.readline = readline
        m.return_value.seek = seek
        m.return_value.truncate = truncate
        m.return_value.__iter__ = s_io_iter

        return m

    def setUp(self):
        self.proc_time = datetime.datetime(2014, 1, 1)

        self.m = self._mock_file_open()

        self.proc =  LogProcessor(
            "./test_result_file.txt", 
            self.proc_time)

    def tearDown(self):
        self.proc = None

    def test_mock_open(self):
        with patch("LogPapa.base.open", self.m, create=True):
            wf = self.proc._open_result_file()

            self.assertEqual(wf.readline(), "FILE LINE 0")
            wf.truncate(0)
            wf.write("FILE LINE 1")
            wf.seek(0)
            self.assertEqual(wf.readline(), "FILE LINE 1")

    def test_initialize(self):
        self.assertEqual(self.proc.name, "BaseLogProcessor")
        self.assertEqual(self.proc.stat_result_class, {})
        self.assertEqual(self.proc.process_time, self.proc_time)
        self.assertEqual(self.proc.result_file, "./test_result_file.txt")

    def test_writting_result(self):
        csv_result = []

        def write_mock(line):
            csv_result.append(line)

        wf = Mock()
        wf.write = write_mock

        stat_result = {
            "ERROR1" : 10, 
            "ERROR2" : 1, 
            }

        self.proc.writing_result(stat_result, wf)
        self.assertEqual(len(csv_result), 2)
        self.assertEqual(csv_result[0], "ERROR1,10\r\n")
        self.assertEqual(csv_result[1], "ERROR2,1\r\n")

    def test_process(self):
        with patch("LogPapa.base.open", self.m, create=True):
            self.proc.get_log_files = MagicMock(return_value=["1.txt", "2.txt"])
            self.proc.is_need_extract = MagicMock(return_value=True)
            self.proc.analysis_log_line = MagicMock()
            self.proc.writing_result = MagicMock()

            self.proc.process()

            self.proc.get_log_files.assert_called_with()
            self.proc.is_need_extract.assert_any_called_with("FILE LINE 0")
            self.proc.analysis_log_line.assert_any_called_with("FILE LINE 0")
            self.proc.writing_result.assert_any_called_with()


if __name__ == '__main__':
    unittest.main()
