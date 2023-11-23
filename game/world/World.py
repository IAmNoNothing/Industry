import sys
import time
from engine.Config import ConfigManager
from engine.Generator import Generator
from engine.vec import Vec2
from game.world.Block import Block
from game.world.Chunk import Chunk
from loguru import logger
import pygame as pg


class World:
    def __init__(self, app) -> None:
        self.app = app
        self.cfg = ConfigManager.load('cfg/world.json')
        self.images = self.load_assets()
        self.rotated_images = self.cache_image_rotations()
        logger.info('Generating world...')
        self.generator = Generator(self.cfg['generator'])
        self.chunks = self.generate()
        logger.info('World generated.')
        self.visible = self.calculate_visible_chunks()
        logger.info('World initialized.')

    def generate(self) -> list[Chunk, ...]:
        chunks = []

        logger.info(f'Generating {self.cfg["w"] * self.cfg["h"]} chunks...')
        start = time.time()
        for y in range(self.cfg['h']):
            for x in range(self.cfg['w']):
                ch = Chunk(self, Vec2(x, y))
                ch.generate()
                chunks.append(ch)
        logger.info(f'World generation took {time.time() - start}s')

        return chunks

    def calculate_visible_chunks(self):
        visible = []
        for chunk in self.chunks:
            if -self.cfg['cw'] * self.cfg['block-size'] <= chunk.s_topleft.x - self.app.camera.pos.x < self.app.w and \
                    -self.cfg['ch'] * self.cfg['block-size'] <= chunk.s_topleft.y - self.app.camera.pos.y < self.app.h:
                visible.append(chunk)

        return visible

    def get_chunk_at(self, chunk_x, chunk_y) -> Chunk | None:
        if not (0 <= chunk_x < self.cfg['w'] and 0 <= chunk_y < self.cfg['h']):
            logger.warning(f'Invalid chunk coordinates: {chunk_x}, {chunk_y} '
                           f'for world with size {self.cfg["w"]}x{self.cfg["h"]}, ignoring...')
            return None
        return self.chunks[chunk_y * self.cfg['w'] + chunk_x]

    def get_block_at(self, block_x, block_y) -> Block:
        if not (0 <= block_x < self.cfg['cw'] * self.cfg['w'] and 0 <= block_y < self.cfg['ch'] * self.cfg['h']):
            logger.error(f'Invalid block coordinates: {block_x}, {block_y} '
                         f'for world block size {self.cfg["cw"] * self.cfg["w"]}x{self.cfg["ch"] * self.cfg["h"]}')
            sys.exit(1)
        return self.get_chunk_at(block_x % self.cfg['cw'], int(block_y // self.cfg['cw'])) \
            .get_block_at(block_x, block_y)

    def load_assets(self):
        logger.info('Loading assets...')
        start = time.time()
        images = [
            pg.transform.scale(pg.image.load(asset).convert_alpha(),
                               (self.cfg['block-size'], self.cfg['block-size']))
            for asset in self.cfg['textures']
        ]
        logger.info(f'Loaded {len(images)} textures in {time.time() - start}s')

        return images

    def cache_image_rotations(self) -> tuple:
        images = []

        logger.info('Caching image rotations...')
        for image in self.images:
            images.append(tuple(pg.transform.rotate(image, i * 90) for i in range(4)))

        return tuple(images)

    def draw(self):
        self.visible = self.calculate_visible_chunks()
        for chunk in self.visible:
            chunk.draw()
