import random
from matplotlib import pyplot as plt
import numpy as np
class Action:
    type = None
    typeDict = {0:"stone", 1:"scissors", 2:"paper"}

    def __init__(self, type):
        if isinstance(type, int):
            self.type = self.typeDict.get(type)
        elif isinstance(type, str):
            self.type = type

    def __eq__(self, other):
        if(self.type == other.type):
            return True
        return False

    def __gt__(self, other):
        if self.type == "stone" and other.type == "scissors":
            return True
        elif self.type == "scissors" and other.type == "paper":
            return True
        elif self.type == "paper" and other.type == "stone":
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__()

    def __lt__(self,other):
        return not self.__gt__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

class Player:

    name = None



    def __init__(self, name):
        self.name = name

    def choose_action(self):
        pass

    def get_result(self, result, own, oponent):
        pass

    def name(self):
        return self.name

class Random_Player(Player):

    def __init__(self):
        super(Random_Player, self).__init__("Random-player")

    def choose_action(self):
        return Action(random.randint(0,2))

class Sequence_Player(Player):
    def __init__(self):
        super(Sequence_Player,self).__init__("Sequence-player")
        self.sequence_var = -1;
    def choose_action(self):
        self.sequence_var = (self.sequence_var+1)%3
        return Action(self.sequence_var)

class Statistical_Player(Player):

    def __init__(self):
        super(Statistical_Player,self).__init__("Statistical-Player")
        self.type_count = {"stone":0, "scissors":0, "paper":0}

    def choose_action(self):
        max = 0
        max_type = "stone"
        for key, value in self.type_count.items():

            if value > max:
                max_type = key
        print(max_type)
        return Action(max_type)

    def get_result(self, result, own, oponent):
        self.type_count[oponent.type] += 1

class SimpleHist_Player(Player):
    def chooseBest(self, action):
        if action.type == 'stone':
            return Action("paper")
        elif action.type == "scissors":
            return Action("stone")
        elif action.type == "paper":
            return Action("scissors")
        else:
            raise ValueError("action argument must be of type; stone, scissors or paper")

    def __init__(self, remember = 1):
        super(SimpleHist_Player, self).__init__("Historical-Player")
        self.moves = []
        self.remember = remember

    def list_finder(self,longList, searchList):
        if len(searchList) == 0:
            if len(longList) != 0:
                return longList[0:1]
            else:
                return []
        foundList =[]
        for i in range(len(longList)):
            if longList[i]==searchList[0]:
                foundList = foundList + (self.list_finder(longList[i+1:],searchList[1:]))
        return foundList


    def get_result(self, result, own, oponent):
        if isinstance(oponent, Action):
            self.moves.append(oponent)
        else:
            raise ValueError("argument was not of type Action")

    def choose_action(self):
        combination = self.moves[-self.remember:]
        countDict = {"stone":0, "scissors":0, "paper":0}

        foundItems = self.list_finder(self.moves, combination)

        for i in foundItems:
            countDict[i.type] += 1

        max_Value = 0
        max_Type = None
        for key, value in countDict.items():
            if(value > max_Value):
                max_Value = value
                max_Type = key

        if(max_Value == 0):
            return self.chooseBest(Action(random.randint(0,2)))
        else:
            return self.chooseBest(Action(max_Type))

class Dumb_Player(Player):

    def __init__(self):
        super(Dumb_Player, self).__init__("Dumb-Player")

    def choose_action(self):
        return Action("stone")

class simple_game():
    player1 = None
    player2 = None
    a1 = None
    a2 = None
    last_winner= None

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.last_winner = 0


    def play(self):
        winner = None

        self.a1 = self.player1.choose_action()
        self.a2 = self.player2.choose_action()

        if self.a1 == self.a2:
            winner = 0
            self.player1.get_result(0, self.a1, self.a2)
            self.player2.get_result(0, self.a2, self.a1)
        elif self.a1 > self.a2:
            winner = 1
            self.player1.get_result(1, self.a1, self.a2)
            self.player2.get_result(-1, self.a2, self.a1)
        elif self.a2 > self.a1:
            winner = 2
            self.player1.get_result(-1, self.a1, self.a2)
            self.player2.get_result(1, self.a2, self.a1)

        self.last_winner = winner

    def __str__(self):
        if(self.last_winner == 0):
            return ("%s 1 spilte: %s, %s 2 spilte: %s - UAVGJORT" % (self.player1.name, self.a1.type, self.player2.name, self.a2.type))

        return ("%s 1 spilte: %s, %s 2 spilte: %s - spiller %d vant"%(self.player1.name, self.a1.type, self.player2.name, self.a2.type, self.last_winner ))

class game_tournament():



    def __init__(self, player1, player2, rounds):
        self.game = simple_game(player1, player2)
        self.rounds_left = rounds
        self.player1_points = 0
        self.player2_points = 0
        self.history = []


    def play(self):
        while self.rounds_left > 0:
            self.game.play()
            print(self.game)
            self.rounds_left -= 1

            if self.game.last_winner == 0:
                self.player1_points += 0.5
                self.player2_points += 0.5
            elif self.game.last_winner == 1:
                self.player1_points += 1
            elif self.game.last_winner == 2:
                self.player2_points += 1

            self.history.append(self.player2_points - self.player1_points)
            print(self.rounds_left)
        plt.plot(self.history)
        plt.show()

def main():
    player1 = SimpleHist_Player()
    player2 = SimpleHist_Player()

    myGame = game_tournament(player1, player2, 1000)
    myGame.play()




if __name__ == '__main__':
    main()
