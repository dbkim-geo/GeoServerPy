from datetime import datetime

class Logger():
    def __init__(self):
        pass
    
    def writeLog(self, message):
        now = datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        log = f'[{nowDatetime}] {message}'

        with open('log.csv', 'a') as f:
            f.write(f'\n')
            f.write(f'{log}')

        return print(log)