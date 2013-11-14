#/usr/bin/env python

from ChessBoard import ChessBoard
import pygame
from pygame.locals import *
import string
from py_menu import Option


class ChessClient:
    options = []

    def __init__(self, size, caption):
        pygame.init()
        self.menu_font = pygame.font.Font(None, 40)
        self.posRect = pygame.Rect(0, 0, 60, 60)
        self.sidebarRect = pygame.Rect(480, 0, 360, 480)
        self.mainLoop(size, caption)

    def getArmies(self, screen, wArmy, bArmy):
        self.options = [Option(screen, self.menu_font, "White:", (480, 0),
                              (50, 30), (255, 255, 255), (255, 255, 255))]

        for army in ChessBoard.army_names2:
            self.options.append(Option(screen, self.menu_font,
                                       ChessBoard.army_names2[army], (480, 0),
                                      (50, 35 * (army + 1)), (100, 100, 100),
                                      (255, 255, 255)))

        #print "White Player, choose an army:"
        #print "1. Classic   2. Nemesis   3. Reaper"
        #print "4. Empowered 5. Two Kings 6. Animals"
        #while True:
            #userInput = raw_input('Type the number, not the name:')
            #if userInput == "":
                #print 'Please enter something.'
            #elif userInput in string.digits:
                #if int(userInput) < 7:
                    #if int(userInput) > 0:
                        #break
                #print 'Please enter only one of the above.'
            #else:
                #print 'Please enter only one character'
        #wArmy = userInput

        #print "Black Player, choose an army:"
        #print "1. Classic   2. Nemesis   3. Reaper"
        #print "4. Empowered 5. Two Kings 6. Animals"
        #while True:
            #userInput = raw_input('Type the number, not the name:')
            #if userInput == "":
                #print 'Please enter something.'
            #elif userInput in string.digits:
                #if int(userInput) < 7:
                    #if int(userInput) > 0:
                        #break
                #print 'Please enter only one of the above.'
            #else:
                #print 'Please enter only one of the above.'
        #bArmy = userInput
        return (wArmy, bArmy)

    def mainLoop(self, size, caption):
        self.size = size
        self.caption = caption

        self.pieces = {}
        chess = ChessBoard(0, 0)
        board = chess.getBoard()
        turn = chess.getTurn()

        screen = pygame.display.set_mode(self.size, 1)
        pygame.display.set_caption(self.caption)
        wArmy, bArmy = self.getArmies(screen, 0, 0)
        clock = pygame.time.Clock()

        chess.resetBoard(int(wArmy), int(bArmy))
        board = chess.getBoard()
        turn = chess.getTurn()

        # load all images
        # pieces format:
        # pieces[background id: 0 = white, 1 = black]["piece letter"]
        self.pieces = [{}, {}]
        self.pieces[0]["."] = pygame.image.load("./img/Generic/w.png")
        self.pieces[1]["."] = pygame.image.load("./img/Generic/b.png")

        # file names format:
        # (army color)(piece letter)(background color).png
        # white background
        for img in chess.piece_to_army_dict:
            for color in chess.color_dict:
                for back in chess.color_dict:
                    if color == 0:
                        self.pieces[back][img] = (
                            pygame.image.load("./img/" +
                                              chess.piece_to_army_dict[img] +
                                              "/" + chess.color_dict[color] +
                                              img.lower() +
                                              chess.color_dict[back] + ".png"))
                    else:
                        img = img.lower()
                        self.pieces[back][img] = (
                            pygame.image.load("./img/" +
                                              chess.piece_to_army_dict[
                                                  img.upper()] + "/" +
                                              chess.color_dict[color] + img +
                                              chess.color_dict[back] + ".png"))

        mousePos = [-1, -1]
        markPos = [-1, -1]
        validMoves = []
        pieceSelected = None

        gameResults = ["", "WHITE WINS!", "BLACK WINS!",
                       "STALEMATE", "DRAW BY THE FIFTHY MOVES RULE",
                       "DRAW BY THE THREE REPETITION RULE",
                       "MIDLINE INVASION BY WHITE!",
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
                    mx, my = pygame.mouse.get_pos()
                    mousePos[0] = mx/60
                    mousePos[1] = my/60
                    if mx > 480:
                        pass
                    else:
                        pass
                    if event.type == MOUSEBUTTONDOWN:
                        if mx > 480:
                            pass
                        elif mousePos[0] != -1:
                            if (markPos[0] == mousePos[0] and
                                    markPos[1] == mousePos[1]):
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
                                            board = chess.getBoard()
                                            turn = chess.getTurn()
                                            chess.updateRoyalLocations()
                                            markPos[0] = -1
                                            validMoves = []
                                            pieceSelected = None

                if chess.isGameOver():
                    pygame.display.set_caption("Game Over! %s" % gameResults[chess.getGameResult()])
                    validMoves = []
                    markPos[0] = -1
                    markPos[1] = -1
                y = 0
                for rank in board:
                    x = 0
                    for p in rank:
                        screen.blit(self.pieces[(x + y) % 2][p], (x * 60, y * 60))
                        x += 1
                    y += 1

                if markPos[0] != -1:
                    self.draw(screen, board, self.posRect, markPos)
                for v in validMoves:
                    self.draw(screen, board, self.posRect, v)
                self.drawSidebar(screen, board, self.sidebarRect, self.options)
                pygame.display.flip()

    def drawBoard(self, screen, board, rect, items):
        rect.left = items[0] * 60
        rect.top = items[1] * 60
        pygame.draw.rect(screen, (255, 255, 0), rect, 4)

    def drawSidebar(self, screen, board, rect, options):
        pygame.draw.rect(screen, (0, 0, 0), self.sidebarRect, 0)
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw(screen, self.menu_font)


def main():
    g = ChessClient((840, 480), "Chess 2: The Sequel")

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
