import time
from log.logger import Logger

class Timer():
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger = Logger()

        self.end = time.time()
        self.interval = self.end - self.start

        logger.writeLog(f'elapsed time: {self.interval} sec\n')

    