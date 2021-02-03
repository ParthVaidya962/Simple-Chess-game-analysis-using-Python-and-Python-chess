from chess import Move
from typing import Any, Union
import os

import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")


# board.push_uci("g1f3")
# print(board)
def goodmoves(fen):
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    best_move = info[0]['pv'][0]
    very_good_move = info[1]['pv'][0]
    good_move = info[2]['pv'][0]
    print("The Best Possible move for the player is : " + str(best_move))# + ", which will result in a score of :" + str(
        #int(str(info[0]['score'])) / 100) + " from white's POV.")
    print("A Very Good move for the player is : " + str(very_good_move))# + ", which will result in a score of :" + str(
        #int(str(info[1]['score'])) / 100) + " from white's POV.")
    print("A Good move for the player is : " + str(good_move))#+ ", which will result in a score of :" + str(
        #int(str(info[2]['score'])) / 100) + " from white's POV.")


def main():
    while True:
        fen = input("Please enter the fen string : ")
        goodmoves(fen)
        st = input("OK?")
        clear = lambda:os.system('cls')
        clear()


if __name__ == '__main__':
    main()
# good_moves=[]
# for i in info:
# print(i['score'])
# print(i['pv'])
#    good_moves.append(i['pv'][0])
# for i in good_moves:
#    print(i)
# print(info)
