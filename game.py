import pygame
from params import *

class Game():
    def __init__(self):
        pygame.init()
        self.weight = WEIGHT
        self.height = HEIGHT
        if SCREEN_MODE == "default":
            screen = pygame.display.set_mode()
            #self.weight,self.height = screen.get_size()
            # pygame.display.quit()
            # pygame.init()
        self.clock = pygame.time.Clock()

        self.display = pygame.Surface((self.weight,self.height))
        self.window = pygame.display.set_mode(((self.weight,self.height)))
        self.running = True

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font("freesansbold.ttf",size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def game_loop(self):
        while self.running :
            self.display.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.running=False
                    #pygame.quit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        print("escape")
                        self.running=False
            self.window.blit(self.display, (0,0))
            w_coord = [(10,i*self.weight/8) for i in range(1,8)]
            #pygame.draw.lines(self.display,BLACK,False,w_coord)
            #pygame.draw.line(self.display,BLACK,(0,10),(100,100),1)
            #pygame.display.update()
            unitw = int(self.weight/11)
            unith = int(self.height/11)
            unit =min(unith,unitw)
            pygame.draw.rect(self.display,(128,128,128),[0,0,11*unit,11*unit])
            for j in range(8):
                for i in range(8):
                    pygame.draw.rect(self.display,WHITE,[(i+1)*unit+i*(unit/10)
                                   ,(j+1)*unit+j*(unit/10),unit,unit])
            self.window.blit(self.display, (0,0))
            pygame.display.flip()
            pass

    def draw_board(self):
        pass

# TODO draw the board
# PLayer Input
# Score
# Final Score



if __name__== "__main__":
    game = Game()
    game.game_loop()
    pygame.quit()
