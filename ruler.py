import numpy as np
import time

class Ruler():
    def __init__(self):
        self.possible_moves = [(i,j) for i in range(8) for j in range(8) if (i,j) not in [(3,3),(3,4),(4,4),(4,3)]]
        self.short_memory = []
        self.board = np.full((8,8),0)
        # Sarting pieces
        self.board[(3,3)],self.board[(4,4)] = 1,1  #"W","W"
        self.board[(3,4)],self.board[(4,3)] = -1,-1 #"B","B"
        # First player is always Black
        self.turn = 0
        self.player_turn = -1 #"B"
        self.stuck = 0
        self.keep_playing = True

        self.score = {-1:2,1:2}

        # TODO methods and returns formats that we should implement
        # STILL NOT DECIDED 100% !!! NEED TO THINK ABOUT IT
        #ruler.redo(self): --> Return to last turn
        # '-> we may need to implement a ruler.memory to keep track of the
        # game
        # like ruler.memory = {turn:{playerWhite:[posoccupiedbyWhite]}
        #                           ,playerBlack:[posoccupiedbuBlack]
        #                   ou alors board:[[1,-1,0 .....]] A voir
        #                           ,score:{-1:0,1:0}
        #                           ,playerTurn:-1 ou 1}
        #
        # ruler.write_move()
        # ruler.valids_move() : return all the possible moove



    def on_board(self,pos:tuple) -> bool :
        return pos[0]>=0 and pos[1]>=0 and pos[0]<8 and pos[1]<8

    def update_score(self):
        '''Update self.score'''
        self.score = {  1:(self.board==1).sum()
                      ,-1:(self.board==-1).sum()
                      }

    def is_valid(self,move:tuple,player:int=None):
        ''' A valid move would be a tuple that correspond to an unoccupied or "pass'''
        move = np.array(move)
        if player == None : player = self.player_turn
        enemy = 1 if player==-1 else -1
        if not self.on_board(move): return False
        directions = [(0, 1), (1,  1), (1,  0), (1, -1)
                              ,(0,-1), (-1,-1), (-1, 0), (-1, 1)]
        flipped = []
        for dire in directions :
            search = move[0]+dire[0],move[1]+dire[1]
            will_it_flipp = []
            while self.on_board(search) and self.board[search]==enemy:
                will_it_flipp.append(search)
                search = search[0]+dire[0],search[1]+dire[1]
            if not self.on_board(search) or self.board[search]!=player:continue
            if will_it_flipp!=[]:
                flipped+=(will_it_flipp)
        if len(flipped)>=1 : return flipped
        return False


    def valids_moves(self) -> tuple :
        '''Return the current player turn and a list of possibles moves
        also if the game is ended return the score ?'''
        valid_move = (self.player_turn,[i for i in self.possible_moves if self.is_valid(i)])

        return valid_move if valid_move[1] else (self.player_turn,['No valid move'])



    def write_move(self,move:tuple):
        if not  (type(move)==tuple or move == 'No valid move') : raise TypeError("Invalid Move format")

        if move == 'No valid move':
            self.short_memory.append(move)
            self.player_turn *= -1
            self.stuck += 1
            self.turn += 1
            if self.stuck == 2:
                self.keep_playing = False
                self.update_score()
                return ("Game Over",self.score)

        else:
            flipped = self.is_valid(move)
            if not flipped : raise SyntaxError("Out of range position")
            self.board[move]=self.player_turn
            self.player_turn *= -1
            self.stuck = 0
            self.possible_moves.remove(move)
            self.short_memory.append(move)
            for pos in flipped :
                self.board[pos] *= -1
            self.turn +=1
            self.update_score()

    def previous_move(self):
        '''
        Rejouer la partie permet de ne pas avoir à se souvenir quels jetons ont été retournés avant.
        '''
        self.possible_moves = [(i,j) for i in range(8) for j in range(8) if (i,j) not in [(3,3),(3,4),(4,4),(4,3)]]
        self.board = np.full((8,8),0)
        self.board[(3,3)],self.board[(4,4)] = 1,1  #"W","W"
        self.board[(3,4)],self.board[(4,3)] = -1,-1 #"B","B"
        self.turn = 0
        self.player_turn = -1 #"B"
        self.stuck = 0
        self.keep_playing = True
        list_ = self.short_memory[:-1]
        self.short_memory = []
        for move in list_:
            self.write_move(move)

    def get_player(self):
        return "BLACK" if self.player_turn ==-1 else "WHITE"

    def get_score(self):
        return {1:np.sum(self.board==1),-1:np.sum(self.board==-1),"turns":self.turn}


if __name__=='__main__':
    start = time.time()
    ruler = Ruler()
    print(ruler.is_valid((5,4)))
    print(ruler.board)
    print(ruler.valids_moves())
    ruler.write_move((5,4))
    #ruler.write_move((2,2))

    print(ruler.board)
    print(ruler.valids_moves())
    print(ruler.get_score())
    end = time.time()
    print("Process time",end-start)
