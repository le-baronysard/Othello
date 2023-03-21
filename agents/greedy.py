# First hand agent to test the UI
import random
from agents.random import RandomAgent
from ruler import Ruler

class GreedyAgent():
    '''
    Always play the moves that return the most in a one turn forecast
    '''
    def __init__(self):
        pass

    def play(self,moves,ruler):
        if ruler.valids_moves()[1][0]=="No valid move":
            return 'No valid move'
        flipped = [len(ruler.is_valid(i)) for i in ruler.valids_moves()[1]]
        return ruler.valids_moves()[1][flipped.index(max(flipped))]


class BreadthFirstSearch():
    '''
    Perform a Breadth search and return the best possible moves at this deep
    If there is multiple possibles mooves return a random choice
    '''
    # TODO WIP

    def __init__(self,ruler,depth=2):
        self.depth = depth
        self.ruler = Ruler() # We need our own instance of the ruler class

    def search(self,board):
        self.ruler.board = board.copy()


if __name__ == "__main__":
    from ruler import Ruler
    agent1,agent2 = RandomAgent(),GreedyAgent()
    ruler = Ruler()
    for _ in range(10):
        print(ruler.board)
        print(ruler.valids_moves())
        ruler.write_move(agent1.play(ruler.valids_moves()[1]))
        print(ruler.board)
        print(ruler.valids_moves())
        ruler.write_move(agent2.play(ruler.valids_moves()[1],ruler))
