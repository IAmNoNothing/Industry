import pygame as pg


class InterfaceManager:
    instances = []

    @staticmethod
    def update():
        for instance in InterfaceManager.instances:
            instance.update()

    @staticmethod
    def draw():
        for instance in InterfaceManager.instances:
            instance.draw()


class Interface:
    def __new__(cls, *args, **kwargs):
        if cls not in InterfaceManager.instances:
            InterfaceManager.instances.append(super(Interface, cls).__new__(cls))
        return InterfaceManager.instances[-1]

    def __init__(self, rect, props):
        self.rect = rect
        self.props = props
        self._text = self.props.get('text', '')
        self.font = pg.font.Font(self.props.get('font', None), self.props.get('font-size', 20))
        self.text_surf = self.font.render(self._text, True, self.props.get('color', (255, 255, 255)))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.text_surf = self.font.render(self._text, True, self.props.get('color', (255, 255, 255)))

    def update(self):
        pass

    def draw(self):
        pg.draw.rect(self.props['screen'], self.props['inner-color'], self.rect)
        if self.props.get('width', -1) > 0:
            pg.draw.rect(self.props['screen'], self.props['outer-color'], self.rect, self.props['width'])
        self.props['screen'].blit(self.text_surf, (self.rect[0] + 5, self.rect[1] + 5))
