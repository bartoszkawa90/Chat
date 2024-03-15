import datetime


class Logger:
    @staticmethod
    def info(message: str = '') -> None:
        print(f'[{datetime.datetime.now()}] [INFO] : {message}')

    @staticmethod
    def warning(message: str = '') -> None:
        print(f'[{datetime.datetime.now()}] [WARNING] : {message}')

    @staticmethod
    def debug(message: str = '') -> None:
        print(f'[{datetime.datetime.now()}] [DEBUG]  : {message}')

    @staticmethod
    def error(message: str = '') -> None:
        print(f'[{datetime.datetime.now()}] [ERROR]  : {message}')

    @staticmethod
    def critical(message: str = '') -> None:
        print(f'[{datetime.datetime.now()}] [CRITICAL]  : {message}')
