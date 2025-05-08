# Tetris.py
# Simple terminal-based Tetris implementation in Python
import random
import os
import sys
import time

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]

WIDTH, HEIGHT = 10, 20

class Tetris:
    def __init__(self):
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.score = 0
        self.gameover = False
        self.new_piece()

    def new_piece(self):
        self.shape = random.choice(SHAPES)
        self.x = WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        if self.collision():
            self.gameover = True

    def collision(self, dx=0, dy=0, shape=None):
        shape = shape or self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
                        return True
                    if self.board[ny][nx]:
                        return True
        return False

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        if not self.collision(shape=rotated):
            self.shape = rotated

    def move(self, dx):
        if not self.collision(dx=dx):
            self.x += dx

    def drop(self):
        if not self.collision(dy=1):
            self.y += 1
        else:
            for y, row in enumerate(self.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.board[self.y + y][self.x + x] = 1
            self.clear_lines()
            self.new_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = HEIGHT - len(new_board)
        self.score += lines_cleared
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * WIDTH)
        self.board = new_board

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        temp_board = [row[:] for row in self.board]
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and 0 <= self.y + y < HEIGHT and 0 <= self.x + x < WIDTH:
                    temp_board[self.y + y][self.x + x] = 2
        print('Score:', self.score)
        for row in temp_board:
            print(''.join(['#' if cell else '.' for cell in row]))
        print('\nControls: a=left, d=right, w=rotate, s=down, q=quit')

    def run(self):
        import threading
        input_char = {'c': None}
        def get_input():
            while not self.gameover:
                input_char['c'] = sys.stdin.read(1)
        threading.Thread(target=get_input, daemon=True).start()
        while not self.gameover:
            self.print_board()
            c = input_char['c']
            input_char['c'] = None
            if c == 'a':
                self.move(-1)
            elif c == 'd':
                self.move(1)
            elif c == 'w':
                self.rotate()
            elif c == 's':
                self.drop()
            elif c == 'q':
                break
            else:
                self.drop()
            time.sleep(0.3)
        print('Game Over! Final Score:', self.score)

if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()
