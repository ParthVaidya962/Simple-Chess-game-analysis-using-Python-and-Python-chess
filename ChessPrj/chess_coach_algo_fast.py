from typing import Optional
import os
import chess.engine
import logging
from chess.engine import PovScore


def coach_opinion(board, curr_move):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")
    curr_analyse = engine.analyse(board, chess.engine.Limit(depth=20))
    curr_score = int(str(curr_analyse.score)) / 100
    board.pop()
    prev_analyse = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    prev_score = int(str(prev_analyse[0].score)) / 100
    best_move = prev_analyse[0]['pv'][0]
    very_good_move = prev_analyse[1]['pv'][0]
    good_move = prev_analyse[2]['pv'][0]
    result = ""
    final_result = ""
    if str(curr_move) == str(best_move):
        result = "Best Move!"
    elif str(curr_move) == str(very_good_move):
        result = "Very Good Move!"
    elif str(curr_move) == str(good_move):
        result = "Good Move!"
    else:
        if board.turn:
            if prev_score >= 0:
                if 0 < curr_score < prev_score:
                    result = "Bad Move!"
                elif curr_score == 0:
                    result = "Very Bad Move!"
                else:
                    result = "Losing Move!"
            elif curr_score - prev_score >= -1.00:
                result = "Bad Move!"
            elif curr_score - prev_score >= -3.00:
                result = "Very Bad Move!"
            else:
                result = "Losing Move!"
        else:
            if prev_score < 0:
                if 0 > curr_score > prev_score:
                    result = "Bad Move!"
                elif curr_score == 0:
                    result = "Very Bad Move!"
                else:
                    result = "Losing Move!"
            elif curr_score - prev_score <= 1.00:
                result = "Bad Move!"
            elif curr_score - prev_score <= 3.00:
                result = "Very Bad Move!"
            else:
                result = "Losing Move!"
    result += "(" + str(curr_score) + ")"
    final_result = result + " (The Best Move was " + str(best_move) + ", " + str(
        int(str(prev_analyse[0]['score'])) / 100) + " )"
    engine.close()
    board.push_uci(curr_move)
    return final_result


def clear():
    os.system('cls')


def main():
    board = chess.Board()
    i = 1
    j = 0
    mov = ""
    side = ""
    while not board.is_game_over():
        if j == 2:
            j = 0
            i = i + 1
        if board.turn:
            side = "(WHITE)"
        else:
            side = "(BLACK)"
        mov = input("Move " + str(i) + side + " : ")
        if mov == "end":
            exit()
        j = j + 1
        board.push_uci(mov)
        print("Analysis in progress...")
        print(coach_opinion(board, str(mov)))
    exit()


if __name__ == '__main__':
    main()
