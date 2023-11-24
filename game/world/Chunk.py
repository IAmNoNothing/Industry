import math
import pygame as pg
from loguru import logger
from random import randrange as rand
from engine.vec import Vec2
from game.world.Block import Block


class Chunk:
    def __init__(self, world, world_pos):
        self.world = world
        self.pos = world_pos
        self.b_size = world.cfg['block-size']
        self.blocks = self.generate()
        self.s_topleft = self.pos * (self.world.cfg['cw'], self.world.cfg['ch']) * self.b_size

    def generate(self) -> list[Block, ...]:
        blocks = []

        generator = self.world.generator
        chunk_topleft = self.pos * self.world.cfg['cw'] * self.world.cfg['block-size']

        for y in range(self.world.cfg['ch']):
            for x in range(self.world.cfg['cw']):
                gx = (self.pos.x * self.world.cfg['cw'] + x) / self.world.cfg['cw'] * self.world.cfg['w']
                gy = (self.pos.y * self.world.cfg['ch'] + y) / self.world.cfg['ch'] * self.world.cfg['w']
                _type = generator.noise2d(gx, gy)
                _type = _type * 0.5 + 0.5  # [-1, 1] -> [0, 1]
                screen_pos = chunk_topleft + Vec2(x, y) * self.b_size
                index = min(math.floor(_type * len(self.world.images)), len(self.world.images) - 1)
                bl = Block(x, y, self, _type,
                           index,
                           int(screen_pos.x), int(screen_pos.y), rand(0, 4))
                blocks.append(bl)

        return blocks

    def get_block_at(self, x, y) -> Block | None:
        try:
            return self.blocks[y * self.world.cfg['cw'] + x]
        except IndexError:
            return None

    def draw(self):
        for block in self.blocks:
            pos = Vec2(block.sx, block.sy) - self.world.app.camera.pos
            if self.world.app.cfg['white-black']:
                c = int(block.type_ * 255), int(block.type_ * 255), int(block.type_ * 255)
                pg.draw.rect(self.world.app.screen, c, (*pos, self.b_size, self.b_size))
            else:
                self.world.app.screen.blit(self.world.rotated_images[block.sprite][block.rot_index], pos)
