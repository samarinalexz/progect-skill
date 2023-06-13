board = [0, 1, 2,
         3, 4, 5,
         6, 7, 8]
victory = [[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8],
           [0, 3, 6],
           [1, 4, 7],
           [2, 5, 8],
           [0, 4, 8],
           [2, 4, 6]]


def disp_board():
    print(f'|{board[0]}', end='')
    print(f'|{board[1]}', end='')
    print(f'|{board[2]}|', end='\n')
    print(f'|{board[3]}', end='')
    print(f'|{board[4]}', end='')
    print(f'|{board[5]}|', end='\n')
    print(f'|{board[6]}', end='')
    print(f'|{board[7]}', end='')
    print(f'|{board[8]}|')


def step_on_board(step, symbol):
    index = board.index(step)
    board[index] = symbol


def result():
    win = ''
    for i in victory:
        if board[i[0]] == 'X' and board[i[1]] == 'X' and board[i[2]] == 'X':
            win = 'Победитель X'
        if board[i[0]] == 'O' and board[i[1]] == 'O' and board[i[2]] == 'O':
            win = 'Победитель O'
    return win


game = True
players = True
cont = 1
while game:
    print(f'Ход номер: {cont}')
    cont += 1
    disp_board()
    if players:
        symbol = 'X'
        step = int(input('Крестик, ваш ход: '))
    else:
        symbol = 'O'
        step = int(input('Нолик, ваш ход: '))
    step_on_board(step, symbol)
    win = result()
    if win != '':
        game = False
    elif cont == 10:
        game = False
        win = 'Ничья'
    else:
        game = True
    players = not players

disp_board()
print(f'результат: {win}')

