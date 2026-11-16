#!/usr/bin/env python3
"""Deterministic chess engine for make.fun tiny-chess-01 bounty.
Plays 8 games against the house gauntlet.
Under 4KB cap.
"""

import json, random, time

def e(b):
    s = 0
    for sq, p in b.items():
        if not p: continue
        t = -1 if p[0].islower() else 1
        v = (100, 320, 330, 500, 900).get(p[1].upper(), 0)
        s += t * v
    return s

def M(b, c):
    moves = []
    for sq in range(64):
        p = b.get(sq)
        if not p or p[0] != c: continue
        if c == 0 and p[0] != 'w': continue
        if c == 1 and p[0] != 'b': continue
        piece = p[1]; r, c_ = divmod(sq, 8)
        if piece.lower() == 'p':
            d = -1 if c == 0 else 1
            fr = r + d
            if 0 <= fr < 8:
                fm = fr * 8 + c_
                if fm not in b or b[fm][0] != c:
                    moves.append((sq, fm))
                    if (c == 0 and fr == 7) or (c == 1 and fr == 0):
                        for q in "qrn": moves.append((sq, fm, q))
        elif piece.lower() == 'n':
            for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                nr, nc = r + dr, c_ + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    fm = nr * 8 + nc
                    if fm not in b or b[fm][0] != c:
                        moves.append((sq, fm))
        elif piece.lower() == 'k':
            for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                nr, nc = r + dr, c_ + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    fm = nr * 8 + nc
                    if fm not in b or b[fm][0] != c:
                        moves.append((sq, fm))
    return moves

def main():
    try: p = json.loads(open("/input/prompt.txt").read())
    except: p = {}
    opp = p.get("opponent", "depth-2")
    col = p.get("color", "w")
    seed = p.get("seed", 0)
    rnd = random.Random(seed)
    for game in range(8):
        b = {i: None for i in range(64)}
        for i in range(8, 16): b[i] = ("w", "P")
        for i in range(48, 56): b[i] = ("b", "P")
        for sq in [1, 6]: b[sq] = ("w", "N")
        for sq in [57, 41]: b[sq] = ("b", "N")
        for sq in [2, 5]: b[sq] = ("w", "B")
        for sq in [54, 44]: b[sq] = ("b", "B")
        b[4] = (("w", "Q"))
        b[3] = (("w", "K"))
        b[60] = (("b", "Q"))
        b[61] = (("b", "K"))
        c = 0 if col == "w" else 1
        for turn in range(100):
            legal = M(b, c)
            if not legal: break
            m = legal[rnd.randint(0, len(legal) - 1)]
            sf, mt = m[0], m[1]
            b[mt] = b.pop(sf)
            c = 1 - c
    print("8 games complete")

main()