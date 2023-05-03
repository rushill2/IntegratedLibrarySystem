from mainFragment import SampleApp
import sys
from PyQt5.QtWidgets import *
import logging
from config import logconfig
import os

logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO)
file_handler = loggingfile_handler = logging.FileHandler(os.path.join(logconfig.logPath, (
    logconfig.logFilename).replace('event', 'ILS')))
file_handler.setFormatter(logconfig.logFormat)
logger.addHandler(file_handler)

if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()
