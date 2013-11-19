#/usr/bin/env python

from ChessBoard import ChessBoard
import sys
import math
import string
from itertools import izip_longest


class ChessClient:
    def grouped(self, iterable, n):
        "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
        return izip_longest(*[iter(iterable)] * n)

    def mainLoop(self):
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

        while True:
            chess.printBoard()
            if not chess.isGameOver():
                if chess._turn == chess.BLACK:
                    curArmy = chess._black_army
                else:
                    curArmy = chess._white_army
                if chess._secondTurn:
                    print "%s's Warrior King turn. Type your move, or type \"decline\" to skip." % str(chess.value_to_color_dict[turn])
                else:
                    print "%s's turn. Type your move." % str(chess.value_to_color_dict[turn])
                move = raw_input("> ")
                if move == "exit":
                    sys.exit(0)
                elif any(var in move for var in ("AN", "an")):
                    an = chess.getAllTextMoves(chess.AN)
                    if an:
                        for x, y in self.grouped(an, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("SAN", "san")):
                    san = chess.getAllTextMoves(chess.SAN)
                    if san:
                        for x, y in self.grouped(an, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("LAN", "lan")):
                    lan = chess.getAllTextMoves(chess.LAN)
                    if lan:
                        for x, y in self.grouped(an, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("FEN", "fen")):
                    print chess.getFEN()
                elif len(move) < 2:
                    print "Type a real move."
                elif move == "whirlwind":
                    if curArmy == chess.TWOKINGS:
                        print "Which Warrior King performs the whirlwind?"
                        while True:
                            location = raw_input("> ")
                            if len(location) != 2:
                                print "Please only enter the square."
                            else:
                                location = chess.locationToTuple(location)
                                res = chess.moveTwoKingsWhirlwind(location)
                                if not res:
                                    print "Can't whirlwind there."
                                board = chess.getBoard()
                                turn = chess.getTurn()
                                break
                    else:
                        print "You're not playing Two Kings!"
                elif move == "decline":
                    if curArmy == chess.TWOKINGS:
                        if chess._secondTurn:
                            print "Second turn skipped."
                            chess._secondTurn = False
                            if chess._turn == chess.BLACK:
                                chess._turn = chess.WHITE
                            else:
                                chess._turn = chess.BLACK
                            board = chess.getBoard()
                            turn = chess.getTurn()
                    else:
                        print "You're not playing Two Kings!"
                else:
                    res = chess.addTextMove(move)
                    if res:
                        board = chess.getBoard()
                        turn = chess.getTurn()
                        chess.updateRoyalLocations()
                    else:
                        print "%s" % chess.move_reason_list[chess.getReason()]
            else:
                break
        chess.printBoard()
        print "Game over! %s" % chess.game_result_list[chess.getGameResult()]


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
