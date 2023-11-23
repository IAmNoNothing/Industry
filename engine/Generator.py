from loguru import logger
from perlin_noise import PerlinNoise
from random import randrange as rand


class Generator:
    def __init__(self, settings: list[dict, ...], seed: int = rand(0, 2**32 - 1)):
        for setting in settings:
            if 'seed' not in setting.keys():
                setting['seed'] = seed

        self.gen = [PerlinNoise(**settings[i]) for i in range(len(settings))]
        logger.info(f'Generator initialized. Seed={seed}.')

    def noise2d(self, x, y):
        return sum(self.gen[i]([x, y]) for i in range(len(self.gen)))

    def noise(self, *args):
        return sum(self.gen[i](args) for i in range(len(self.gen)))
