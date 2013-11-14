# Highlight-able menu in Pygame
#
# To run, use:
#     python pygame-menu-mouseover.py
#
# You should see a window with three grey menu options on it.  Place the mouse
# cursor over a menu option and it will become white.

import pygame
from pygame.locals import *


class Option:

    def __init__(self, screen, menu_font, text, offset, pos, still_color, hovered_color):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.still_color = still_color
        self.hovered_color = hovered_color
        self.hovered = False
        self.set_rect(offset, pos, menu_font)
        self.draw(screen, menu_font)

    def draw(self, screen, menu_font):
        self.set_rend(menu_font)
        screen.blit(self.rend, self.rect)

    def set_rend(self, menu_font):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return self.hovered_color
        else:
            return self.still_color

    def set_rect(self, offset, pos, menu_font):
        self.set_rend(menu_font)
        self.rect = self.rend.get_rect()
        self.rect.topleft = map(sum, zip(offset, pos))


#pygame.init()
#screen = pygame.display.set_mode((480, 320))
#menu_font = pygame.font.Font(None, 40)
#options = [Option(screen, menu_font, "NEW GAME", (0, 0), (135, 105), (100, 100, 100), (255, 255, 255)),
           #Option("LOAD GAME", (135, 155), (100, 100, 100), (255, 255, 255)),
           #Option("OPTIONS", (135, 205), (100, 100, 100), (255, 255, 255))]
#while True:
    #pygame.event.pump()
    #screen.fill((0, 0, 0))
    #for option in options:
        #if option.rect.collidepoint(pygame.mouse.get_pos()):
            #option.hovered = True
        #else:
            #option.hovered = False
        #option.draw()
    #for e in pygame.event.get():
        #if e.type == QUIT:
            #raise SystemExit, "QUIT"
        #if e.type == KEYDOWN and e.key == K_ESCAPE:
            #raise SystemExit, "ESCAPE"
    #pygame.display.update()
