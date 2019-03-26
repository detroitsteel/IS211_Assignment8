#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Good ol family fun game of pig"""

import random
import datetime
import operator

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(len(self.items),item)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

class Player:
    def __init__(self):
        self.plynum = 0
        self.rollturn = 0
        self.turnpoints = 0

    def getPlyNum(self):
        return self.plynum

    def getRollTurn(self):
        return self.rollturn

    def getTurnPoints(self):
        return self.turnpoints

class realPly(Player):

    def realPlyVals(self, plynum):
        self.plynum = plynum
        return(self.plynum, 'Player', self.rollturn, self.turnpoints)

class compPly(Player):

    def compPlyVals(self, plynum):
        self.plynum = plynum
        return(self.plynum, 'Computer', self.rollturn, self.turnpoints)

class PlayerFactory:
    def getPly(self, numply, numcpu):
        self.ply_dict = {}
        self.ply_queue = Queue()
        totalply = numply + numcpu
        real_Ply = realPly()
        comp_Ply = compPly()
        for ply in range(totalply):
            ply = ply + 1
            if (numply > 0):
                person = real_Ply.realPlyVals(ply)
                self.ply_dict.update({person[0]: person[1:]})
                self.ply_queue.enqueue(ply)
                numply = numply -1 
            elif numcpu > 0:
                computer = comp_Ply.compPlyVals(ply)
                self.ply_dict.update({computer[0]: computer[1:]})
                self.ply_queue.enqueue(ply)
        return

class Game:      
    def __init__(self, numply, numcpu):
        self.factory = PlayerFactory()
        self.factory.getPly(numply, numcpu)
        self.plydecide = ''
        self.dieroll = 0
        self.rollturn = 1
        self.turnpoints = 0
        self.ply_queue = self.factory.ply_queue
        self.ply_dict = self.factory.ply_dict
        self.gameOn = 1
        self.plyOn = 1

    def pigGame(self):
        """pigGame Function - Play the game pig with unlimited players against
        unlimted number of computer players.
        The rules of Pig are simple.
        The game features at least two players, with the goal of reaching
        100 points first. Each turn, a player repeatedly rolls a die until
        either a 1 is rolled or the player holds and scores the sum of the
        rolls (i.e. the turn total). At any time during a player's turn,
        the player is faced with two decisions:
        roll ­ If the player rolls a 1: the player scores nothing and it becomes
        the opponent's turn. if the player rolls 2 ­ 6: the number is added to
        the player's turn total and the player's turn continues.
        hold ­ The turn total
        is added to the player's score and it becomes the opponent's turn.
        Args:
            numply (int): The number of human players who will play the game
            numcpu (int): The number of computer players who will play the game

        Output: Game play according to the rules
        Example:
            >>> pigGame(2)
            >>>Player 1 current turn score is 0.
                1 roll(s) of the die returns 5.
                Roll again type R or to hold type H:h
                Next Player
                Player 2 turn.
                .....
                Player 1 turn.
                Player 1 score is currently 99.

                Player 1 current turn score is 0.
                26 roll(s) of the die returns 6.
                Roll again type R or to hold type H:h
                Player 1 wins
        """
        while self.gameOn:
            self.plyturn = self.ply_queue.items[0]
            self.turnpoints = self.ply_dict[self.plyturn][2]
            self.rollturn = (self.ply_dict[self.plyturn][1]) + 1
            self.plytype = self.ply_dict[self.plyturn][0]
            self.curturnpoints = 0
            self.plyOn = 1
            self.dieroll = random.randint(1,6)
            print ("Player %i turn.\nPlayer %i score is currently %i.\n"
                   %(self.plyturn, self.plyturn, self.turnpoints))
            self.pigGamePlay()

    def pigGamePlay(self):
        while self.plyOn:
            if self.dieroll == 1:
                print '\n!!OOOPS, you rolled a 1. Next Players turn!!\n'
                self.ply_queue.dequeue()
                self.ply_queue.enqueue(self.plyturn)
                self.plyOn = 0
                break
            if self.plytype == 'Player':
                print ("Player %i current turn score is %i.\n"
                       "%i roll(s) of the die returns %i."
                       %(self.plyturn, self.curturnpoints, self.rollturn,
                         self.dieroll))
                self.plydecide = (raw_input("Roll again type R or to hold type H:\n"))
                self.plydecide = self.plydecide.upper()
            elif self.plytype == 'Computer':
                if self.curturnpoints >= 25:
                    self.plydecide = 'H'
                else:
                    self.plydecide = 'R'
            self.curturnpoints = self.curturnpoints + self.dieroll
            if self.plydecide == 'R':
                self.dieroll = random.randint(1,6)
                self.rollturn += 1
            elif self.plydecide == 'H':
                self.turnpoints = self.turnpoints + self.curturnpoints
                if self.turnpoints >= 100:
                    print "\n\nPlayer %i wins!!!!!" %self.plyturn
                    self.gameOn = 0
                    return
                print 'Next Player'
                self.ply_dict.update({self.plyturn: (self.plytype, self.rollturn
                                                     , self.turnpoints)})
                self.ply_queue.dequeue()
                self.ply_queue.enqueue(self.plyturn)
                self.plyOn = 0
            else:
                print 'Invalid Entry, try again'
                break

class timedGameProxy(Game):
    def __init__(self, numply, numcpu, time):
        self.time = time
        self.curtime = datetime.datetime.now()
        self.expire = self.curtime + datetime.timedelta(seconds = self.time)
        self.factory = PlayerFactory()
        self.factory.getPly(numply, numcpu)
        self.plydecide = ''
        self.dieroll = 0
        self.rollturn = 1
        self.turnpoints = 0
        self.ply_queue = self.factory.ply_queue
        self.ply_dict = self.factory.ply_dict
        self.gameOn = 1
        self.plyOn = 1
        winner = 0
        winnerscore = 0
        winnertype = ''

    def timedPigGame(self):
        """timedPigGame Function - Play the game pig with unlimited players
        against unlimted number of computer players for a specificed time
        limit in seconds.
        The rules of Pig are simple.
        The game features at least two players, with the goal of reaching
        100 points first. Each turn, a player repeatedly rolls a die until
        either a 1 is rolled or the player holds and scores the sum of the
        rolls (i.e. the turn total). At any time during a player's turn,
        the player is faced with two decisions:
        roll ­ If the player rolls a 1: the player scores nothing and it becomes
        the opponent's turn. if the player rolls 2 ­ 6: the number is added to
        the player's turn total and the player's turn continues.
        hold ­ The turn total
        is added to the player's score and it becomes the opponent's turn.
        Args:
            numply (int): The number of human players who will play the game
            numcpu (int): The number of computer players who will play the game
            time (int): How long the game will last before a winner is declared

        Output: Game play according to the rules
        Example:
            >>> pigGame(2)
            >>>Player 1 current turn score is 0.
                1 roll(s) of the die returns 5.
                Roll again type R or to hold type H:h
                Next Player
                Player 2 turn.
                .....
                Player 1 turn.
                Player 1 score is currently 99.

                Player 1 current turn score is 0.
                26 roll(s) of the die returns 6.
                Next Player
                
                Times up. Player number 1 wins with a score of 15.
        """
        while self.gameOn:
            if datetime.datetime.now() >= self.expire:
                winner = (max(self.ply_dict.iteritems(),
                             key = operator.itemgetter(1))[0])
                winnerscore = self.ply_dict[winner][2]
                winnertype = self.ply_dict[winner][0]
                print ('\nTimes up. %s number %i wins with a score of %i.\n '
                       %(winnertype, winner, winnerscore))
                self.gameOn = 0
                break
            self.plyturn = self.ply_queue.items[0]
            self.turnpoints = self.ply_dict[self.plyturn][2]
            self.rollturn = (self.ply_dict[self.plyturn][1]) + 1
            self.plytype = self.ply_dict[self.plyturn][0]
            self.curturnpoints = 0
            self.plyOn = 1
            self.dieroll = random.randint(1,6)
            print ("Player %i turn.\nPlayer %i score is currently %i.\n"
                   %(self.plyturn, self.plyturn, self.turnpoints))
            self.pigGamePlay()
        
    

if __name__ == '__main__':
    numoPlayers = int((raw_input("How many human players?\n")))
    numoComputes = int((raw_input("How many computer players?\n")))
    timePlay = int((raw_input("How long in seconds is this game?"
                              "(0 = Unlimited)")))
    if timePlay == 0:
        plyPigGame = Game(numoPlayers, numoComputes)
        plyPigGame.pigGame()
    elif timePlay > 0:
        time_Pig_Game = timedGameProxy(numoPlayers, numoComputes, timePlay)
        time_Pig_Game.timedPigGame()
