#/usr/bin/env python

from ChessBoard import ChessBoard
import sys
import getpass
import time
import string


class ChessClient:

    def mainLoop(self):
        print("White Player, choose an army:")
        print("1. Classic   2. Nemesis   3. Empowered")
        print("4. Reaper 5. Two Kings 6. Animals")
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
        print("1. Classic   2. Nemesis   3. Empowered")
        print("4. Reaper 5. Two Kings 6. Animals")
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

        prototype = []
        prototype.append('[Event "Sample Games"]')
        prototype.append('[Site "' + 'Fantasy Strike Website' '\"]')
        prototype.append('[Date "' + ".".join((time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"))) + '"]')
        prototype.append('[Round "' + '-' + '"]')
        prototype.append('[White "' + chess.army_name_dict[int(wArmy)] + '"]')
        prototype.append('[Black "' + chess.army_name_dict[int(bArmy)] + '"]')

        while True:
            turn = chess.getTurn()
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
                elif move == "set":
                    chess.setFEN(input("Paste FEN: "))
                elif move == "get": # Displaying available moves for a given space.
                    getter = input("> ")
                    print(str(getter))
                    getter = chess.parseTextMove(getter)[3:5]
                    print(chess.getValidMoves(getter))
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
                    # True: a correctly entered move
                    if res is True:
                        result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                        if result:
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
                            result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn)
                            if result:
                                turn = chess.getTurn()
                                chess.updateRoyalLocations()
                            else:
                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                        else:
                            print("{}".format(chess.move_reason_list[chess.getReason()]))
                    # False: The move couldn't be parsed or is ambiguous or wrong
                    elif res is False:
                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                    # Other: TIME TO DU-DU-DU-DUEL
                    else:
                        print("{}, would you like to initiate a duel? It will cost {}.".format(str(chess.value_to_color_dict[not turn]), res))
                        tmp_white = chess._white_stones
                        tmp_black = chess._black_stones
                        duel_cost = None
                        while True:
                            answer = input("> ")
                            if answer == "exit":
                                sys.exit(0)
                            # Duel initiation
                            elif any(var in answer for var in ('y', 'Y', 'Yes', 'yes')):
                                duel_cost = res
                                if turn == chess.WHITE:
                                    tmp_white = tmp_white + res
                                    tmp_att = tmp_white
                                    tmp_def = tmp_black
                                else:
                                    tmp_black = tmp_black + res
                                    tmp_att = tmp_black
                                    tmp_def = tmp_white
                                print("White stones: {}".format(tmp_white))
                                print("Black stones: {}".format(tmp_black))
                                print("{}, how much would you like to bid?".format(str(chess.value_to_color_dict[not turn])))
                                # Defender Bid
                                while True:
                                    defending_bid = getpass.getpass("> ")
                                    if defending_bid == "exit":
                                        sys.exit(0)
                                    elif defending_bid in string.digits:
                                        if int(defending_bid) <= min(2, tmp_def):
                                            if int(defending_bid) > -1:
                                                defending_bid = int(defending_bid)
                                                break
                                            print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_def)))
                                        print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_def)))
                                    else:
                                        print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_def)))
                                print("{}, how much would you like to bid?".format(str(chess.value_to_color_dict[turn])))
                                # Attacker Bid
                                while True:
                                    attacking_bid = getpass.getpass("> ")
                                    if attacking_bid == "exit":
                                        sys.exit(0)
                                    elif attacking_bid in string.digits:
                                        if int(attacking_bid) <= min(2, tmp_att):
                                            if int(attacking_bid) > -1:
                                                attacking_bid = int(attacking_bid)
                                                break
                                            print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_att)))
                                        print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_att)))
                                    else:
                                        print("Please only bid a number of stones between 0 and {}.".format(min(2, tmp_att)))
                                if attacking_bid == 0 and defending_bid == 0:
                                    duel_results = chess.BLUFF
                                elif attacking_bid >= defending_bid:
                                    duel_results = chess.ATT_WIN
                                else:
                                    duel_results = chess.DEF_WIN
                                # duel_results will now be either 0, 1, or 2
                                print("{} bid: {}".format(chess.value_to_color_dict[turn], attacking_bid))
                                print("{} bid: {}".format(chess.value_to_color_dict[not turn], defending_bid))
                                if duel_results == chess.BLUFF:
                                    print("{} called the bluff! Do you want to gain a stone or force {} to lose a stone?".format(
                                        chess.value_to_color_dict[turn], chess.value_to_color_dict[not turn]))
                                    while True:
                                        bluff_choice = input("> ")
                                        if bluff_choice == "exit":
                                            sys.exit(0)
                                        elif any(var in bluff_choice for var in ("g", "gain", "G", "Gain")):
                                            att_result = chess.addTextMove(move, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "g")
                                            if att_result:
                                                turn = chess.getTurn()
                                                chess.updateRoyalLocations()
                                                break
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
                                                att_result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "g")
                                                if att_result:
                                                    turn = chess.getTurn()
                                                    chess.updateRoyalLocations()
                                                else:
                                                    print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                    break
                                            else:
                                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                break
                                        elif any(var in bluff_choice for var in ("l", "lose", "L", "Lose")):
                                            att_result = chess.addTextMove(move, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "l")
                                            if att_result:
                                                turn = chess.getTurn()
                                                chess.updateRoyalLocations()
                                                break
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
                                                att_result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "l")
                                                if att_result:
                                                    turn = chess.getTurn()
                                                    chess.updateRoyalLocations()
                                                else:
                                                    print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                    break
                                            else:
                                                print("{}".format(chess.move_reason_list[chess.getReason()]))
                                                break
                                        else:
                                            print('Please choose between gaining a stone and forcing a lose of a stone.')
                                elif duel_results == chess.ATT_WIN:
                                    print("Attacker wins!")
                                    att_result = chess.addTextMove(move, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "n")
                                    if att_result:
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
                                        att_result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "n")
                                        if att_result:
                                            turn = chess.getTurn()
                                            chess.updateRoyalLocations()
                                        else:
                                            print("{}".format(chess.move_reason_list[chess.getReason()]))
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                else:
                                    print("Defender wins!")
                                    att_result = chess.addTextMove(move, secondTurn=chess._secondTurn, clearLocation=True, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "n")
                                    if att_result:
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
                                        att_result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn, duel=str(duel_cost) + str(attacking_bid) + str(defending_bid) + "n")
                                        if att_result:
                                            turn = chess.getTurn()
                                            chess.updateRoyalLocations()
                                        else:
                                            print("{}".format(chess.move_reason_list[chess.getReason()]))
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                turn = chess.getTurn()
                                break
                            # Non-Duel initiation
                            elif any(var in answer for var in ('n', 'N', 'No', 'no')):
                                result = chess.addTextMove(move, secondTurn=chess._secondTurn)
                                if result:
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
                                    result = chess.addTextMove(move+promo, secondTurn=chess._secondTurn)
                                    if result:
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print("{}".format(chess.move_reason_list[chess.getReason()]))
                                else:
                                    print("{}".format(chess.move_reason_list[chess.getReason()]))
                                break
                            else:
                                print('Please enter \'yes\' or \'no\'.')
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

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
