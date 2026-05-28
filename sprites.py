import pygame, os
from pygame.locals import *
import math
class SpriteCarta(pygame.sprite.Sprite):
    def __init__(self,carta,posizione):
        pygame.sprite.Sprite.__init__(self)
        dir_image = "res" + os.sep + "carte" + os.sep + str(carta.seme) + str(carta.valore-1) + ".gif"
        self.image = pygame.image.load(dir_image).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = posizione
        self.carta = carta
    def draw(self,screen):
        screen.blit(self.image,self.rect)
    def update(self,rel):
        self.rect = self.rect.move(rel)
    def move(self, screen, pos):
        new_x, new_y = pos
        cur_x , cur_y = self.rect.topleft
        dif_x, dif_y = (cur_x - new_x), (cur_y - new_y)
        i = math.sqrt(pow((dif_x),2) + pow((dif_y),2))
        if dif_y < dif_x:
            pass
        