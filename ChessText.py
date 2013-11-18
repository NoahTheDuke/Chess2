#/usr/bin/env python

from ChessBoard import ChessBoard

import os
import sys
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

        while 1:
            if not chess.isGameOver():
                chess.printBoard()
                print "%s's turn. Type your move." % str(chess.value_to_color_dict[turn])
                move = raw_input("> ")
                if move == "exit":
                    sys.exit(0)
                elif len(move) < 2:
                    print "Type a real move, ya dope."
                else:
                    res = chess.addTextMove(move)
                    if res:
                        print chess.getLastTextMove(chess.SAN)
                        board = chess.getBoard()
                        turn = chess.getTurn()
                        chess.updateRoyalLocations()


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
