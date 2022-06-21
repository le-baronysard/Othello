import numpy as np

class Ruler():
    def __init__(self):
        self.board = np.full((8,8),"0")
        # Sarting pieces
        self.board[(3,3)],self.board[(4,4)] = "W","W"
        self.board[(3,4)],self.board[(4,3)] = "B","B"
        # First player is always Black
        self.turn = 0
        self.player_turn = "B"


    def on_board(self,pos:tuple):
        return pos[0]>0 and pos[1]>0 and pos[0]<8 and pos[1]<8

    def is_valid(self,move:tuple,player=None):
        move = np.array(move)
        if player == None : player = self.player_turn
        enemy = "W" if player=="B" else "B"
        if not self.on_board(move): return False
        directions = np.array([(0, 1), (1,  1), (1,  0), (1, -1)
                              ,(0,-1), (-1,-1), (-1, 0), (-1, 1)])
        flipped = []
        for dir in directions :
            search = move + dir
            will_it_flipp = []
            while self.on_board(search) and self.board[tuple(search)]==enemy:
                print(search)
                will_it_flipp.append(tuple(search))
                search += dir
                if not self.on_board(search) : break
                self.board[tuple(search)]
            if not self.on_board(search):continue
            if will_it_flipp==[]:continue
            flipped.append(will_it_flipp)
        if len(flipped)>=1 : return flipped
        return False


if __name__=='__main__':
    ruler = Ruler()
    print(ruler.is_valid((2,3)))
    print(ruler.board)
