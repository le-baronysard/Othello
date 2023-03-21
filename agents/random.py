# First hand agent to test the UI
import random


class RandomAgent():
    def __init__(self):
        pass

    def play(self,moves):
        choice = random.randint(0,len(moves)-1)
        return moves[choice]






if __name__ == "__main__":
    from tqdm import tqdm
    from ruler import Ruler
    agent1,agent2 = RandomAgent(),RandomAgent()
    stats,i = [],0
    for _ in tqdm(range(10_000)):
        ruler = Ruler()
        i+=1
        # for _ in range(10):
        #     print(ruler.board)
        #     print(ruler.valids_moves())
        #     ruler.write_move(agent1.play(ruler.valids_moves()[1]))
        #     ruler.write_move(agent2.play(ruler.valids_moves()[1]))
        #     print(ruler.board)
        while ruler.keep_playing:
            #print(ruler.board)
            player,list_=(ruler.valids_moves())
            ruler.write_move(agent1.play(list_))
        #print(ruler.short_memory)
        score =(ruler.get_score())
        #print(score)
        winner = max([1,-1],key=lambda x:score[x])
        stats.append(winner)
        if i%100==0 :
            print(f"game number {i}")
        if i%1000==0 :
            print(sum(stats))
            winner = "Black" if sum(stats)<0 else "White"
            print(f"The winner is {winner}")

    print(sum(stats))
    winner = "Black" if sum(stats)<0 else "White"
    print(f"The winner is {winner}")
