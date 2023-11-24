import sys
import time
from engine.Config import ConfigManager
from engine.Generator import Generator
from engine.Interface import Interface
from engine.vec import Vec2
from game.world.Block import Block
from game.world.Chunk import Chunk
from loguru import logger
import pygame as pg


class World:
    def __init__(self, app) -> None:
        self.app = app
        self.cfg = ConfigManager.load('cfg/world.json')
        self.chosen_block_img = pg.transform.scale_by(pg.image.load('assets/chosen.png').convert_alpha(), 2)
        self.images = self.load_assets()
        self.rotated_images = self.cache_image_rotations()
        logger.info('Generating world...')
        self.generator = Generator(self.cfg['generator'])
        self.chunks = self.generate()
        logger.info('World generated.')
        self.visible = self.calculate_visible_chunks()
        self.chosen_block = None  # warn: add `not None` check
        self.interface_props = self.cfg['info-panel-props']
        self.interface_props.update({'screen': self.app.screen})
        self.interface_props.update({'rect': pg.Rect(self.cfg['info-panel-rect'])})
        self.interface = Interface(self.cfg['info-panel-rect'], self.interface_props)
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

    def get_block_at(self, block_x, block_y) -> Block | None:
        if chunk := self.get_chunk_at(int(block_x // self.cfg['cw']), int(block_y // self.cfg['cw'])):
            return chunk.get_block_at(block_x, block_y)
        return None

    def load_assets(self):
        logger.info('Loading assets...')
        start = time.time()
        images = [
            pg.transform.scale(pg.image.load(asset).convert_alpha(),
                               (self.cfg['block-size'], self.cfg['block-size']))
            for asset in self.cfg['textures']
        ]
        if not self.chosen_block_img:
            logger.error('Chosen block image not found!')
            sys.exit(1)
        logger.info(f'Loaded {len(images)} textures in {time.time() - start}s')

        return images

    def cache_image_rotations(self) -> tuple:
        images = []

        logger.info('Caching image rotations...')
        for image in self.images:
            images.append(tuple(pg.transform.rotate(image, i * 90) for i in range(4)))

        return tuple(images)

    def draw(self):
        for chunk in self.visible:
            chunk.draw()
        if self.chosen_block:
            if not self.chosen_block_img:
                logger.error('Chosen block image not found!')
                sys.exit(1)
            self.app.screen.blit(self.chosen_block_img, Vec2(self.chosen_block.sx, self.chosen_block.sy)
                                 - self.app.camera.pos)

    def update(self):
        self.visible = self.calculate_visible_chunks()
        mouse = pg.mouse.get_pos()
        if 0 <= mouse[0] - self.app.camera.pos.x <= self.app.w:
            if 0 <= mouse[1] - self.app.camera.pos.y <= self.app.h:
                x = int((mouse[0] + self.app.camera.pos.x) // (self.cfg['block-size']))
                y = int((mouse[1] + self.app.camera.pos.y) // (self.cfg['block-size']))
                chunk = self.get_chunk_at(x // self.cfg['cw'], y // self.cfg['ch'])
                if chunk:
                    self.chosen_block = chunk.get_block_at(x % self.cfg['cw'], y % self.cfg['ch'])

        if self.chosen_block:
            self.interface.rect[0] = mouse[0]
            self.interface.rect[1] = mouse[1]
            self.interface.text = str(self.chosen_block.type_)
