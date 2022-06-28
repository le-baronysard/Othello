import pygame
from user_interface.params import *

class Minus_Button(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position,"plus" for a +
    def __init__(self, color, unit,btype="plus",filler=(250,250,250)):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([unit,unit])
        self.image.fill(filler)

        # |
        if btype =='plus' :
            pygame.draw.rect(self.image,color=color,rect=(unit/2-unit/6,0,unit/3,unit))
        # _
        pygame.draw.rect(self.image,color=color,rect=(0,unit/2-unit/6,unit,unit/3))

        pygame.draw.circle(self.image,color=(64,64,64),center=(unit/2,unit/2),radius=unit/2+unit/10,width=10)


        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


class ClickableBox(pygame.sprite.Sprite):

    def __init__(self,unit,pos,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((unit-1,unit-1))
        self.image.fill(GREEN)
        self.image.blit(image,(unit/3,unit/3))
        self.rect=self.image.get_rect()
        self.pos = pos

class Menu_Bounding_Box(pygame.sprite.Sprite):

    def __init__(self,width,height,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image,color,(0,0,width-1,height-1),width=1)
        self.rect = self.image.get_rect()
