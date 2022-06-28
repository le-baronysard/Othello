from pydoc import cli
import pygame
import time
import random
import json

# locals Imports
from user_interface.params import *
from ruler import Ruler
from user_interface_utils import Minus_Button,ClickableBox,Menu_Bounding_Box



class Game():
    def __init__(self):
        pygame.init()
        self.ruler = Ruler()
        self.width = WIDTH
        self.height = HEIGHT


        # Set Up the Music
        with open('user_interface/data/preferences.json') as json_file:
            params = json.load(json_file)
        self.music = pygame.mixer.music.load("user_interface/data/Myuu-TenderRemains.mp3")
        pygame.mixer.music.play(fade_ms=10_000)
        self.music_volume = params["musique_volume"]
        pygame.mixer.music.set_volume(self.music_volume/10)
        self.sound_volume = params["sound_volume"]


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




    def save_parameters(self):
        params = {"musique_volume":self.music_volume
                  ,"sound_volume":self.sound_volume}
        with open('user_interface/data/preferences.json', 'w') as outfile:
            json.dump(params,outfile)

    def draw_text(self, text, size, x, y ,color =WHITE,surface=None,printRect=True):
        if not surface : surface = self.display
        font = pygame.font.Font("freesansbold.ttf",size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        (a,b)=text_rect.bottomright
        text_rect.center = (x,y)
        surface.blit(text_surface,text_rect)
        return (a,b)

    def check_user_input(self,pos=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.running=False
                #pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    print("Escape key pressed, Game shutting down...")
                    self.running=False
                if event.key == pygame.K_RETURN :
                    return "enter"
                if event.key == pygame.K_DOWN :
                    return "key_down"
                if event.key == pygame.K_UP :
                    return "key_up"
            if event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
                if pos : return click_pos

    def game_loop(self):
        t = 0
        self.running = True
        self.player = self.ruler.get_player()
        while self.running :
            self.display.fill(WHITE)
            pos = self.check_user_input(pos=True)
            # If the windows has beeen resize we need to update "unit"
            # and resize the img we are using
            if self.unit != min( self.display.get_height()/11
                            ,self.display.get_width()/11) :
                self.load_and_resize()
            self.draw_leaderboard()
            self.draw_board()
            if t==0 : print(self.ruler.board)
            self.draw_text(f"Current Player : {self.player}",self.unit_int//2,self.height/2,self.unit/2)
            pygame.display.flip()

            if pos :
                print(pos)
                clicked_sprites = [s for s in self.clickable_square if s.rect.collidepoint(pos)]
                if not clicked_sprites ==[] :
                    print("clicked on ",pos,clicked_sprites)

                    print("POS",clicked_sprites[0].pos,type(clicked_sprites[0].pos))
                    self.ruler.write_move(clicked_sprites[0].pos)
                    self.player = self.ruler.get_player()
                    print(self.ruler.board)


            self.clock.tick(60)
            t += 1
            if t>60*300: #FPS x time
                print("Game automatically closing after 300 sec during test phase")
                break


    def draw_leaderboard(self):
        leaderboard = pygame.Surface(size=(self.width-11*self.unit,self.height))
        leaderboard.fill(color=BLACK)
        self.draw_text("LEADERBOARD",25,leaderboard.get_width()/2,self.unit/2,
                       surface=leaderboard,color=((random.randint(0,254),random.randint(0,254),random.randint(0,254))))
        # Drawing basics Info
        score = {-1:0,1:0} #TODO connect to ruler.py input
        letters_size = 8
        self.draw_text("PLAYER_1  WHITE",letters_size,leaderboard.get_width()/4,2*self.unit,
                       surface=leaderboard)
        self.draw_text("PLAYER_2  BLACK",letters_size,3*leaderboard.get_width()/4,2*self.unit,
                       surface=leaderboard)
        self.draw_text(f"SCORE : {score[1]}",letters_size,leaderboard.get_width()/4,
                       2*self.unit+2*letters_size,
                       surface=leaderboard)
        self.draw_text(f"SCORE : {score[-1]}",letters_size,3*leaderboard.get_width()/4,
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
        #print(self.clickable_square)
        for i in range(9):
            pygame.draw.aaline(board,color=BLACK,start_pos=(i*unit,0),end_pos=(i*unit,9*unit))
            pygame.draw.aaline(board,color=BLACK,start_pos=(0,i*unit),end_pos=(9*unit,i*unit))
        pygame.draw.aaline(board,color=BLACK,start_pos=(8*unit-1,0),end_pos=(8*unit-1,8*unit-1))
        pygame.draw.aaline(board,color=BLACK,start_pos=(0,8*unit-1),end_pos=(8*unit-1,8*unit-1))


        left_panel.blit(board,(1.5*unit,1.5*unit))
        # Drawing pieces
        player,possibles_mooves = self.ruler.valids_moves()
        player_small_token = self.small_black_token if player==-1 else self.small_white_token
        self.clickable_square = pygame.sprite.Group()
        for j in range(8):
            for i in range(8):
                token = self.ruler.board[(i,j)]
                if token == -1 : left_panel.blit(self.black_token,(1.5*unit+i*unit,1.5*unit+j*unit))
                if token ==  1 : left_panel.blit(self.white_token,(1.5*unit+i*unit,1.5*unit+j*unit))
                if token ==  0 :
                    if (i,j) in possibles_mooves :
                        # square = pygame.Surface((unit-1,unit-1))
                        # square.fill(GREEN)
                        # square.blit(player_small_token,((1/3)*unit,(1/3)*unit))
                        # board.blit(square,(i*unit+1,j*unit+1))
                        square = ClickableBox(unit=self.unit,pos=(i,j),image=player_small_token,)
                        square.rect.topleft = (1.5*unit+i*unit+1,1.5*unit+j*unit+1)
                        self.clickable_square.add(square)
                        left_panel.blit(square.image,square.rect)
        self.display.blit(left_panel,(0,0))

    def load_and_resize(self):
        if self.width != self.display.get_width() or self.height != self.display.get_height():
            self.unit = min( self.display.get_height()/11
                                ,self.display.get_width()/11)
            self.width, self.height = self.display.get_size()
            self.unit_int = int(self.unit)
            self.white_token = pygame.transform.scale(pygame.image.load("user_interface/data/w6.png")
                                                    ,(self.unit,self.unit))
            self.small_white_token = pygame.transform.scale(pygame.image.load("user_interface/data/w6.png")
                                                    ,(self.unit/3,self.unit/3))
            self.black_token = pygame.transform.scale(pygame.image.load("user_interface/data/b.png")
                                                    ,(self.unit,self.unit))
            self.small_black_token = pygame.transform.scale(pygame.image.load("user_interface/data/b.png")
                                                    ,(self.unit/3,self.unit/3))
            self.wood_board = pygame.transform.scale(pygame.image.load("user_interface/data/brown_wood.jpg")
                                                    ,(9*self.unit,9*self.unit))

    def main_menu_loop(self):
        self.titles = ["Start  Game", "Options", "Credits"]
        self.cursor = self.titles.pop(0)
        self.titles.append(self.cursor)
        self.letters_pos={word : [(random.randint(0,self.width),random.randint(0,self.height)) for _ in word]
                          for word in self.titles}

        def draw_title(title,c,y,):
            bottom_right = (0,0)
            letter_pos = self.letters_pos[title]
            x = self.width/2-len(title)*self.unith/3
            #print(c/255,((255-c)/255))
            for i,letter in enumerate(title):
                #y += bottom_right[1]
                bottom_right = self.draw_text(letter,self.int_unith-1,
                                                (c/255)*letter_pos[i][0]+((255-c)/255)*x,
                                                (c/255)*letter_pos[i][0]+((255-c)/255)*y,
                                                color=(c,c,c))
                x += bottom_right[0]/2 + (self.unitw)/3

        t =  0
        title = "THE OTHELLO PROJECT"
        while self.running :
            self.next = None
            self.display.fill(color=(WHITE))
            self.width, self.height = self.display.get_size()
            self.unitw,self.unith = self.width/20,self.height/20
            self.int_unitw,self.int_unith = int(self.unitw),int(self.unith)

            # TEMPORAIRE c
            c = 0
            c = max(0,255-t)

            # Draw clickable Bounding Boxes for user input
            if c == 0 :
                cc = max(125,2*255-t) #Bouding_Box transitioning color
                cc = 125
                height = {"Start  Game":self.height/2-self.unith
                          ,"Options":self.height/2+self.unith
                          ,"Credits":self.height/2+3*self.unith}[self.cursor]
                bounding_box = Menu_Bounding_Box(10*self.unitw,(4/3)*self.unith,(cc,cc,cc))
                bounding_box.rect.center = (10*self.unitw,height)
                self.display.blit(bounding_box.image,bounding_box.rect)


            transition = (c,c,c)
            for i,letter in enumerate(title) :
                color = BLACK if i%2==0 else transition
                self.draw_text(letter,self.int_unith,(i+1)*self.unitw,self.unitw,color=color)
            draw_title("Start  Game",c,self.height/2-self.unith)
            draw_title("Options",c,self.height/2+self.unith)
            draw_title("Credits",c,self.height/2+3*self.unith)

            user_input = self.check_user_input(pos=True)
            if user_input == "key_down" :
                self.cursor=self.titles.pop(0)
                self.titles.append(self.cursor)
            if user_input == "key_up" :
                self.cursor=self.titles.pop(-1)
                self.titles.insert(0,self.cursor)
            if user_input == "enter" :
                if self.cursor == "Start  Game" : self.next = self.game_loop
                if self.cursor == "Options" : self.next = self.option_menu_loop
                if self.cursor == "Credits" : self.next = None
                self.running = False
                self.load_and_resize()

            pygame.display.flip()
            self.clock.tick(60)
            t += 1


            if t>10_000:
                print("Game automatically closing after 30 sec during test phase")
                break
        if self.next :
            self.next()
        pygame.quit()

    def option_menu_loop(self):
        '''Option screen with Music,Resolution,Sound options'''
        self.load_and_resize()
        self.running = True
        while self.running :
            self.load_and_resize()
            self.display.fill(WHITE)
            self.draw_text("Music Volume",self.unit_int,self.width/2,self.height/4,BLACK)
            # Draw music - button
            music_minus = Minus_Button(BLACK,self.unit,btype="minus")
            music_minus.rect.topleft = (self.width/4-self.unit,self.height/4+self.unit)
            self.display.blit(music_minus.image,music_minus.rect)

            # Draw Music + button
            music_plus = Minus_Button(ALMOST_BLACK,self.unit,btype="plus")
            music_plus.rect.topleft = (3*self.width/4,self.height/4+self.unit)
            self.display.blit(music_plus.image,music_plus.rect)
            # Draw Sound text
            self.draw_text("Sound Volume",self.unit_int,self.width/2,2*self.height/4,BLACK)
            # Draw Sound - button
            sound_minus = Minus_Button(ALMOST_BLACK,self.unit,btype="minus")
            sound_minus.rect.topleft = (self.width/4-self.unit,2*self.height/4+self.unit_int)
            self.display.blit(sound_minus.image,sound_minus.rect)
            # Draw Sound + button
            sound_plus = Minus_Button(ALMOST_BLACK,self.unit,btype="plus")
            sound_plus.rect.topleft = (3*self.width/4,2*self.height/4+self.unit_int)
            self.display.blit(sound_plus.image,sound_plus.rect)

            self.draw_text("Main Menu",self.unit_int//2+2,self.width/2,4*self.height/5,BLACK)

            # Let's check if the user click on something
            sprites = [music_plus,music_minus,sound_minus,sound_plus]
            pos = self.check_user_input(pos=True)
            if pos :
                clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
                clicked_sprites = [0] if clicked_sprites == [] else clicked_sprites
                print("clicked on ",pos,clicked_sprites,clicked_sprites[0]==music_minus)
                if clicked_sprites :
                    if clicked_sprites[0]==music_minus :
                        self.music_volume = max(0,self.music_volume-1)
                    if clicked_sprites[0]==music_plus :
                        self.music_volume = min(10,self.music_volume+1)
                    pygame.mixer.music.set_volume(self.music_volume/10)
                    if clicked_sprites[0]==sound_minus :
                        self.sound_volume = max(0,self.sound_volume-1)
                    if clicked_sprites[0]==sound_plus :
                        self.sound_volume = min(10,self.sound_volume+1)
                    print("Sound Volume Set to ",self.sound_volume/10)
                    self.save_parameters()

            pygame.display.flip()
            self.clock.tick(60)

            pass





# TODO
# PLayer Input
# Final Score



if __name__== "__main__":
    game = Game()

    # game.ruler.player_turn=1
    #game.option_menu_loop()
    game.main_menu_loop()
