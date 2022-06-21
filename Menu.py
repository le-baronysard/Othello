import pygame
from game import Game
from params import *


class Menu(Game):
    def __init__(self):
        super().__init__()
        #self.game = game
        pass

    def display_menu(self):
        while self.running :
            self.display.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.running=False
                    #pygame.quit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        print("escape")
                        self.running=False
            self.draw_text("The Othello project",50,self.weight/2,self.height/4)
            self.draw_text("Start Game", 30, self.weight/2, self.height/3+50)
            self.draw_text("Options", 30, self.weight/2, self.height/3+100)
            self.draw_text("Credits", 30, self.weight/2, self.height/3+150)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(60)
            pass


if __name__== "__main__":
    menu = Menu()
    menu.display_menu()
