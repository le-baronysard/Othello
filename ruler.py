from xmlrpc.client import Boolean
import numpy as np
import time

class Ruler():
    def __init__(self):
        self.board = np.full((8,8),0)
        # Sarting pieces
        self.board[(3,3)],self.board[(4,4)] = 1,1  #"W","W"
        self.board[(3,4)],self.board[(4,3)] = -1,-1 #"B","B"
        # First player is always Black
        self.turn = 0
        self.player_turn = -1 #"B"


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

    def is_valid(self,move:tuple,player:int=None):
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
        '''Return the current player turn and a list of possibles moves'''
        return (self.player_turn,[(i,j) for i in range(8) for j in range(8) if self.is_valid((i,j))])


    def write_move(self,move:tuple):
        # TODO Update score and write self.memory
        if not  type(move)==tuple : raise TypeError("Invalid Move format")
        flipped = self.is_valid(move)
        if not flipped : raise SyntaxError("Out of range position")
        self.board[move]=self.player_turn
        self.player_turn *= -1
        for pos in flipped :
            self.board[pos] *= -1




if __name__=='__main__':
    start = time.time()
    ruler = Ruler()
    print(ruler.is_valid((3,2)))
    print(ruler.board)
    print(ruler.valids_moves())
    ruler.write_move((3,2))
    #ruler.write_move((2,2))
    print(ruler.board)
    end = time.time()

    print("Process time",end-start)
