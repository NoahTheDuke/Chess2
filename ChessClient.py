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

        screen = pygame.display.set_mode((840, 480), 1)
        pygame.display.set_caption('ChessBoard Client')

        # load all images
        # pieces format:
        # pieces[background id: 0 = white, 1 = black]["piece letter"]
        pieces = [{}, {}]
        pieces[0]["."] = pygame.image.load("./img/Generic/w.png")
        pieces[1]["."] = pygame.image.load("./img/Generic/b.png")

        # file names format:
        # (army color)(piece letter)(background color).png
        # white background
        for img in chess.piece_to_army_dict:
            for color in chess.color_dict:
                for back in chess.color_dict:
                    if color == 0:
                        pieces[back][img] = pygame.image.load(
                            "./img/" +
                            chess.piece_to_army_dict[img] + "/" +
                            chess.color_dict[color] + img.lower() +
                            chess.color_dict[back] + ".png")
                    else:
                        img = img.lower()
                        pieces[back][img] = pygame.image.load(
                            "./img/" +
                            chess.piece_to_army_dict[img.upper()] + "/" +
                            chess.color_dict[color] + img +
                            chess.color_dict[back] + ".png")

        clock = pygame.time.Clock()

        posRect = pygame.Rect(0, 0, 60, 60)
        sidebarRect = pygame.Rect(480, 0, 360, 480)

        mousePos = [-1, -1]
        markPos = [-1, -1]
        validMoves = []
        pieceSelected = None

        gameResults = ["", "WHITE WINS!", "BLACK WINS!",
                       "STALEMATE", "DRAW BY THE FIFTHY MOVES RULE",
                       "DRAW BY THE THREE REPETITION RULE", "MIDLINE INVASION BY WHITE!",
                       "MIDLINE INVASION BY BLACK!"]

        while 1:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_LEFT:
                        chess.undo()
                    elif event.key == K_RIGHT:
                        chess.redo()
                    elif event.unicode in ("f", "F"):
                        print chess.getFEN()
                    elif event.unicode in ("a", "A"):
                        an = chess.getAllTextMoves(chess.AN)
                        if an:
                            print "AN: " + ", ".join(an)
                    elif event.unicode in ("s", "S"):
                        san = chess.getAllTextMoves(chess.SAN)
                        if san:
                            print "SAN: " + ", ".join(san)
                    elif event.unicode in ("l", "L"):
                        lan = chess.getAllTextMoves(chess.LAN)
                        if lan:
                            print "LAN: " + ", ".join(lan)
                    board = chess.getBoard()
                    turn = chess.getTurn()
                    markPos[0] = -1
                    validMoves = []

                if not chess.isGameOver():
                    if event.type == MOUSEMOTION:
                        mx = event.pos[0]
                        my = event.pos[1]
                        mousePos[0] = mx / 60
                        mousePos[1] = my / 60
                    elif event.type == MOUSEBUTTONDOWN:
                        if mousePos[0] != -1:
                            if markPos[0] == mousePos[0] and markPos[1] == mousePos[1]:
                                markPos[0] = -1
                                validMoves = []
                                pieceSelected = None
                            else:
                                if pieceSelected is None:
                                    if (turn == ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()) or \
                                       (turn == ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):
                                        markPos[0] = mousePos[0]
                                        markPos[1] = mousePos[1]
                                        validMoves = chess.getValidMoves(tuple(markPos))
                                        pieceSelected = board[markPos[1]][markPos[0]].upper
                                elif pieceSelected == ("H" or "E"):
                                    if markPos[0] != -1:
                                        res = chess.addMove(markPos, mousePos)
                                        if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                                            chess.setPromotion(chess.QUEEN)
                                            res = chess.addMove(markPos, mousePos)
                                        if res:
                                            print chess.getLastTextMove(chess.SAN)
                                            board = chess.getBoard()
                                            turn = chess.getTurn()
                                            chess.updateRoyalLocations()
                                            markPos[0] = -1
                                            validMoves = []
                                            pieceSelected = None
                                else:
                                    if markPos[0] != -1:
                                        res = chess.addMove(markPos, mousePos)
                                        if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                                            chess.setPromotion(chess.QUEEN)
                                            res = chess.addMove(markPos, mousePos)
                                        if res:
                                            print chess.getLastTextMove(chess.SAN)
                                            board = chess.getBoard()
                                            turn = chess.getTurn()
                                            chess.updateRoyalLocations()
                                            markPos[0] = -1
                                            validMoves = []
                                            pieceSelected = None

                if chess.isGameOver():
                    pygame.display.set_caption("Game Over! %s" % gameResults[chess.getGameResult()])
                    validMove = []
                    markPos[0] = -1
                    markPos[1] = -1
                else:
                    pygame.display.set_caption('ChessBoard Client')

                y = 0
                for rank in board:
                    x = 0
                    for p in rank:
                        screen.blit(pieces[(x + y) % 2][p], (x * 60, y * 60))
                        x += 1
                    y += 1

                if markPos[0] != -1:
                    posRect.left = markPos[0] * 60
                    posRect.top = markPos[1] * 60
                    pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

                for v in validMoves:
                    posRect.left = v[0] * 60
                    posRect.top = v[1] * 60
                    pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

                pygame.draw.rect(screen, (0, 0, 0), sidebarRect, 0)
                pygame.display.flip()


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
