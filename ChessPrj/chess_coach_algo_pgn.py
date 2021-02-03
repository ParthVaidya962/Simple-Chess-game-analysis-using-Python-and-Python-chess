import sys
import chess.engine
import chess.pgn


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
    curr_an_score = curr_analyse.score.pov(chess.WHITE)
    curr_val = str(curr_an_score)
    if not curr_an_score.is_mate():
        curr_int = int(curr_val)
        curr_score = curr_int / 100
    else:
        result = ""
        temp = board.pop()
        prev_analyse2 = engine.analyse(board, chess.engine.Limit(depth=20))
        best_move2 = prev_analyse2['pv'][0]
        board.push(temp)
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
        if not prev_analyse2.score.is_mate():
            best_string = str(int(str(prev_analyse2.score.pov(chess.WHITE))) / 100)
        else:
            best_string = str(prev_analyse2.score.pov(chess.WHITE))
        final_result = result + " (" + curr_val + ")" + " (The Best Move was " + str(
            best_move2) + ", " + best_string + ")."
        return final_result

    # print("debug: curr_score:"+str(curr_score))

    temp = board.pop()
    prev_analyse = engine.analyse(board, chess.engine.Limit(depth=20))
    good_moves = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    prev_an_score = prev_analyse.score.pov(chess.WHITE)
    prev_val = str(prev_an_score)
    board.push(temp)

    if not prev_an_score.is_mate():
        prev_int = int(prev_val)
        prev_score = prev_int / 100
    else:
        chars = []
        for i, char in enumerate(prev_val):
            chars.append(char)
        result = ""
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
        if not prev_analyse.score.is_mate():
            best_string = str(int(str(prev_analyse.score)) / 100)
        else:
            best_string = str(prev_analyse.score)
        try:
            best_move = str(prev_analyse.pv[0])
        except IndexError:
            best_move = None
        final_result = result + " (" + curr_val + ")" + " (The Best Move was " + str(
            best_move) + ", " + best_string + ")."
        return final_result

    # print("debug: prev_score:"+str(prev_score))
    # good_moves = engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)
    # print("debug: "+str(prev_analyse[0].pv))
    best_score = ""
    try:
        best_move = good_moves[0]['pv'][0]
        if not good_moves[0].score.is_mate():
            best_score = str(int(str(good_moves[0].score.pov(chess.WHITE)))/100)
        else:
            best_score = str(good_moves[0].score.pov(chess.WHITE))
    except IndexError:
        best_move = None
    try:
        very_good_move = good_moves[1]['pv'][0]
    except IndexError:
        very_good_move = None
    try:
        good_move = good_moves[2]['pv'][0]
    except IndexError:
        good_move = None
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
    result += " (" + str(curr_score) + ")"
    final_result = result + " (The Best Move was " + str(best_move) + ", " + best_score + " )"
    engine.close()
    return final_result


def clear():
    os.system('cls')


def main():
    with open("pgn_file.pgn") as pgn:
        game = chess.pgn.read_game(pgn)
    game_analysed = chess.pgn.Game()
    board = game.board()
    flag = 1
    node = ""
    for move in game.mainline_moves():
        if flag == 1:
            board.push(move)
            print(move)
            node = game_analysed.add_variation(move=move, comment=coach_opinion(board, move))
            print(node)
            flag = 0
            continue
        board.push(move)
        print(move)
        node = node.add_variation(move=move, comment=coach_opinion(board, move))
        print(node)
    with open("pgn_file_analysed.pgn", "w+") as file_write:
        if not file_write.closed:
            print("alpha")
            print(game_analysed, file=file_write, end="\n\n")
            sys.exit()
        else:
            print("gamma")
            file_write.close()
            print("delta")
        file_write.close()
        exit()


if __name__ == '__main__':
    main()
    exit()
