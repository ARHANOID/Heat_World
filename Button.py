from Paiter import Painter
import pygame, sys, math

class Button():
    def __init__(self,surface, color, x, y, width, height, img = None, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect((self.x, self.y),( width, height))
        self.draw(surface, img)


    def draw(self, surface, img):
        if img is not None:
            surface.blit(img,(self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)



        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (255, 255, 255))
            # surface.blit(text,(self.x, self.y))
            surface.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_mouseover(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)

