import re
import glob
import datetime

from base import LogProcessor

class DateTailLogProcessor(LogProcessor):
    """date tail log (plain text file) analysis processor"""

    name = "DateTailProcessor"
    stat_result_class = {}

    def __init__(
        self, key_regex, result_file="./DateTailLogStat.csv",
        process_time=datetime.datetime.now(), ignore_info_regix=[], 
        stat_key_regex="[\w\W]*", file_glob="*.log"):
    
        """
        initialization the processor

        :param(key_regex) : the regex of the log line extracting key
        :param(result_file) : the statistic result file path
        :param(process_time) : the processing time
        :param(ignore_info_regix) : the regex to replace log line dynamic part
        :param(stat_key_regex) : the key of the log line for statistic dictionary
        :param(file_glob) : the glob to find the log files
        """

        self.key_regex = key_regex
        self.ignore_info_regix = ignore_info_regix
        self.stat_key_regex = stat_key_regex
        self.file_glob = file_glob

        self.key_regex_compiled = re.compile(key_regex, re.IGNORECASE)
        self.ignore_info_regex_compiled = \
            [re.compile(e, re.IGNORECASE) for e in ignore_info_regix] if ignore_info_regix else []
        self.stat_key_regex_compiled = \
            re.compile(stat_key_regex, re.IGNORECASE) if stat_key_regex else None

        self.file_path_list = []

        super(DateTailLogProcessor, self).__init__(result_file, process_time)

    def get_log_files(self):
        return glob.glob(self.file_glob)

    def is_need_extract(self, line):
        if self.key_regex_compiled.search(line):
            return True

        return False

    def analysis_log_line(self, line):
        # transform the info format
        if self.ignore_info_regex_compiled:
            for r in self.ignore_info_regex_compiled:
                line = r.sub("", line)

        # search the log key
        stat_key_result = self.stat_key_regex_compiled.search(line)
        stat_key = stat_key_result.group(0)

        if not stat_key:
            stat_key = ""

        # insert into the stat dict
        if stat_key not in self.stat_result_class:
            self.stat_result_class[stat_key] = 0

        self.stat_result_class[stat_key] += 1
