import logging
import os


class Logger:

    def __init__(self, log_dir, log_level):
        self.LOG_LEVEL = log_level
        self.log_dir = log_dir

        self._make_log_directory()
        self._setup_logger()
        self._add_console_handler()

    def _make_log_directory(self):
        os.makedirs(self.log_dir, exist_ok=True)

    def _setup_logger(self):
        logging.basicConfig(level=self.LOG_LEVEL,
                            format=f"%(levelname)s %(filename)s - %(asctime)s - method: %(funcName)s|%(lineno)d ->"
                                   f"\n msg: %(message)s\n{'-' * 50}\n",
                            filename=self.log_dir + "logs.log"
                            )
        logging.getLogger("pika").setLevel(self.LOG_LEVEL)

    def _add_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.LOG_LEVEL)
        console_formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        logger = logging.getLogger()
        logger.addHandler(console_handler)
