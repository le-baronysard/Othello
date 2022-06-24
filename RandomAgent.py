# First hand agent to test the UI
import random

class RandomAgent():
    def __init__(self):
        pass

    def play(self,moves):
        choice = random.randint(0,len(moves)-1)
        return moves[choice]



if __name__ == "__main__":
    from ruler import Ruler
    agent1,agent2 = RandomAgent(),RandomAgent()
    ruler = Ruler()
    for _ in range(10):
        print(ruler.board)
        print(ruler.valids_moves())
        ruler.write_move(agent1.play(ruler.valids_moves()[1]))
        ruler.write_move(agent2.play(ruler.valids_moves()[1]))
        print(ruler.board)
