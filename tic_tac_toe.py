from fastapi import FastAPI, Query, Path
from uvicorn import run
import numpy as np
from random import choice

table = np.full((3, 3), '☺').reshape((1, 9))
table_one_player = np.full((3, 3), '☺').reshape((1, 9))


app = FastAPI()

winning_combs = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7},
                 {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 8}]

x_moves = set()
y_moves = set()

x_moves_one_player = set()
computer_moves = set()
computer_possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

x_wins = 0
y_wins = 0

x_wins_one_player = 0
computer_wins = 0

winner = ''
winner_one_player = '.'

x_turn = True
add_win = True
add_win_one_player = True

table_string = ''
for i in table:
    for j in i:
        table_string += j+' '
    table_string += '\n'


@app.get("/")
async def root():
    return {"message": table_string}


@app.get("/hello/{name}")
async def say_hello(name: str):

    return {"message": f"Hello {name}"}


@app.get('/tic-tac-toe')
def tic_tac_toe(player: int = Query(ge=1, le=2), num: int = Query(ge=1, le=9)):

    global table
    global table_string
    global x_turn
    global x_wins
    global y_wins
    global winner
    global add_win

    player_winning_moves = set()

    if player == 1:
        if table[0][num-1] != 'Y' and x_turn:
            table[0][num-1] = 'X'
            x_moves.add(num)
            x_turn = False
    elif player == 2:
        if table[0][num - 1] != 'X' and not x_turn:
            table[0][num-1] = 'Y'
            y_moves.add(num)
            x_turn = True

    table_string = ''

    for i in table:
        for j in i:
            table_string += j + ' '
        table_string += '\n'

    for i in winning_combs:
        if i.issubset(x_moves):
            winner = 'X'
            player_winning_moves = i
            if add_win:
                x_wins += 1
                add_win = False
        elif i.issubset(y_moves):
            winner = 'Y'
            player_winning_moves = i
            if add_win:
                y_wins += 1
                add_win = False
    result = {'winner': winner, 'winning moves': player_winning_moves,
              'x wins': x_wins, 'y wins': y_wins}

    if winner == '':
        if len(x_moves) + len(y_moves) < 9:
            return {'player': player, 'move': num, 'table': table_string, 'x': x_moves, 'y': y_moves}
        else:
            return {'result': 'draw', 'x wins': x_wins, 'y wins': y_wins}
    else:
        return result


@app.get('/tic-tac-toe/two-player/play-again')
def play_again():
    global table
    global winner
    global table_string
    global x_turn
    global x_moves
    global y_moves
    global add_win

    x_turn = True
    add_win = True
    winner = ''
    x_moves = set()
    y_moves = set()
    table_string = ''
    table = np.full((3, 3), '☺').reshape((1, 9))

    return 'You can play again'


@app.get('/tic-tac-toe/one-player/{num}')
def one_player(num: int = Path(ge=1, le=9)):
    global table_one_player
    global table_string
    global x_wins_one_player
    global winner_one_player
    global computer_moves
    global x_moves_one_player
    global computer_possible_moves
    global computer_wins
    global add_win_one_player

    if table_one_player[0][num - 1] != 'Y':
        table_one_player[0][num - 1] = 'X'
        if int(num) in computer_possible_moves:
            computer_possible_moves.remove(int(num))
        x_moves_one_player.add(num)
    if computer_possible_moves != [] and len(x_moves_one_player) > len(computer_moves):
        rand = choice(computer_possible_moves)-1
        table_one_player[0][rand] = 'Y'
        computer_possible_moves.remove(rand+1)
        computer_moves.add(rand+1)

    table_string = ''

    for i in table_one_player:
        for j in i:
            table_string += j + ' '
        table_string += '\n'

    for i in winning_combs:
        if i.issubset(x_moves_one_player):
            winner_one_player = 'X'
            if add_win_one_player:
                x_wins_one_player += 1
                add_win_one_player = False
        elif i.issubset(computer_moves):
            winner_one_player = 'computer'
            if add_win_one_player:
                computer_wins += 1
                add_win_one_player = False
    result = {'winner': winner_one_player, 'x wins': x_wins_one_player, 'computer wins': computer_wins}

    if winner_one_player == '.':
        if len(x_moves_one_player) + len(computer_moves) < 9:
            return {'table': table_string, 'x': x_moves_one_player, 'computer moves':
                    computer_moves, 'possible': computer_possible_moves}
        else:
            return {'result': 'draw', 'x wins': x_wins_one_player, 'computer wins': computer_wins}
    else:
        return result

comb = set()

@app.get('/tic-tac-toe/hard/{num}')
def hard(num: int = Path(ge=1, le=9)):

    global table_one_player
    global table_string
    global x_wins_one_player
    global winner_one_player
    global computer_moves
    global x_moves_one_player
    global computer_possible_moves
    global computer_wins
    global add_win_one_player
    global comb

    if table_one_player[0][num - 1] != 'Y':
        table_one_player[0][num - 1] = 'X'
        if int(num) in computer_possible_moves:
            computer_possible_moves.remove(int(num))
        x_moves_one_player.add(num)

        for i in winning_combs:
            if num in i:
                i.remove(int(num))
                for j in i:
                    comb.add(j)


    if computer_possible_moves != [] and len(x_moves_one_player) > len(computer_moves):
        rand = choice(list(comb))
        table_one_player[0][rand-1] = 'Y'
        computer_possible_moves.remove(rand)
        comb.remove(rand)
        computer_moves.add(rand)

    table_string = ''

    for i in table_one_player:
        for j in i:
            table_string += j + ' '
        table_string += '\n'

    for i in winning_combs:
        if i.issubset(x_moves_one_player):
            winner_one_player = 'X'
            if add_win_one_player:
                x_wins_one_player += 1
                add_win_one_player = False
        elif i.issubset(computer_moves):
            winner_one_player = 'computer'
            if add_win_one_player:
                computer_wins += 1
                add_win_one_player = False
    result = {'winner': winner_one_player, 'x wins': x_wins_one_player, 'computer wins': computer_wins,
              'computer moves': computer_moves, 'x moves': x_moves_one_player, 'comb': comb}

    if winner_one_player == '.':
        if len(x_moves_one_player) + len(computer_moves) < 9:
            return {'table': table_string, 'x': x_moves_one_player, 'computer moves':
                    computer_moves, 'possible': computer_possible_moves, 'comb': comb}
        else:
            return {'result': 'draw', 'x wins': x_wins_one_player, 'computer wins': computer_wins}
    else:
        return result


@app.get('/tic-tac-toe/play-again/one-player')
def play_again_one_player():
    global table_one_player
    global winner_one_player
    global table_string
    global computer_moves
    global computer_possible_moves
    global x_moves_one_player
    global add_win_one_player
    global comb

    winner_one_player = '.'
    x_moves_one_player = set()
    computer_moves = set()
    computer_possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    table_string = ''
    table_one_player = np.full((3, 3), '☺').reshape((1, 9))
    add_win_one_player = True


    return 'You can play again'


if __name__ == "__main__":
    run(app)

