import json
from loguru import logger


class ConfigManager:
    @staticmethod
    def load(path) -> dict:
        logger.info(f'Loading config from {path}...')
        with open(path) as f:
            content = json.load(f)
        return content

    @staticmethod
    def save(path, content):
        logger.info(f'Saving config to {path}...')
        with open(path, 'w') as f:
            json.dump(content, f)
