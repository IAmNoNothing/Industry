import math

from engine.vec import Vec2
import pygame as pg
from loguru import logger


class Camera:
    def __init__(self, app):
        self.app = app
        self.pos = Vec2(0, 0)
        self._vel = Vec2(0, 0)
        logger.info('Camera initialized.')

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self._vel.y -= self.app.cfg['speed']
        else:
            if keys[pg.K_s]:
                self._vel.y += self.app.cfg['speed']
            else:
                self._vel.y += math.copysign(self.app.cfg['speed'], -self._vel.y)\
                               * self.app.delta * self.app.cfg['slowdown']

        if keys[pg.K_a]:
            self._vel.x -= self.app.cfg['speed']
        else:
            if keys[pg.K_d]:
                self._vel.x += self.app.cfg['speed']
            elif abs(self._vel.x) > 10:
                self._vel.x += math.copysign(self.app.cfg['speed'], -self._vel.x) \
                               * self.app.delta * self.app.cfg['slowdown']

        self._vel = self._vel.clamp(-self.app.cfg['max-speed'], self.app.cfg['max-speed'])
        if abs(self._vel.x) < 10:
            self._vel.x = 0
        if abs(self._vel.y) < 10:
            self._vel.y = 0
        # draw self._vel on screen
        text = self.app.font.render(f'Vel: {self._vel}', True, (255, 255, 255))
        self.app.screen.blit(text, (0, 50))
        self.pos += self._vel * self.app.delta
