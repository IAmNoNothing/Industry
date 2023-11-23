import datetime

from App import App
from loguru import logger

if __name__ == '__main__':
    logger.add(f'logs/{datetime.datetime.today().strftime("%Y-%m-%d")}.log')
    logger.info('Running game...')
    App().run()
    logger.success('Game finished!')
