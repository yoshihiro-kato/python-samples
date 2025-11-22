import tkinter as tk
import random

# Simple Tetris implementation using tkinter
# Run: python tetris.py

CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

SHAPES = {
    'I': [
        [(0,1),(1,1),(2,1),(3,1)],
        [(2,0),(2,1),(2,2),(2,3)],
    ],
    'J': [
        [(0,0),(0,1),(1,1),(2,1)],
        [(1,0),(2,0),(1,1),(1,2)],
        [(0,1),(1,1),(2,1),(2,2)],
        [(1,0),(1,1),(0,2),(1,2)],
    ],
    'L': [
        [(2,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(1,2),(2,2)],
        [(0,1),(1,1),(2,1),(0,2)],
        [(0,0),(1,0),(1,1),(1,2)],
    ],
    'O': [
        [(1,0),(2,0),(1,1),(2,1)],
    ],
    'S': [
        [(1,0),(2,0),(0,1),(1,1)],
        [(1,0),(1,1),(2,1),(2,2)],
    ],
    'T': [
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(2,1),(1,2)],
        [(0,1),(1,1),(2,1),(1,2)],
        [(1,0),(0,1),(1,1),(1,2)],
    ],
    'Z': [
        [(0,0),(1,0),(1,1),(2,1)],
        [(2,0),(1,1),(2,1),(1,2)],
    ],
}

COLORS = {
    'I': '#00ffff',
    'J': '#0000ff',
    'L': '#ff7f00',
    'O': '#ffff00',
    'S': '#00ff00',
    'T': '#800080',
    'Z': '#ff0000',
}

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rot = 0
        self.x = 3
        self.y = 0

    def cells(self):
        rotations = SHAPES[self.shape]
        coords = rotations[self.rot % len(rotations)]
        return [(self.x + x, self.y + y) for x,y in coords]

    def rotated_cells(self, rot_delta=1):
        rotations = SHAPES[self.shape]
        rot = (self.rot + rot_delta) % len(rotations)
        coords = rotations[rot]
        return [(self.x + x, self.y + y) for x,y in coords]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH+150, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

        self.bag = []
        self.cur = None
        self.next = None
        self.game_over = False

        self.drop_interval = 700

        self.setup_bindings()
        self.spawn_piece()
        self.draw()
        self.tick()

    def setup_bindings(self):
        self.root.bind('<Left>', lambda e: self.move(-1))
        self.root.bind('<Right>', lambda e: self.move(1))
        self.root.bind('<Down>', lambda e: self.soft_drop())
        self.root.bind('<Up>', lambda e: self.rotate())

    def new_bag(self):
        pieces = list(SHAPES.keys())
        random.shuffle(pieces)
        self.bag.extend(pieces)

    def next_piece_from_bag(self):
        if not self.bag:
            self.new_bag()
        return Piece(self.bag.pop(0))

    def spawn_piece(self):
        if self.next is None:
            self.next = self.next_piece_from_bag()
        self.cur = self.next
        self.cur.x = 3
        self.cur.y = 0
        self.next = self.next_piece_from_bag()
        if self.collides(self.cur.cells()):
            self.game_over = True

    def collides(self, cells):
        for x,y in cells:
            if x < 0 or x >= COLS or y < 0 or y >= ROWS:
                return True
            if y >= 0 and self.board[y][x] is not None:
                return True
        return False

    def move(self, dx):
        if self.game_over:
            return
        self.cur.x += dx
        if self.collides(self.cur.cells()):
            self.cur.x -= dx
        else:
            self.draw()

    def rotate(self, dir=1):
        if self.game_over:
            return
        self.cur.rot = (self.cur.rot + dir) % len(SHAPES[self.cur.shape])
        if self.collides(self.cur.cells()):
            # simple wall-kick attempts
            for dx in (-1,1,-2,2):
                self.cur.x += dx
                if not self.collides(self.cur.cells()):
                    self.draw()
                    return
                self.cur.x -= dx
            # fail -> revert
            self.cur.rot = (self.cur.rot - dir) % len(SHAPES[self.cur.shape])
        else:
            self.draw()

    def soft_drop(self):
        if self.game_over:
            return
        self.cur.y += 1
        if self.collides(self.cur.cells()):
            self.cur.y -= 1
            self.lock_piece()
        else:
            self.score += 1
        self.draw()

    def lock_piece(self):
        for x,y in self.cur.cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.board[y][x] = COLORS[self.cur.shape]
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_board = [row[:] for row in self.board]
        lines = 0
        for y in range(ROWS-1, -1, -1):
            if all(new_board[y][x] is not None for x in range(COLS)):
                del new_board[y]
                new_board.insert(0, [None for _ in range(COLS)])
                lines += 1
        if lines:
            self.lines_cleared += lines
            self.score += (100 * (2 ** (lines-1))) * self.level
            self.level = 1 + self.lines_cleared // 10
            self.drop_interval = max(80, 700 - (self.level-1) * 60)
            self.board = new_board

    def restart(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.bag = []
        self.cur = None
        self.next = None
        self.game_over = False
        self.drop_interval = 700
        self.spawn_piece()
        self.draw()

    def tick(self):
        if not self.game_over:
            self.cur.y += 1
            if self.collides(self.cur.cells()):
                self.cur.y -= 1
                self.lock_piece()
            self.draw()
        self.root.after(self.drop_interval, self.tick)

    def draw_grid(self):
        for c in range(COLS+1):
            x = c * CELL_SIZE
            self.canvas.create_line(x, 0, x, HEIGHT, fill='#222')
        for r in range(ROWS+1):
            y = r * CELL_SIZE
            self.canvas.create_line(0, y, WIDTH, y, fill='#222')

    def draw_cell(self, x, y, color, offset_x=0):
        x0 = offset_x + x * CELL_SIZE
        y0 = y * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        self.canvas.create_rectangle(x0+1, y0+1, x1-1, y1-1, fill=color, outline='black')

    def draw(self):
        self.canvas.delete('all')
        # background for playfield
        self.canvas.create_rectangle(0,0,WIDTH,HEIGHT, fill='#111', outline='')
        # draw placed blocks
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.board[y][x])

        # draw current piece
        if self.cur:
            for x,y in self.cur.cells():
                if y >= 0:
                    self.draw_cell(x, y, COLORS[self.cur.shape])

        # draw grid lines
        self.draw_grid()

        # right panel
        off = WIDTH + 10
        self.canvas.create_text(off+70, 20, text='Next', fill='white', font=('Arial', 14))
        if self.next:
            # draw next piece small
            for x,y in SHAPES[self.next.shape][0]:
                self.draw_cell(x, y+1, COLORS[self.next.shape], offset_x=off)

        self.canvas.create_text(off+70, 140, text=f'Score: {self.score}', fill='white', font=('Arial', 12))
        self.canvas.create_text(off+70, 170, text=f'Level: {self.level}', fill='white', font=('Arial', 12))
        self.canvas.create_text(off+70, 200, text=f'Lines: {self.lines_cleared}', fill='white', font=('Arial', 12))

        if self.game_over:
            self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text='GAME OVER', fill='red', font=('Arial', 32))
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 20, text='Press R to restart', fill='white', font=('Arial', 14))


def main():
    root = tk.Tk()
    root.title('Tetris - tkinter')
    app = Tetris(root)
    root.mainloop()

if __name__ == '__main__':
    main()
