import pygame
import time
import random

# locals Imports
from params import *
from ruler import Ruler
from RandomAgent import RandomAgent

printRect= True

class Menu():
    def __init__(self):
        pygame.init()
        self.music = pygame.mixer.music.load("data/Myuu-TenderRemains.mp3")
        pygame.mixer.music.play(fade_ms=10_000)
        self.width = WIDTH
        self.height = HEIGHT
        if SCREEN_MODE == "DEFAULT":
            screen = pygame.display.set_mode()
            self.width,self.height = screen.get_size()
            # pygame.display.quit()
            # pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(size=(self.width,self.height)
                                               ,flags=pygame.RESIZABLE)
        pygame.display.set_caption("The Othello Project")
        self.running = True
        print(f"UI initialised with {self.width}x{self.height} pixels")
        #
        self.unit = min( self.display.get_height()/11
                            ,self.display.get_width()/11)
        self.int_unit = int(self.unit)

    def draw_text(self, text, size, x, y ,color =WHITE,surface=None,printRect=True):
        if not surface : surface = self.display
        font = pygame.font.Font("freesansbold.ttf",size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        (a,b)=text_rect.bottomright
        text_rect.center = (x,y)
        surface.blit(text_surface,text_rect)
        return (a,b)



class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        titles = ["Start  Game", "Options", "Credits"]
        self.letters_pos={word : [(random.randint(0,self.width),random.randint(0,self.height)) for _ in word]
                          for word in titles}
        print(self.letters_pos)

    def draw_title(self,title,c,y,):
        bottom_right = (0,0)
        letter_pos = self.letters_pos[title]
        x = self.width/2-len(title)*self.unit/3
        #print(c/255,((255-c)/255))
        for i,letter in enumerate(title):
            #y += bottom_right[1]
            bottom_right = self.draw_text(letter,self.int_unit-1,
                                            (c/255)*letter_pos[i][0]+((255-c)/255)*x,
                                            (c/255)*letter_pos[i][0]+((255-c)/255)*y,
                                            color=(c,c,c))
            x += bottom_right[0]/2 + (self.unit)/3

    def loop(self):
        t =  0
        while self.running :
            self.display.fill(color=(WHITE))
            self.unit = self.display.get_width()/20
            self.int_unit = int(self.unit)
            self.width, self.height = self.display.get_size()

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

            title = "THE OTHELLO PROJECT"
            c = max(0,255-t)
            transition = (c,c,c)
            for i,letter in enumerate(title) :
                color = BLACK if i%2==0 else transition
                self.draw_text(letter,self.int_unit,(i+1)*self.unit,self.unit,color=color)
            #self.draw_text("Start Game", self.int_unit, self.width/2, self.height/2-self.unit,color=transition)
            # self.draw_text("Start ", self.int_unit, (255-c)*self.width/(2*255)-self.int_unit, self.height/2-self.unit,color=transition)
            # self.draw_text("Game", self.int_unit, self.width/2+c*self.width/(2*255)+self.unit, self.height/2-self.unit,color=transition)
            #word = "Start  Game"
            #for i,letter in enumerate(word):
            #   self.draw_text(letter,self.int_unit-1,self.letters_pos[word][i][0],self.letters_pos[word][i][1],color=color)
            #self.letters_pos[word] = [(random.randint(0,self.width),random.randint(0,self.height)) for _ in word]
            titles = ["Start  Game", "Options", "Credits"]

            self.draw_title("Start  Game",c,self.height/2-self.unit)
            self.draw_title("Options",c,self.height/2+self.unit)
            self.draw_title("Credits",c,self.height/2+3*self.unit)
            word = "Options"
            # x,y = self.width/2-len(word)*self.unit/3,self.height/2+self.unit
            # for i,letter in enumerate(word):
            #     #y += bottom_right[1]
            #     bottom_right = self.draw_text(letter,self.int_unit, x,y,color=transition)
            #     x += bottom_right[0]/2 + (self.unit)/3
            # word = "Credits"
            # x,y = self.width/2-len(word)*self.unit/3,self.height/2+3*self.unit
            # for i,letter in enumerate(word):
            #     #y += bottom_right[1]
            #     bottom_right = self.draw_text(letter,self.int_unit, x,y,color=transition)
            #     x += bottom_right[0]/2 + (self.unit)/3
            #self.draw_text("Options", self.int_unit, self.width/2, self.height/2+self.unit,color=transition)
            #self.draw_text("Credits", self.int_unit, self.width/2, self.height/2+4*self.unit,color=transition)
            pygame.display.flip()
            self.clock.tick(60)
            t += 1
            if t>10_000:
                print("Game automatically closing after 30 sec during test phase")
                break
        pygame.quit()




if __name__== "__main__":
    menu = MainMenu()
    menu.loop()
