import chess.engine

board = chess.Board()
board.push_san("e4")
print(chess.engine)
engine = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe", debug=True)
print(engine.analyse(board, chess.engine.Limit(depth=20)))
for i in engine.analyse(board, chess.engine.Limit(depth=20), multipv=3):
    print(i)
    print(i.score)
    print(i.score.pov(chess.WHITE))
