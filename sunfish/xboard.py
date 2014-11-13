#!/usr/bin/env pypy -u
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import re
import sys
import sunfish

# Python 2 compatability
if sys.version_info[0] == 2:
    input = raw_input

# Sunfish doesn't know about colors. We have to.
WHITE, BLACK = range(2)
FEN_INITIAL = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 Cc 33 '

army_abr_dict = {
    1: 'C', 'C': 1,
    2: 'N', 'N': 2,
    3: 'E', 'E': 3,
    4: 'R', 'R': 4,
    5: 'T', 'T': 5,
    6: 'A', 'A': 6}

classic_piece_to_army_piece_dict = {
    #      c    n    e    r    t    a
    'P': ['P', 'L', 'P', 'P', 'P', 'P'],
    'B': ['B', 'B', 'X', 'B', 'B', 'T'],
    'N': ['N', 'N', 'Y', 'N', 'N', 'H'],
    'R': ['R', 'R', 'Z', 'G', 'R', 'E'],
    'Q': ['Q', 'M', 'O', 'A', 'U', 'J'],
    'K': ['K', 'C', 'C', 'C', 'W', 'C']}

army_piece_to_classic_piece_dict = {
    'P': 'P', 'B': 'B', 'N': 'N', 'R': 'R', 'Q': 'Q', 'K': 'K',
    'L': 'P', 'M': 'Q',
    'X': 'B', 'Y': 'N', 'Z': 'R', 'O': 'Q',
    'G': 'R', 'A': 'Q',
    'U': 'Q', 'W': 'K',
    'T': 'B', 'H': 'N', 'E': 'R', 'J': 'Q',
    'C': 'K', '/': '/'}

def parseFEN(fen):
    """ Parses a string in Forsyth-Edwards Notation into a Position """
    armies, stones, board, color, castling, enpas, hclock, fclock = fen.split()
    wa, ba = int(army_abr_dict[armies[0]]), int(army_abr_dict[armies[1].upper()])
    ws, bs = int(stones[0]), int(stones[1])
    board = re.sub('\d', (lambda m: '.'*int(m.group(0))), board)
    board = list(' '*9+'\n'+' '*9+'\n ' + '\n '.join(board.split('/')) + '\n'+' '*9+'\n'+' '*10)
    change = lambda p, a: classic_piece_to_army_piece_dict[p][a - 1]
    for num, char in enumerate(board):
        if char == '.': continue
        if char.isspace(): continue
        if char.isupper():
            board[num] = change(char, wa)
        else:
            board[num] = change(char.upper(), ba).lower()
    board = "".join(board)
    color = 0 if color == 'w' else 1
    if color == 1:
        board = board[::-1].swapcase()
    wc = ('Q' in castling, 'K' in castling)
    bc = ('k' in castling, 'q' in castling)
    ep = sunfish.parse(enpas) if enpas != '-' else 0
    score = sum(sunfish.pst[p][i] for i,p in enumerate(board) if p.isupper() and p != 'U')
    score -= sum(sunfish.pst[p.upper()][i] for i,p in enumerate(board) if p.islower() and p != 'u')
    pos = sunfish.Position(board, color, False, score, wa, ba, ws, bs, wc, bc, ep, 0)
    return pos

def printFEN(pos):
    """ Prints a Chess2 FEN """
    board, color, second, score, wa, ba, ws, bs, wc, bc, ep, fifty = pos
    if color:
        board = board[::-1].swapcase()
        wa, ba, ws, bs = ba, wa, bs, ws
    else:
        ep = 119 if ep == 0 else ep
        wc, bc, ep = bc, wc, 119-ep
    board = "".join(board.split())
    board = [formatPieceNames(var) for var in board]
    rows = []
    for i in range(8):
        row = board[i * 8:(i + 1) * 8]
        cnt = 0
        res = ""
        for c in row:
            if c == ".":
                cnt += 1
            else:
                if cnt:
                    res += str(cnt)
                    cnt = 0
                res += c
        if cnt:
            res += str(cnt)
        rows.append(res)
    board = "/".join(rows)

    turn = (["w", "b"])[color]

    armystones = "{}{} {}{}".format(army_abr_dict[wa], army_abr_dict[ba].lower(), int(ws), int(bs))

    kq = ""
    if wa == WHITE and wc[1] is True:
            kq += "K"
    elif wa == WHITE and wc[0] is True:
            kq += "Q"
    if ba == WHITE and bc[1] is True:
            kq += "k"
    elif ba == WHITE and bc[0] is True:
            kq += "q"
    if not kq:
        kq = "-"

    if ep != 0:
        rank, fil = divmod(ep - 91, 10)
        ep = chr(fil + ord('a')) + str(-rank + 1)
    else: ep = "-"

    return "{} {} {} {} {} {} {}".format(armystones, board, turn, kq, ep, fifty, 0)

def formatPieceNames(piece):
    if piece != ".":
        if all(word.isupper() for word in piece):
            piece = army_piece_to_classic_piece_dict[piece]
        else:
            piece = army_piece_to_classic_piece_dict[piece.upper()]
            piece = piece.lower()
    return piece

def mrender(pos, m):
    # Sunfish always assumes promotion to queen
    p = 'q' if sunfish.A8 <= m[1] <= sunfish.H8 and pos.board[m[0]] == 'P' else ''
    if pos.color == 0: m = (119-m[0], 119-m[1])
    return sunfish.render(m[0]) + sunfish.render(m[1]) + p

def mparse(color, move):
    m = (sunfish.parse(move[0:2]), sunfish.parse(move[2:4]))
    return m if color == WHITE else (119-m[0], 119-m[1])

def pv(color, pos):
    res = []
    origc = color
    res.append(str(pos.score))
    while True:
        entry = sunfish.tp.get(pos)
        if entry is None:
            break
        if entry.move is None:
            res.append('null')
            break
        move = mrender(color,pos,entry.move)
        if move in res:
            res.append(move)
            res.append('loop')
            break
        res.append(move)
        pos, color = pos.move(entry.move), 1-color
        res.append(str(pos.score if color==origc else -pos.score))
    return ' '.join(res)

def main():
    pos = parseFEN(FEN_INITIAL)
    forced = False
    color = WHITE
    time, otim = 1, 1

    stack = []
    while True:
        if stack:
            smove = stack.pop()
        else: smove = input()

        if smove == 'quit':
            break

        elif smove == 'protover 2':
            print('feature done=0')
            print('feature myname="Sunfish"')
            print('feature usermove=1')
            print('feature setboard=1')
            print('feature ping=1')
            print('feature sigint=0')
            print('feature variants="normal"')
            print('feature done=1')

        elif smove == 'new':
            stack.append('setboard ' + FEN_INITIAL)

        elif smove.startswith('setboard'):
            _, fen = smove.split(' ', 1)
            pos = parseFEN(fen)
            color = WHITE if fen.split()[1] == 'w' else BLACK

        elif smove == 'force':
            forced = True

        elif smove == 'go':
            forced = False

            # Let's follow the clock of our opponent
            nodes = 2e4
            if time > 0 and otim > 0: nodes *= time/otim
            m, s = sunfish.search(pos, maxn=nodes)
            # We don't play well once we have detected our death
            if s <= -sunfish.MATE_VALUE:
                print('resign')
            else:
                print('# %d %+d %d %d %s' % (0, s, 0, sunfish.nodes, pv(color,pos)))
                print('move', mrender(color, pos, m))
                print('score before %d after %+d' % (pos.score, pos.value(m)))
                pos = pos.move(m)
                color = 1-color

        elif smove.startswith('ping'):
            _, N = smove.split()
            print('pong', N)

        elif smove.startswith('usermove'):
            _, smove = smove.split()
            m = mparse(color, smove)
            pos = pos.move(m)
            color = 1-color
            if not forced:
                stack.append('go')

        elif smove.startswith('time'):
            time = int(smove.split()[1])

        elif smove.startswith('otim'):
            otim = int(smove.split()[1])

        elif any(smove.startswith(x) for x in ('xboard','post','random','hard','accepted','level')):
            pass

        else:
            print("Error (unkown command):", smove)

if __name__ == '__main__':
    main()
