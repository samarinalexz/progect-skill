from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вне игрового поля'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Этот вариант хода уже был сделан'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y}'


class Ship:
    def __init__(self, nose, size, rotation):
        self.nose = nose
        self.size = size
        self.rotation = rotation
        self.health = size

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.size):
            length_x = self.nose.x
            length_y = self.nose.y

            if self.rotation == 0:
                length_x += i
            elif self.rotation == 1:
                length_y += i
            ship_dots.append(Dot(length_x, length_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, board_matrix=10):
        self.board_matrix = board_matrix
        self.hid = hid

        self.count = 0
        self.field = [['0'] * board_matrix for _ in range(board_matrix)]

        self.busy = []
        self.ships = []

    def __str__(self):
        result = ''
        result += "  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |" #Хотел реализовать доску 10 на 10
        for i, row in enumerate(self.field):                   #но столкнулся с проблемой искривления игрового поля
            result += f"\n{i} | " + " | ".join(row) + " |" #никак не смог выправить игровую доску, если номер координаты оси двузначный, если подскажете, буду благодарен

        if self.hid:
            result = result.replace("■", '0')
        return result

    def out(self, point):
        return not ((0 <= point.x < self.board_matrix) and (0 <= point.y < self.board_matrix))

    def contour(self, ship, verb=False):
        nearby = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for point in ship.dots:
            for point_x, point_y in nearby:
                cur = Dot(point.x + point_x, point.y + point_y)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for point in ship.dots:
            if self.out(point) or point in self.busy:
                raise BoardWrongShipException()
        for point in ship.dots:
            self.field[point.x][point.y] = '■'
            self.busy.append(point)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, point):
        if self.out(point):
            raise BoardOutException()

        if point in self.busy:
            raise BoardUsedException()

        self.busy.append(point)

        for ship in self.ships:
            if point in ship.dots:
                ship.health -= 1
                self.field[point.x][point.y] = 'X'
                if ship.health == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль убит!')
                    return False
                else:
                    print('Есть попадание!')
                    return True

        self.field[point.x][point.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        point = Dot(randint(0, 9), randint(0, 9))
        print(f'Ход компьютера: {point.x}{point.y}')
        return point


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите координаты выстрела: ').split()

            if len(cords) != 2:
                print('Нужны две координаты! ')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа! ')
                continue

            x, y = int(x), int(y)

            return Dot(x, y)


class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(board_matrix=self.size)
        attempts = 0
        for L in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), L, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print('____________________')
        print('  Добро пожаловать  ')
        print('      в игру        ')
        print('    морской бой     ')
        print('____________________')
        print(' формат ввода: x y  ')
        print('  x - номер строки  ')
        print('  y - номер столбца ')

    def loop(self):
        num = 0
        while True:
            print('_' * 20)
            print('Доска игрока: ')
            print(self.us.board)
            print('_' * 20)
            print('Доска компьютера: ')
            print(self.ai.board)
            print('_' * 20)
            if num % 2 == 0:
                print('Ваш ход!: ')
                repeat = self.us.move()
            else:
                print('Ход компьютера!: ')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 10:
                print('_' * 20)
                print('Вы победили!')
                break

            if self.us.board.count == 10:
                print('_' * 20)
                print('Компьютер победили!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
