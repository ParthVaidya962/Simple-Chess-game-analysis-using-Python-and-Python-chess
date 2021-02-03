from typing import Optional
import os
import chess.engine
# import logging
# from chess.engine import PovScore


def coach_opinion(board, curr_move):
    if board.is_game_over():
        res = str(board.result())
        if res == "1-0":
            return "White is Victorious! " + "(" + str(board.result()) + ")"
        elif res == "0-1":
            return "Black is Victorious!" + "(" + str(board.result()) + ")"
        else:
            return "The game has resulted in a Draw." + "(" + str(board.result()) + ")"
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")
    curr_analyse = engine.analyse(board, chess.engine.Limit(depth=20))
    curr_an_score = chess.engine.PovScore(curr_analyse.score, board.turn)
    curr_val = str(curr_an_score.relative)
    if not curr_an_score.is_mate():
        curr_int = int(curr_val)
        curr_score = curr_int / 100;
    else:
        board.pop()
        prev_analyse2 = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
        best_move2 = prev_analyse2[0]['pv'][0]
        board.push_san(str(curr_move))
        chars = []
        for i, char in enumerate(curr_val):
            chars.append(char)

        if chars[1] == '+':
            if not board.turn:
                result = "You can deliver Checkmate in " + chars[2] + " Moves!"
            else:
                result = "Opponent can force Checkmate in " + chars[2] + " moves!"
        elif chars[1] == '-':
            if board.turn:
                result = "Opponent can force Checkmate in " + chars[2] + " moves!"
            else:
                result = "You can deliver Checkmate in " + chars[2] + " Moves!"
        if not prev_analyse2[0].score.is_mate():
            best_string = str(int(str(prev_analyse2[0].score)) / 100)
        else:
            best_string = str(prev_analyse2[0].score)
        final_result = result + "(" + curr_val + ")" + " (The Best Move was " + str(
            best_move2) + ", " + best_string + ")."
        return final_result

    # print("debug: curr_score:"+str(curr_score))
    board.pop()
    prev_analyse = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    prev_an_score = chess.engine.PovScore(prev_analyse[0].score, board.turn)
    prev_val = str(prev_an_score.relative)
    board.push_san(str(curr_move))
    if not prev_an_score.is_mate():
        prev_int = int(prev_val)
        prev_score = prev_int / 100;
    else:
        chars = []
        for i, char in enumerate(prev_val):
            chars.append(char)

        if chars[1] == '+':
            if not board.turn:
                result = "You can deliver Checkmate in " + chars[2] + " Moves!"
            else:
                result = "Opponent can force Checkmate in " + chars[2] + " moves!"
        elif chars[1] == '-':
            if board.turn:
                result = "Opponent can force Checkmate in " + chars[2] + " moves!"
            else:
                result = "You can deliver Checkmate in " + chars[2] + " Moves!"
        if not prev_analyse[0].score.is_mate():
            best_string = str(int(str(prev_analyse[0].score)) / 100)
        else:
            best_string = str(prev_analyse[0].score)
        try:
            best_move = str(prev_analyse[0].pv[0])
        except IndexError:
            best_move = None
        final_result = result + "(" + curr_val + ")" + " (The Best Move was " + str(
            best_move) + ", " + best_string + ")."
        return final_result

    # print("debug: prev_score:"+str(prev_score))
    # good_moves = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    # print("debug: "+str(prev_analyse[0].pv))
    try:
        best_move = prev_analyse[0]['pv'][0]
        very_good_move = prev_analyse[1]['pv'][0]
        good_move = prev_analyse[2]['pv'][0]
    except IndexError:
        best_move = None
        very_good_move = None
        good_move = None
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
        board.push_san(mov)
        print(board)
        if not board.is_game_over():
            print("Analysis in progress... please wait...")

        print(coach_opinion(board, str(mov)))

    exit()


if __name__ == '__main__':
    main()
