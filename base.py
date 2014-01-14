import logging
import csv

class LogProcessor(object):
    """log processor base class"""

    name = "BaseLogProcessor"   # the name of processor
    stat_result_class = {}      # log times statistic result dictionary

    def __init__(self, result_file, process_time):
        super(LogProcessor, self).__init__()
        self.result_file = result_file
        self.logger = logging.getLogger("LogPapa")
        self.process_time = process_time

    def get_log_files(self):
        """
        (for overriding)
        get all log files for analysising, should return a list of str

        @return (list) files' path
        """
        raise NotImplementedError(
            "you need to implement the fucntion [get_log_files] for your LogProcessor subclass")

    def is_need_extract(self, line):
        """
        (for overriding)
        determine whether the log line need to be extracted

        :param(line): the log line

        @return (boolean) whether the log line need to be extracted
        """
        raise NotImplementedError(
            "you need to implement the fucntion [is_need_extract] for your LogProcessor subclass")        

    def analysis_log_line(self, line):
        """
        (for overriding)
        analysis the log line and record it in stat_dict

        :param(line): the log line

        no return value
        """
        raise NotImplementedError(
            "you need to implement the fucntion [analysis_log_line] for your LogProcessor subclass")        

    def writing_result(self, stat_dict):
        """
        (for overriding)
        write the statistic result into file

        :param(stat_dict): the statistic result

        no return value        
        """
        with open(self.result_file, "wb") as wf:
            writer = csv.writer(wf)
            writer.writerows([[k.strip(), str(v).strip()] for k, v in stat_dict.items()])

    def process(self):
        """
        the main processing logic
        """

        # 1.get all log files
        self.logger.info("getting log files...")
        file_paths = self.get_log_files()

        # 2.loop the log files, extract and analysis every log line
        for file_path in file_paths:
            with open(file_path, "r") as rf:
                self.logger.info("process log file => [%s]...", file_path)
                for line in rf:
                    if self.is_need_extract(line):
                        self.analysis_log_line(line)

        # 3.write the statistic result into file
        self.logger.info("writing stat result => [%s]...", self.result_file)
        self.writing_result(self.stat_result_class)
