#/usr/bin/env python

from ChessBoard import ChessBoard

import os
import pygame
import math
from pygame.locals import *
import string
from pprint import pprint


class ChessClient:
    def mainLoop(self):
        pygame.init()

        print "White Player, choose an army:"
        print "1. Classic   2. Nemesis   3. Reaper"
        print "4. Empowered 5. Two Kings 6. Animals"
        while True:
            userInput = raw_input('Type the number, not the name:')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print 'Please enter only one of the above.'
            else:
                print 'Please enter only one character'
        wArmy = userInput

        print "Black Player, choose an army:"
        print "1. Classic   2. Nemesis   3. Reaper"
        print "4. Empowered 5. Two Kings 6. Animals"
        while True:
            userInput = raw_input('Type the number, not the name:')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print 'Please enter only one of the above.'
            else:
                print 'Please enter only one of the above.'
        bArmy = userInput

        pieces = {}
        chess = ChessBoard(int(wArmy), int(bArmy))
        board = chess.getBoard()
        turn = chess.getTurn()
        chess.printBoard()
        print str(turn)

        if not chess.isGameOver():
            print "%s's turn. Type your move." % str(chess.value_to_color_dict[turn])
            move = raw_input("> ")
            if len(move) < 2:
                print "Type a real move, ya dope."
            else:
                print "got it."


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
