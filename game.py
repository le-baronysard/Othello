import pygame
from params import *
import time
import random

class Game():
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        if SCREEN_MODE == "DEFAULT":
            screen = pygame.display.set_mode()
            self.width,self.height = screen.get_size()
            # pygame.display.quit()
            # pygame.init()
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode(size=(self.width,self.height))
        pygame.display.set_caption("Othello")
        self.running = True
        print(f"UI initialised with {self.width}x{self.height} pixels")
        #
        unitw = int(self.width/11)
        unith = int(self.height/11)
        self.unit =min(unith,unitw)


    def draw_text(self, text, size, x, y ,color =WHITE,surface=None):
        if not surface : surface = self.display
        font = pygame.font.Font("freesansbold.ttf",size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface,text_rect)

    def game_loop(self):
        t = 0
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
            #pygame.draw.lines(self.display,BLACK,False,w_coord)
            #pygame.draw.line(self.display,BLACK,(0,10),(100,100),1)
            #pygame.display.update()

            unit = self.unit
            pygame.draw.rect(self.display,(128,128,128),[0,0,11*unit,self.height])
            for j in range(8):
                for i in range(8):
                    pygame.draw.rect(self.display,WHITE,[(i+1)*unit+i*(unit/10)
                                   ,(j+1)*unit+j*(unit/10),unit,unit])
            if t==0 :
                for j in range(8):
                    for i in range(8):
                        print([(i+1)*unit+i*(unit/10)
                                    ,(j+1)*unit+j*(unit/10),unit,unit])

            # BEST POS
            #game.draw_text("TDKLAPDO",11,self.width-1/3*self.height,unit/2)

            game.draw_text("TDKLAPDO",11,250,self.unit/2)
            game.draw_leaderboard()
            pygame.display.flip()
            time.sleep(0.5)
            t += 1
            if t>30 :
                print(self.width-self.unit*11,self.width/3)
                print("Game automatically closing after 15 sec during test phase")
                pygame.quit()
                break
        pygame.quit()

    def draw_leaderboard(self):
        leaderboard = pygame.Surface(size=(self.width-11*self.unit,self.height))
        leaderboard.fill(color=BLACK)
        game.draw_text("LEADERBOARD",25,leaderboard.get_width()/2,self.unit/2,
                       surface=leaderboard,color=((random.randint(0,254),random.randint(0,254),random.randint(0,254))))
        # Drawing basics Info
        score = {-1:0,1:0}
        letters_size = 8
        game.draw_text("PLAYER_1  WHITE",letters_size,leaderboard.get_width()/4,2*self.unit,
                       surface=leaderboard)
        game.draw_text("PLAYER_2  BLACK",letters_size,3*leaderboard.get_width()/4,2*self.unit,
                       surface=leaderboard)
        game.draw_text(f"SCORE : {score[1]}",letters_size,leaderboard.get_width()/4,
                       2*self.unit+2*letters_size,
                       surface=leaderboard)
        game.draw_text(f"SCORE : {score[-1]}",letters_size,3*leaderboard.get_width()/4,
                       2*self.unit+2*letters_size,
                       surface=leaderboard)
        self.display.blit(leaderboard,(11*self.unit,0))

    def draw_board(self):
        pass

# TODO draw the board
# PLayer Input
# Score
# Final Score



if __name__== "__main__":
    game = Game()
    game.game_loop()
