import pygame

FONT_FILE = 'font/SourceHanSerifSC-Medium-Subset.otf'
FONT_SMALL = pygame.font.Font(FONT_FILE, 8)
FONT_NORMAL = pygame.font.Font(FONT_FILE, 12)
FONT_LARGE = pygame.font.Font(FONT_FILE, 16)

class FontRenderer:
    def __init__(self, font: pygame.font.Font, color: pygame.Color) -> None:
        self.cached: pygame.Surface = None
        self.font = font
        self.color = color
        self.text = ''

    def render(self, text: str) -> pygame.Surface:
        if not self.cached or text != self.text:
            # print('Create font cache')
            self.text = text
            sizes = tuple(self.font.size(x) for x in text.splitlines())
            width = max(x[0] for x in sizes)
            height = sum(x[1] for x in sizes)
            self.cached = pygame.Surface((width, height), pygame.SRCALPHA)
            acc = 0
            for line, (width, height) in zip(text.splitlines(), sizes):
                self.cached.blit(self.font.render(line, True, self.color), (0, acc))
                acc += height
        return self.cached
