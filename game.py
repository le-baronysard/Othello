import pygame
import time
import random

# locals Imports
from params import *
from ruler import Ruler



class Game():
    def __init__(self):
        pygame.init()
        self.ruler = Ruler()
        self.width = WIDTH
        self.height = HEIGHT
        if SCREEN_MODE == "FULL":
            screen = pygame.display.set_mode()
            self.width,self.height = screen.get_size()
            # pygame.display.quit()
            # pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(size=(self.width,self.height)
                                               ,flags=pygame.RESIZABLE)
        pygame.display.set_caption("Othello")
        self.running = True
        self.clickable_square = []
        print(f"UI initialised with {self.width}x{self.height} pixels")
        #
        ## loading the images before the game loop to save comput time
        self.load_and_resize()



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
                        print("Escape key pressed, Game shutting down...")
                        self.running=False
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()
                    print(click_pos)
                    clicked_sprites = [s for s in self.clickable_square if s.get_rect().collidepoint(click_pos)]
                    print(clicked_sprites)
            # If the windows has beeen resize we need to update "unit"
            # and resize the img we are using
            if self.unit != min( self.display.get_height()/11
                            ,self.display.get_width()/11) :
                self.load_and_resize()



            game.draw_leaderboard()
            self.draw_board()
            if t==0 : print(self.ruler.board)
            game.draw_text("TDKLAPDO",11,250,self.unit/2)
            pygame.display.flip()
            time.sleep(1)
            self.clock.tick(30)
            t += 1
            if t>30:
                print("Game automatically closing after 30 sec during test phase")
                break
        pygame.quit()

    def draw_leaderboard(self):

        leaderboard = pygame.Surface(size=(self.width-11*self.unit,self.height))
        leaderboard.fill(color=BLACK)
        game.draw_text("LEADERBOARD",25,leaderboard.get_width()/2,self.unit/2,
                       surface=leaderboard,color=((random.randint(0,254),random.randint(0,254),random.randint(0,254))))
        # Drawing basics Info
        score = {-1:0,1:0} #TODO connect to ruler.py input
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
        unit = self.unit
        # pygame.draw.rect(self.display,(128,128,128),[0,0,11*unit,self.height])
        # for j in range(8):
        #     for i in range(8):
        #         pygame.draw.rect(self.display,(0,102,51),[(i+1)*unit+i*(unit/30)
        #                         ,(j+1.3)*unit+j*(unit/30),unit,unit])
        # Draw little circle in the corners
        left_panel = pygame.Surface(size=[11*unit,self.height])
        left_panel.fill(GREY)
        board = pygame.Surface(size=[8*unit,8*unit])
        board.fill(color=GREEN)
        pygame.draw.circle(self.display,color=WHITE,center=(3.15*unit,3.15*unit),radius=unit/10)
        left_panel.blit(self.wood_board,(unit,unit))

        #print(board.get_height(),board.get_width())
        # Drawing pieves
        player,possibles_mooves = self.ruler.valids_moves()
        player_small_token = self.small_black_token if player==-1 else self.small_white_token
        self.clickable_square = []
        for j in range(8):
            for i in range(8):
                token = self.ruler.board[(i,j)]
                if token == -1 : board.blit(self.black_token,(i*unit,j*unit))
                if token ==  1 : board.blit(self.white_token,(i*unit,j*unit))
                if token ==  0 :
                    if (i,j) in possibles_mooves :
                        square = pygame.Surface((unit-1,unit-1))
                        square.fill(GREEN)
                        square.blit(player_small_token,((1/3)*unit,(1/3)*unit))

                        self.clickable_square.append(square)
                        board.blit(square,(i*unit+1,j*unit+1))

        #print(self.clickable_square)
        for i in range(9):
            pygame.draw.aaline(board,color=BLACK,start_pos=(i*unit,0),end_pos=(i*unit,9*unit))
            pygame.draw.aaline(board,color=BLACK,start_pos=(0,i*unit),end_pos=(9*unit,i*unit))
        pygame.draw.aaline(board,color=BLACK,start_pos=(8*unit-1,0),end_pos=(8*unit-1,8*unit-1))
        pygame.draw.aaline(board,color=BLACK,start_pos=(0,8*unit-1),end_pos=(8*unit-1,8*unit-1))


        left_panel.blit(board,(1.5*unit,1.5*unit))
        self.display.blit(left_panel,(0,0))

    def load_and_resize(self):
        self.unit = min( self.display.get_height()/11
                            ,self.display.get_width()/11)
        self.width, self.height = self.display.get_size()
        self.white_token = pygame.transform.scale(pygame.image.load("data/w6.png")
                                                  ,(self.unit,self.unit))
        self.small_white_token = pygame.transform.scale(pygame.image.load("data/w6.png")
                                                  ,(self.unit/3,self.unit/3))
        self.black_token = pygame.transform.scale(pygame.image.load("data/b.png")
                                                  ,(self.unit,self.unit))
        self.small_black_token = pygame.transform.scale(pygame.image.load("data/b.png")
                                                  ,(self.unit/3,self.unit/3))
        self.wood_board = pygame.transform.scale(pygame.image.load("data/brown_wood.jpg")
                                                 ,(9*self.unit,9*self.unit))

# TODO draw the board
# PLayer Input
# Score
# Final Score



if __name__== "__main__":
    game = Game()
    game.game_loop()
