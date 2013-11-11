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

    # load all images
    # pieces format:
    # pieces[background id: 0 = white, 1 = black]["piece letter"]
    pieces = [{}, {}]
    # file names format:
    # (army color)(piece letter)(background color).png
    # white background
    pieces[0]["."] = pygame.image.load("./img/Generic/w.png")
     #black classic
    pieces[0]["p"] = pygame.image.load("./img/Classic/bpw.png")
    pieces[0]["b"] = pygame.image.load("./img/Classic/bbw.png")
    pieces[0]["n"] = pygame.image.load("./img/Classic/bnw.png")
    pieces[0]["r"] = pygame.image.load("./img/Classic/brw.png")
    pieces[0]["q"] = pygame.image.load("./img/Classic/bqw.png")
    pieces[0]["k"] = pygame.image.load("./img/Classic/bkw.png")
     #black nemesis
    pieces[0]["l"] = pygame.image.load("./img/Nemesis/blw.png")
    pieces[0]["m"] = pygame.image.load("./img/Nemesis/bmw.png")
     #black reaper
    pieces[0]["g"] = pygame.image.load("./img/Reaper/bgw.png")
    pieces[0]["a"] = pygame.image.load("./img/Reaper/baw.png")
     #black empowered
    pieces[0]["i"] = pygame.image.load("./img/Empowered/biw.png")
    pieces[0]["x"] = pygame.image.load("./img/Empowered/bxw.png")
    pieces[0]["y"] = pygame.image.load("./img/Empowered/byw.png")
    pieces[0]["z"] = pygame.image.load("./img/Empowered/bzw.png")
    pieces[0]["o"] = pygame.image.load("./img/Empowered/bow.png")
     #black two kings
    pieces[0]["u"] = pygame.image.load("./img/TwoKings/buw.png")
    pieces[0]["w"] = pygame.image.load("./img/TwoKings/bww.png")
     #black animals
    pieces[0]["t"] = pygame.image.load("./img/Animals/btw.png")
    pieces[0]["h"] = pygame.image.load("./img/Animals/bhw.png")
    pieces[0]["e"] = pygame.image.load("./img/Animals/bew.png")
    pieces[0]["j"] = pygame.image.load("./img/Animals/bjw.png")
     #black other
    pieces[0]["d"] = pygame.image.load("./img/Generic/bdw.png")
     #white classic
    pieces[0]["P"] = pygame.image.load("./img/Classic/wpw.png")
    pieces[0]["B"] = pygame.image.load("./img/Classic/wbw.png")
    pieces[0]["N"] = pygame.image.load("./img/Classic/wnw.png")
    pieces[0]["R"] = pygame.image.load("./img/Classic/wrw.png")
    pieces[0]["Q"] = pygame.image.load("./img/Classic/wqw.png")
    pieces[0]["K"] = pygame.image.load("./img/Classic/wkw.png")
     #white nemesis
    pieces[0]["L"] = pygame.image.load("./img/Nemesis/wlw.png")
    pieces[0]["M"] = pygame.image.load("./img/Nemesis/wmw.png")
     #white reaper
    pieces[0]["G"] = pygame.image.load("./img/Reaper/wgw.png")
    pieces[0]["A"] = pygame.image.load("./img/Reaper/waw.png")
     #white empowered
    pieces[0]["I"] = pygame.image.load("./img/Empowered/wiw.png")
    pieces[0]["X"] = pygame.image.load("./img/Empowered/wxw.png")
    pieces[0]["Y"] = pygame.image.load("./img/Empowered/wyw.png")
    pieces[0]["Z"] = pygame.image.load("./img/Empowered/wzw.png")
    pieces[0]["O"] = pygame.image.load("./img/Empowered/wow.png")
     #white two kings
    pieces[0]["U"] = pygame.image.load("./img/TwoKings/wuw.png")
    pieces[0]["W"] = pygame.image.load("./img/TwoKings/www.png")
     #white animals
    pieces[0]["T"] = pygame.image.load("./img/Animals/wtw.png")
    pieces[0]["H"] = pygame.image.load("./img/Animals/whw.png")
    pieces[0]["E"] = pygame.image.load("./img/Animals/wew.png")
    pieces[0]["J"] = pygame.image.load("./img/Animals/wjw.png")
     #white other
    pieces[0]["D"] = pygame.image.load("./img/Generic/wdw.png")
#######################################################
    # black background
    pieces[1]["."] = pygame.image.load("./img/Generic/b.png")
     #black classic
    pieces[1]["p"] = pygame.image.load("./img/Classic/bpb.png")
    pieces[1]["b"] = pygame.image.load("./img/Classic/bbb.png")
    pieces[1]["n"] = pygame.image.load("./img/Classic/bnb.png")
    pieces[1]["r"] = pygame.image.load("./img/Classic/brb.png")
    pieces[1]["q"] = pygame.image.load("./img/Classic/bqb.png")
    pieces[1]["k"] = pygame.image.load("./img/Classic/bkb.png")
     #black nemesis
    pieces[1]["l"] = pygame.image.load("./img/Nemesis/blb.png")
    pieces[1]["m"] = pygame.image.load("./img/Nemesis/bmb.png")
     #black reaper
    pieces[1]["g"] = pygame.image.load("./img/Reaper/bgb.png")
    pieces[1]["a"] = pygame.image.load("./img/Reaper/bab.png")
     #black empowered
    pieces[1]["i"] = pygame.image.load("./img/Empowered/bib.png")
    pieces[1]["x"] = pygame.image.load("./img/Empowered/bxb.png")
    pieces[1]["y"] = pygame.image.load("./img/Empowered/byb.png")
    pieces[1]["z"] = pygame.image.load("./img/Empowered/bzb.png")
    pieces[1]["o"] = pygame.image.load("./img/Empowered/bob.png")
     #black two kings
    pieces[1]["u"] = pygame.image.load("./img/TwoKings/bub.png")
    pieces[1]["w"] = pygame.image.load("./img/TwoKings/bwb.png")
     #black animals
    pieces[1]["t"] = pygame.image.load("./img/Animals/btb.png")
    pieces[1]["h"] = pygame.image.load("./img/Animals/bhb.png")
    pieces[1]["e"] = pygame.image.load("./img/Animals/beb.png")
    pieces[1]["j"] = pygame.image.load("./img/Animals/bjb.png")
     #black other
    pieces[1]["d"] = pygame.image.load("./img/Generic/bdb.png")
     #white classic
    pieces[1]["P"] = pygame.image.load("./img/Classic/wpb.png")
    pieces[1]["B"] = pygame.image.load("./img/Classic/wbb.png")
    pieces[1]["N"] = pygame.image.load("./img/Classic/wnb.png")
    pieces[1]["R"] = pygame.image.load("./img/Classic/wrb.png")
    pieces[1]["Q"] = pygame.image.load("./img/Classic/wqb.png")
    pieces[1]["K"] = pygame.image.load("./img/Classic/wkb.png")
     #white nemesis
    pieces[1]["L"] = pygame.image.load("./img/Nemesis/wlb.png")
    pieces[1]["M"] = pygame.image.load("./img/Nemesis/wmb.png")
     #white reaper
    pieces[1]["G"] = pygame.image.load("./img/Reaper/wgb.png")
    pieces[1]["A"] = pygame.image.load("./img/Reaper/wab.png")
     #white empowered
    pieces[1]["I"] = pygame.image.load("./img/Empowered/wib.png")
    pieces[1]["X"] = pygame.image.load("./img/Empowered/wxb.png")
    pieces[1]["Y"] = pygame.image.load("./img/Empowered/wyb.png")
    pieces[1]["Z"] = pygame.image.load("./img/Empowered/wzb.png")
    pieces[1]["O"] = pygame.image.load("./img/Empowered/wob.png")
     #white two kings
    pieces[1]["U"] = pygame.image.load("./img/TwoKings/wub.png")
    pieces[1]["W"] = pygame.image.load("./img/TwoKings/wwb.png")
     #white animals
    pieces[1]["T"] = pygame.image.load("./img/Animals/wtb.png")
    pieces[1]["H"] = pygame.image.load("./img/Animals/whb.png")
    pieces[1]["E"] = pygame.image.load("./img/Animals/web.png")
    pieces[1]["J"] = pygame.image.load("./img/Animals/wjb.png")
     #white other
    pieces[1]["D"] = pygame.image.load("./img/Generic/wdb.png")

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


