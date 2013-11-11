#/usr/bin/env python

from ChessBoard import ChessBoard

import os, pygame, math
from pygame.locals import *

from pprint import pprint

class ChessClient:
  def mainLoop(self):
    pygame.init()

    pieces = {}
    chess = ChessBoard("Classic", "Nemesis")
    board = chess.getBoard()
    turn = chess.getTurn()

    screen = pygame.display.set_mode((480, 480), 1)
    pygame.display.set_caption('ChessBoard Client')

    # load all images
    # file names format:
    # (army color)(piece letter)(background color).png
    # pieces format:
    # pieces[background id: 0 = white, 1 = black]["piece letter"]
    pieces = [{}, {}]
    # white background
     #black classic
    pieces[0]["p"] = pygame.image.load("./img/bpw.png")
    pieces[0]["b"] = pygame.image.load("./img/bbw.png")
    pieces[0]["n"] = pygame.image.load("./img/bnw.png")
    pieces[0]["r"] = pygame.image.load("./img/brw.png")
    pieces[0]["q"] = pygame.image.load("./img/bqw.png")
    pieces[0]["k"] = pygame.image.load("./img/bkw.png")
     #black nemesis
    pieces[0]["l"] = pygame.image.load("./img/blw.png")
    pieces[0]["m"] = pygame.image.load("./img/bmw.png")
     #black reaper
    pieces[0]["g"] = pygame.image.load("./img/bgw.png")
    pieces[0]["a"] = pygame.image.load("./img/baw.png")
     #black empowered
    pieces[0]["i"] = pygame.image.load("./img/biw.png")
    pieces[0]["x"] = pygame.image.load("./img/bxw.png")
    pieces[0]["y"] = pygame.image.load("./img/byw.png")
    pieces[0]["z"] = pygame.image.load("./img/bzw.png")
    pieces[0]["o"] = pygame.image.load("./img/bqw.png")
     #black two kings
    pieces[0]["u"] = pygame.image.load("./img/buw.png")
    pieces[0]["w"] = pygame.image.load("./img/bww.png")
     #black animals
    pieces[0]["t"] = pygame.image.load("./img/bbw.png")
    pieces[0]["h"] = pygame.image.load("./img/bnw.png")
    pieces[0]["e"] = pygame.image.load("./img/brw.png")
    pieces[0]["j"] = pygame.image.load("./img/bqw.png")
     #black other
    pieces[0]["d"] = pygame.image.load("./img/bdw.png")
     #white classic
    pieces[0]["P"] = pygame.image.load("./img/wpw.png")
    pieces[0]["B"] = pygame.image.load("./img/wbw.png")
    pieces[0]["N"] = pygame.image.load("./img/wnw.png")
    pieces[0]["R"] = pygame.image.load("./img/wrw.png")
    pieces[0]["Q"] = pygame.image.load("./img/wqw.png")
    pieces[0]["K"] = pygame.image.load("./img/wkw.png")
     #white nemesis
    pieces[0]["L"] = pygame.image.load("./img/wlw.png")
    pieces[0]["M"] = pygame.image.load("./img/wmw.png")
     #white reaper
    pieces[0]["G"] = pygame.image.load("./img/wgw.png")
    pieces[0]["A"] = pygame.image.load("./img/waw.png")
     #white empowered
    pieces[0]["I"] = pygame.image.load("./img/wiw.png")
    pieces[0]["X"] = pygame.image.load("./img/wxw.png")
    pieces[0]["Y"] = pygame.image.load("./img/wyw.png")
    pieces[0]["Z"] = pygame.image.load("./img/wzw.png")
    pieces[0]["O"] = pygame.image.load("./img/wqw.png")
     #white two kings
    pieces[0]["U"] = pygame.image.load("./img/wuw.png")
    pieces[0]["W"] = pygame.image.load("./img/www.png")
     #white animals
    pieces[0]["T"] = pygame.image.load("./img/wbw.png")
    pieces[0]["H"] = pygame.image.load("./img/wnw.png")
    pieces[0]["E"] = pygame.image.load("./img/wrw.png")
    pieces[0]["J"] = pygame.image.load("./img/wqw.png")
     #white other
    pieces[0]["D"] = pygame.image.load("./img/wdw.png")
    # white background
    pieces[0]["."] = pygame.image.load("./img/w.png")
#######################################################
    # black background
     #black classic
    pieces[1]["p"] = pygame.image.load("./img/bpb.png")
    pieces[1]["b"] = pygame.image.load("./img/bbb.png")
    pieces[1]["n"] = pygame.image.load("./img/bnb.png")
    pieces[1]["r"] = pygame.image.load("./img/brb.png")
    pieces[1]["q"] = pygame.image.load("./img/bqb.png")
    pieces[1]["k"] = pygame.image.load("./img/bkb.png")
     #black nemesis
    pieces[1]["l"] = pygame.image.load("./img/blb.png")
    pieces[1]["m"] = pygame.image.load("./img/bmb.png")
     #black reaper
    pieces[1]["g"] = pygame.image.load("./img/bgb.png")
    pieces[1]["a"] = pygame.image.load("./img/bab.png")
     #black empowered
    pieces[1]["i"] = pygame.image.load("./img/bib.png")
    pieces[1]["x"] = pygame.image.load("./img/bxb.png")
    pieces[1]["y"] = pygame.image.load("./img/byb.png")
    pieces[1]["z"] = pygame.image.load("./img/bzb.png")
    pieces[1]["o"] = pygame.image.load("./img/bqb.png")
     #black two kings
    pieces[1]["u"] = pygame.image.load("./img/bub.png")
    pieces[1]["w"] = pygame.image.load("./img/bwb.png")
     #black animals
    pieces[1]["t"] = pygame.image.load("./img/bbb.png")
    pieces[1]["h"] = pygame.image.load("./img/bnb.png")
    pieces[1]["e"] = pygame.image.load("./img/brb.png")
    pieces[1]["j"] = pygame.image.load("./img/bqb.png")
     #black other
    pieces[1]["d"] = pygame.image.load("./img/bdb.png")
     #white classic
    pieces[1]["P"] = pygame.image.load("./img/wpb.png")
    pieces[1]["B"] = pygame.image.load("./img/wbb.png")
    pieces[1]["N"] = pygame.image.load("./img/wnb.png")
    pieces[1]["R"] = pygame.image.load("./img/wrb.png")
    pieces[1]["Q"] = pygame.image.load("./img/wqb.png")
    pieces[1]["K"] = pygame.image.load("./img/wkb.png")
     #white nemesis
    pieces[1]["L"] = pygame.image.load("./img/wlb.png")
    pieces[1]["M"] = pygame.image.load("./img/wmb.png")
     #white reaper
    pieces[1]["G"] = pygame.image.load("./img/wgb.png")
    pieces[1]["A"] = pygame.image.load("./img/wab.png")
     #white empowered
    pieces[1]["I"] = pygame.image.load("./img/wib.png")
    pieces[1]["X"] = pygame.image.load("./img/wxb.png")
    pieces[1]["Y"] = pygame.image.load("./img/wyb.png")
    pieces[1]["Z"] = pygame.image.load("./img/wzb.png")
    pieces[1]["O"] = pygame.image.load("./img/wqb.png")
     #white two kings
    pieces[1]["U"] = pygame.image.load("./img/wub.png")
    pieces[1]["W"] = pygame.image.load("./img/wwb.png")
     #white animals
    pieces[1]["T"] = pygame.image.load("./img/wbb.png")
    pieces[1]["H"] = pygame.image.load("./img/wnb.png")
    pieces[1]["E"] = pygame.image.load("./img/wrb.png")
    pieces[1]["J"] = pygame.image.load("./img/wqb.png")
     #white other
    pieces[1]["D"] = pygame.image.load("./img/wdb.png")
    # black background
    pieces[0]["."] = pygame.image.load("./img/b.png")

    clock = pygame.time.Clock()

    posRect = pygame.Rect(0, 0, 60, 60)

    mousePos = [-1, -1]
    markPos = [-1, -1]
    validMoves = []

    gameResults = ["", "WHITE WINS!", "BLACK WINS!", "STALEMATE", "DRAW BY THE FIFTHY MOVES RULE", "DRAW BY THE THREE REPETITION RULE"]

    while 1:
      clock.tick(30)

      for event in pygame.event.get():
        if event.type ==  QUIT:
          return
        elif event.type ==  KEYDOWN:
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
          if event.type ==  MOUSEMOTION:
            mx = event.pos[0]
            my = event.pos[1]
            mousePos[0] = mx/60
            mousePos[1] = my/60
          elif event.type ==  MOUSEBUTTONDOWN:
            if mousePos[0] !=  -1:
              if markPos[0] ==  mousePos[0] and markPos[1] ==  mousePos[1]:
                markPos[0] = -1
                validMoves = []
              else:
                if (turn == ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()) or \
                   (turn == ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):
                  markPos[0] = mousePos[0]
                  markPos[1] = mousePos[1]
                  validMoves = chess.getValidMoves(tuple(markPos))

                else:
                  if markPos[0] !=  -1:
                    res = chess.addMove(markPos, mousePos)
                    if not res and chess.getReason() ==  chess.MUST_SET_PROMOTION:
                      chess.setPromotion(chess.QUEEN)
                      res = chess.addMove(markPos, mousePos)
                    if res:
                      #print chess.getLastMove()
                      print chess.getLastTextMove(chess.SAN)
                      board = chess.getBoard()
                      turn = chess.getTurn()
                      markPos[0] = -1
                      validMoves = []

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

        if markPos[0] !=  -1:
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
if __name__ ==  '__main__': main()


