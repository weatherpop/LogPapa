import unittest
import logging
import datetime
import sys

sys.path.append("../..")

from LogPapa.processor import DateTailLogProcessor

logging.basicConfig(level = logging.DEBUG)

class TestDateTailLogProcessor(unittest.TestCase):
    """unittest for TestDateTailLogProcessor"""

    def setUp(self):
        self.proc_time = datetime.datetime(2014, 1, 1)

        self.proc =  DateTailLogProcessor(
            "ERROR|WARN", 
            result_file="./unittest.csv",
            process_time=self.proc_time,
            ignore_info_regix=[r"\[[\d\s\:\-]+\]", r"\:[\d]+"],
            stat_key_regex=r"[\w\W]*",
            file_glob="*.log")

    def tearDown(self):
        pass

    def test_initialize(self):
        self.assertEqual(self.proc.name, "DateTailProcessor")
        self.assertEqual(self.proc.process_time, self.proc_time)
        self.assertEqual(self.proc.result_file, "./unittest.csv")
        self.assertEqual(self.proc.key_regex_compiled.pattern, "ERROR|WARN")
        self.assertEqual(self.proc.ignore_info_regex_compiled[0].pattern, r"\[[\d\s\:\-]+\]")
        self.assertEqual(self.proc.ignore_info_regex_compiled[1].pattern, r"\:[\d]+")
        self.assertEqual(self.proc.stat_key_regex_compiled.pattern, r"[\w\W]*")
        self.assertEqual(self.proc.file_glob, "*.log")

    def test_is_need_extract(self):
        self.assertEqual(self.proc.is_need_extract("[2013-01-01 01:01:01]ERROR:1"), True)
        self.assertEqual(self.proc.is_need_extract("[2013-01-01 01:01:01]Error:1"), True)
        self.assertEqual(self.proc.is_need_extract("[2013-01-01 01:01:01]WARN:1"), True)
        self.assertEqual(self.proc.is_need_extract("[2013-01-01 01:01:01]Warn:1"), True)
        self.assertEqual(self.proc.is_need_extract(""), False)
        self.assertEqual(self.proc.is_need_extract("   "), False)
        self.assertEqual(self.proc.is_need_extract(" W A R N "), False)

    def test_analysis_log_line(self):
        for i in range(0, 100):
            if i % 2 == 0:
                self.proc.analysis_log_line("[2014-01-21 00:00:00]ERROR:%d" % i)
            else:
                self.proc.analysis_log_line("[2014-01-21 00:00:00]WARN:%d" % i)

        self.assertEqual(self.proc.stat_result_class["ERROR"], 50)
        self.assertEqual(self.proc.stat_result_class["WARN"], 50)

if __name__ == '__main__':
    unittest.main()
