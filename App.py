from engine.Config import ConfigManager
import pygame as pg
from loguru import logger

from engine.Interface import InterfaceManager
from game.Camera import Camera
from game.world.World import World


class App:
    def __init__(self):
        pg.init()
        self.cfg = ConfigManager.load('cfg/config.json')

        if self.cfg['fullscreen']:
            import pyautogui
            self.w, self.h = pyautogui.size()
            logger.info(f'Fullscreen: {self.w}x{self.h}')
        else:
            try:
                self.w, self.h = self.cfg['resolution']
                logger.info(f'No fullscreen, using custom resolution: {self.w}x{self.h}')
            except KeyError:
                logger.warning('No resolution specified, using default: 800x600')
                self.w, self.h = 800, 600

        self.screen = pg.display.set_mode((self.w, self.h),
                                          (pg.FULLSCREEN if self.cfg['fullscreen'] else 0) | pg.DOUBLEBUF)
        logger.info('Created screen surface.')
        self.camera = Camera(self)
        self.world = World(self)
        self.clock = pg.time.Clock()
        self.running = True
        self.delta = 1 / self.cfg['fps'] if self.cfg['fps'] > 0 else 0
        self.font = pg.font.Font(None, 40)
        logger.info('App initialized.')

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw()
        if self.cfg['show-fps']:
            fps = self.font.render(f'{round(self.clock.get_fps(), 1)}', True, (255, 255, 255))
            self.screen.blit(fps, (0, 0))
        self.camera.move()
        InterfaceManager.draw()

    def _update(self):
        pg.display.flip()
        self.world.update()
        self.delta = self.clock.tick(self.cfg['fps']) / 1000
        InterfaceManager.update()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def run(self):
        logger.info('Running app...')
        while self.running:
            self._check_events()
            self._draw()
            self._update()
