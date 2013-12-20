#/usr/bin/env python

from ChessBoard import ChessBoard
import sys
import getpass
import time
import string


class ChessClient:

    def mainLoop(self):
        print("White Player, choose an army:")
        print("1. Classic   2. Nemesis   3. Reaper")
        print("4. Empowered 5. Two Kings 6. Animals")
        while True:
            print('Type the number, not the name.')
            userInput = getpass.getpass('> ')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print('Please enter only one of the above.')
            else:
                print('Please enter only one character')
        wArmy = userInput

        print("Black Player, choose an army:")
        print("1. Classic   2. Nemesis   3. Reaper")
        print("4. Empowered 5. Two Kings 6. Animals")
        while True:
            print('Type the number, not the name.')
            userInput = getpass.getpass('> ')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print('Please enter only one of the above.')
            else:
                print('Please enter only one of the above.')
        bArmy = userInput

        turn = 0
        chess = ChessBoard(int(wArmy), int(bArmy))
        turn = chess.getTurn()

        prototype = []
        prototype.append('[Event "Sample Games"]')
        prototype.append('[Site "' + 'Fantasy Strike Website' '\"]')
        prototype.append('[Date "' + ".".join((time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"))) + '"]')
        prototype.append('[Round "' + '-' + '"]')
        prototype.append('[White "' + chess.army_name_dict[int(wArmy)] + '"]')
        prototype.append('[Black "' + chess.army_name_dict[int(bArmy)] + '"]')

        while True:
            board = chess.printBoard()
            for row in board:
                print(row)
            if not chess.isGameOver():
                if chess._turn == chess.BLACK:
                    curArmy = chess._black_army
                else:
                    curArmy = chess._white_army
                if chess._secondTurn:
                    print("{}'s Warrior King turn. Type your move, or type \"decline\" to skip.".format(str(chess.value_to_color_dict[turn])))
                else:
                    print("{}'s turn. Type your move.".format(str(chess.value_to_color_dict[turn])))
                move = input("> ")
                # Fully quit the program, regardless.
                if move == "exit":
                    sys.exit(0)
                # Save the current game as a pgn file.
                elif move == "save":
                    f = open('san.pgn', 'w')
                    acc = ""
                    save = chess.getAllTextMoves(chess.SAN)
                    for moves in save:
                        length, w, b = moves
                        if b is None:
                            b = ""
                        acc = acc + "{}. {} {} ".format(length, w, b)
                    pgn_details = prototype
                    pgn_details.append('[Result "' + chess.pgn_result_list[chess.getGameResult()] + '"]')
                    pgn_details.append('')
                    pgn_details.append(acc.rstrip())
                    for x in pgn_details:
                        f.write(str(x) + '\n')
                    f.close()
                elif any(var in move for var in ("SAN", "san")):
                    san = chess.getAllTextMoves(chess.SAN)
                    if san:
                        for moves in san:
                            length, x, y = moves
                            print("{}. {} {}".format(length, x, y))
                elif any(var in move for var in ("LAN", "lan")):
                    lan = chess.getAllTextMoves(chess.LAN)
                    if lan:
                        for moves in lan:
                            length, x, y = moves
                            print("{}. {} {}".format(length, x, y))
                elif any(var in move for var in ("AN", "an")):
                    an = chess.getAllTextMoves(chess.AN)
                    if an:
                        for moves in an:
                            length, x, y = moves
                            print("{}. {} {}".format(length, x, y))
                elif any(var in move for var in ("FEN", "fen")):
                    print(chess.getFEN())
                elif len(move) < 2:
                    print("Type a real move.")
                elif any(var in move for var in ("whirlwind", "ww", "Whirlwind", "WW")):
                    if curArmy == chess.TWOKINGS:
                        print("Which Warrior King performs the whirlwind?")
                        while True:
                            location = input("> ")
                            if location == "exit":
                                sys.exit(0)
                            elif len(location) != 2:
                                print("Please only enter the square.")
                            else:
                                res = chess.addTextMove("K" + location, secondTurn=chess._secondTurn, whirlwind=True)
                                if not res:
                                    print("Can't whirlwind there.")
                                turn = chess.getTurn()
                                break
                    else:
                        print("You're not playing Two Kings!")
                elif any(var in move for var in ("decline", "Decline", "skip", "s", "Skip", "S")):
                    if curArmy == chess.TWOKINGS:
                        if chess._secondTurn:
                            print("Second turn skipped.")
                            chess._secondTurn = False
                            if chess._turn == chess.BLACK:
                                chess._turn = chess.WHITE
                            else:
                                chess._turn = chess.BLACK
                            turn = chess.getTurn()
                    else:
                        print("You're not playing Two Kings!")
                else:
                    res = chess.checkTextMove(move)
                    if res == -1:
                        result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                        if result:
                            print(chess.getLastTextMove(chess.SAN))
                            turn = chess.getTurn()
                            chess.updateRoyalLocations()
                        elif chess.getReason() == chess.MUST_SET_PROMOTION:
                            print("{}, what do you want to promote to?".format(chess.value_to_color_dict[turn]))
                            print('Please enter the letter of the piece: QRNB.')
                            while True:
                                promo = input("> ")
                                if promo in string.letters:
                                    if len(promo) < 2:
                                        if int(promo) > 0:
                                            break
                                        print('Please enter the letter of the piece: QRNB.')
                                    print('Please enter the letter of the piece: QRNB.')
                                else:
                                    print('Please enter the letter of the piece: QRNB.')
                            chess.setPromotion(promo)
                            result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                            if result:
                                print(chess.getLastTextMove(chess.SAN))
                                turn = chess.getTurn()
                                chess.updateRoyalLocations()
                            else:
                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                        else:
                            print("{}".format(chess.move_reason_list[chess.getReason()]))
                    elif res is False:
                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                    else:
                        if turn == 0:
                            unturn = 1
                        else:
                            unturn = 0
                        print("{}, would you like to initiate a duel? It will cost {}.".format(str(chess.value_to_color_dict[unturn]), res))
                        while True:
                            answer = input("> ")
                            if answer == "exit":
                                sys.exit(0)
                            elif any(var in answer for var in ('y', 'Y', 'Yes', 'yes')):
                                chess.payDuelCost(res)
                                print("White stones: {}".format(chess.getStones(chess.WHITE)))
                                print("Black stones: {}".format(chess.getStones(chess.BLACK)))
                                print("{}, how much would you like to bid?".format(str(chess.value_to_color_dict[unturn])))
                                while True:
                                    defending_bid = getpass.getpass("> ")
                                    if defending_bid == "exit":
                                        sys.exit(0)
                                    elif defending_bid in string.digits:
                                        if int(defending_bid) < 3:
                                            if int(defending_bid) > -1:
                                                break
                                            print('Please only bid a number of stones between 0 and 2.')
                                        print('Please only bid a number of stones between 0 and 2.')
                                    else:
                                        print('Please only bid a number of stones between 0 and 2.')
                                print("{}, how much would you like to bid?".format(str(chess.value_to_color_dict[turn])))
                                while True:
                                    attacking_bid = getpass.getpass("> ")
                                    if attacking_bid == "exit":
                                        sys.exit(0)
                                    elif attacking_bid in string.digits:
                                        if int(attacking_bid) < 3:
                                            if int(attacking_bid) > -1:
                                                break
                                            print('Please only bid a number of stones between 0 and 2.')
                                        print('Please only bid a number of stones between 0 and 2.')
                                    else:
                                        print('Please only bid a number of stones between 0 and 2.')
                                duel_results = chess.initiateDuel(int(attacking_bid), int(defending_bid))
                                # duel_results will now be either None, 1, or 2
                                print("{} bid: {}".format(chess.value_to_color_dict[chess._turn], int(attacking_bid)))
                                print("{} bid: {}".format(chess.value_to_color_dict[chess._unturn], int(defending_bid)))
                                if duel_results is None:
                                    print("Someone tried to bid too much!")
                                    break
                                elif duel_results == chess.BLUFF:
                                    print("{} called the bluff! Do you want to gain a stone or force {} to lose a stone?".format(
                                        chess.value_to_color_dict[chess._turn], chess.value_to_color_dict[chess._unturn]))
                                    while True:
                                        bluff_choice = input("> ")
                                        if bluff_choice == "exit":
                                            sys.exit(0)
                                        elif any(var in bluff_choice for var in ("g", "gain", "G", "Gain")):
                                            chess.calledBluff(1)
                                            att_result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                            if att_result:
                                                print(chess.getLastTextMove(chess.SAN))
                                                turn = chess.getTurn()
                                                chess.updateRoyalLocations()
                                                break
                                            else:
                                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                break
                                        elif any(var in bluff_choice for var in ("l", "lose", "L", "Lose")):
                                            chess.calledBluff(-1)
                                            att_result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                            if att_result:
                                                print(chess.getLastTextMove(chess.SAN))
                                                turn = chess.getTurn()
                                                chess.updateRoyalLocations()
                                                break
                                            else:
                                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                break
                                        else:
                                            print('Please choose between gaining a stone and forcing a lose of a stone.')
                                elif duel_results == chess.ATT_WIN:
                                    print("Attacker wins!")
                                    att_result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                    if att_result:
                                        print(chess.getLastTextMove(chess.SAN))
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                else:
                                    print("Defender wins!")
                                    att_result = chess.addTextMove(move, secondTurn=chess._secondTurn, clearLocation=True)
                                    if att_result:
                                        print(chess.getLastTextMove(chess.SAN))
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                turn = chess.getTurn()
                                break
                            else:
                                result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                if result:
                                    print(chess.getLastTextMove(chess.SAN))
                                    turn = chess.getTurn()
                                    chess.updateRoyalLocations()
                                elif chess.getReason() == chess.MUST_SET_PROMOTION:
                                    print("{}, what do you want to promote to?".format(chess.value_to_color_dict[turn]))
                                    print('Please enter the letter of the piece: QRNB.')
                                    while True:
                                        promo = input("> ")
                                        promo = str(promo.upper())
                                        if len(promo) == 1:
                                            if any(var in promo for var in ("Q", "R", "N", "B")):
                                                break
                                            print('Please enter the letter of the piece: QRNB.')
                                        print('Please enter the letter of the piece: QRNB.')
                                    chess.setPromotion(promo)
                                    result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                    if result:
                                        print(chess.getLastTextMove(chess.SAN))
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                else:
                                    print("{}".format(chess.move_reason_list[chess.getReason()]))
                                break
                            break
            else:
                break
        f = open('san.pgn', 'w')
        acc = ""
        save = chess.getAllTextMoves(chess.SAN)
        for moves in save:
            length, w, b = moves
            if b is None:
                b = ""
            acc = acc + "{}. {} {} ".format(length, w, b)
        acc = acc + chess.pgn_result_list[chess.getGameResult()]
        pgn_details = prototype
        pgn_details.append('[Result "' + chess.pgn_result_list[chess.getGameResult()] + '"]')
        pgn_details.append('')
        pgn_details.append(acc.rstrip())
        for x in pgn_details:
            f.write(str(x) + '\n')
        f.close()
        print("Game over! {}".format(chess.game_result_list[chess.getGameResult()]))


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
