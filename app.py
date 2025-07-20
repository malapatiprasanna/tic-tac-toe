from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Minimax logic
def check_winner(board, player):
    win_cond = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
    return any(board[i] == board[j] == board[k] == player for i,j,k in win_cond)

def is_draw(board):
    return ' ' not in board

def minimax(board, is_max):
    if check_winner(board, 'O'): return 1
    if check_winner(board, 'X'): return -1
    if is_draw(board): return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, False)
                board[i] = ' '
                best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ' '
                best = min(score, best)
        return best

def best_move(board):
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    move_index = best_move(board)
    if move_index != -1:
        board[move_index] = 'O'
    status = "continue"
    if check_winner(board, 'O'):
        status = "ai_win"
    elif check_winner(board, 'X'):
        status = "player_win"
    elif is_draw(board):
        status = "draw"
    return jsonify({"board": board, "status": status})

if __name__ == '__main__':
    app.run(debug=True)
