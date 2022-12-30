import os, datetime
import logging

if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("data"):
    os.makedirs("data")

logPath = os.path.join("logs")
jsonPath = os.path.join("data")

logFilename = 'integrated-library-' + datetime.datetime.now().strftime('%d-%b-%Y-%H-%M') + '.log'
logFormat = logging.Formatter('%(asctime)s :: %(levelname)s : %(name)s: %(message)s', datefmt = '%H:%M:%S')