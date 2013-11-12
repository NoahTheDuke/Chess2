#/usr/bin/env python

from ChessBoard import ChessBoard

import os, pygame, math
from pygame.locals import *

from pprint import pprint

class ChessClient:
  def mainLoop(self):
    pygame.init()

    print "White Player, choose an army:"
    print "1. Classic   2. Nemesis   3. Reaper"
    print "4. Empowered 5. Two Kings 6. Animals"
    wArmy = raw_input("Type the number, not the name: ")
    print "Black Player, choose an army:"
    print "1. Classic   2. Nemesis   3. Reaper"
    print "4. Empowered 5. Two Kings 6. Animals"
    bArmy = raw_input("Type the number, not the name: ")

    pieces = {}
    chess = ChessBoard(int(wArmy), int(bArmy))
    board = chess.getBoard()
    turn = chess.getTurn()

    screen = pygame.display.set_mode((480, 480), 1)
    pygame.display.set_caption('ChessBoard Client')
    
    img_dict = {
        "P": "Classic",
        "B": "Classic",
        "N": "Classic",
        "R": "Classic",
        "Q": "Classic",
        "K": "Classic",
        "L": "Nemesis",
        "M": "Nemesis",
        "G": "Reaper",
        "A": "Reaper",
        "X": "Empowered",
        "Y": "Empowered",
        "Z": "Empowered",
        "I": "Empowered",
        "O": "Empowered",
        "U": "TwoKings",
        "W": "TwoKings",
        "T": "Animals",
        "H": "Animals",
        "E": "Animals",
        "J": "Animals",
        "D": "Generic",
        "C": "Generic"
        }

    color_dict = {
        0: "w",
        1: "b"
        }

    # load all images
    # pieces format:
    # pieces[background id: 0 = white, 1 = black]["piece letter"]
    pieces = [{}, {}]
    # file names format:
    # (army color)(piece letter)(background color).png
    # white background
    pieces[0]["."] = pygame.image.load("./img/Generic/w.png")
    pieces[1]["."] = pygame.image.load("./img/Generic/b.png")

    for img in img_dict:
      for color in color_dict:
        for back in color_dict:
          if color == 0:
            pieces[back][str(img)] = pygame.image.load("./img/" + str(img_dict[img]) + "/" + str(color_dict[color]) + str(img).lower() + str(color_dict[back]) + ".png")
          else:
            img = img.lower()
            pieces[back][str(img)] = pygame.image.load("./img/" + str(img_dict[img.upper()]) + "/" + str(color_dict[color]) + str(img) + str(color_dict[back]) + ".png")
    print str(pieces)

    clock = pygame.time.Clock()

    posRect = pygame.Rect(0, 0, 60, 60)

    mousePos = [-1, -1]
    markPos = [-1, -1]
    validMoves = []
    pieceSelected = None

    gameResults = ["", "WHITE WINS!", "BLACK WINS!", "STALEMATE", "DRAW BY THE FIFTHY MOVES RULE", "DRAW BY THE THREE REPETITION RULE"]

    while 1:
      clock.tick(30)

      for event in pygame.event.get():
        if event.type ==  QUIT:
          return
        elif event.type == KEYDOWN:
          if event.key ==  K_ESCAPE:
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
            mousePos[0] = mx/60
            mousePos[1] = my/60
          elif event.type ==  MOUSEBUTTONDOWN:
            if mousePos[0] != -1:
              if markPos[0] == mousePos[0] and markPos[1] == mousePos[1]:
                markPos[0] = -1
                validMoves = []
                pieceSelected = None
              else:
                if pieceSelected == None:
                  if (turn == ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()) or \
                     (turn == ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):
                    markPos[0] = mousePos[0]
                    markPos[1] = mousePos[1]
                    validMoves = chess.getValidMoves(tuple(markPos))
                    pieceSelected = board[markPos[1]][markPos[0]].upper
                elif pieceSelected == ("H" or "E"):
                  if markPos[0] !=  -1:
                    res = chess.addMove(markPos, mousePos)
                    if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                      chess.setPromotion(chess.QUEEN)
                      res = chess.addMove(markPos, mousePos)
                    if res:
                      print chess.getLastTextMove(chess.SAN)
                      board = chess.getBoard()
                      turn = chess.getTurn()
                      markPos[0] = -1
                      validMoves = []
                      pieceSelected = None
                else:
                  if markPos[0] !=  -1:
                    res = chess.addMove(markPos, mousePos)
                    if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                      chess.setPromotion(chess.QUEEN)
                      res = chess.addMove(markPos, mousePos)
                    if res:
                      print chess.getLastTextMove(chess.SAN)
                      board = chess.getBoard()
                      turn = chess.getTurn()
                      markPos[0] = -1
                      validMoves = []
                      pieceSelected = None

        if chess.isGameOver():
          pygame.display.set_caption("Game Over! (Reason:%s)" % gameResults[chess.getGameResult()])
          validMove = []
          markPos[0] = -1
          markPos[1] = -1
        else:
          pygame.display.set_caption('ChessBoard Client')

        y = 0
        for rank in board:
          x = 0
          for p in rank:
            screen.blit(pieces[(x+y)%2][p], (x*60, y*60))
            x+= 1
          y+= 1

        if markPos[0] != -1:
          posRect.left = markPos[0]*60
          posRect.top = markPos[1]*60
          pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

        for v in validMoves:
          posRect.left = v[0]*60
          posRect.top = v[1]*60
          pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

        pygame.display.flip()

def main():
  g = ChessClient()
  g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
  main()

