import tkinter as tk, random

CELL=30;COLS=10;ROWS=20;W=CELL*COLS;H=CELL*ROWS
SHAPES={'I':[[ (0,1),(1,1),(2,1),(3,1) ],[(2,0),(2,1),(2,2),(2,3)]],
        'J':[[(0,0),(0,1),(1,1),(2,1)],[(1,0),(2,0),(1,1),(1,2)],[(0,1),(1,1),(2,1),(2,2)],[(1,0),(1,1),(0,2),(1,2)]],
        'L':[[(2,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(1,2),(2,2)],[(0,1),(1,1),(2,1),(0,2)],[(0,0),(1,0),(1,1),(1,2)]],
        'O':[[(1,0),(2,0),(1,1),(2,1)]],
        'S':[[(1,0),(2,0),(0,1),(1,1)],[(1,0),(1,1),(2,1),(2,2)]],
        'T':[[(1,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(2,1),(1,2)],[(0,1),(1,1),(2,1),(1,2)],[(1,0),(0,1),(1,1),(1,2)]],
        'Z':[[(0,0),(1,0),(1,1),(2,1)],[(2,0),(1,1),(2,1),(1,2)]]}
COLOR='#D3D3D3'
board=[[None]*COLS for _ in range(ROWS)]; cur=None; score=0; drop=700; root=None; cv=None; game_over=False
def make(shape): return {'s':shape,'r':0,'x':3,'y':0}
def cells(p): R=SHAPES[p['s']]; return [(p['x']+x,p['y']+y) for x,y in R[p['r']%len(R)]]
def coll(c):
    for x,y in c:
        if x<0 or x>=COLS or y<0 or y>=ROWS: return True
        if y>=0 and board[y][x] is not None: return True
    return False
def spawn():
    global cur,game_over
    cur=make(random.choice(list(SHAPES.keys())))
    if coll(cells(cur)): game_over=True
def lock():
    global board
    for x,y in cells(cur):
        if 0<=y<ROWS and 0<=x<COLS: board[y][x]=COLOR
    clear_lines(); spawn()
def clear_lines():
    global board,score,drop
    nb=[r[:] for r in board];lines=0
    for y in range(ROWS-1,-1,-1):
        if all(nb[y][x] is not None for x in range(COLS)):
            del nb[y]; nb.insert(0,[None]*COLS); lines+=1
    if lines:
        score += 100*(2**(lines-1))
        drop = max(80, drop - lines*60)
        board=nb
def move(dx):
    if game_over: return
    cur['x']+=dx
    if coll(cells(cur)): cur['x']-=dx
    draw()
def rotate(d=1):
    if game_over: return
    s=cur['s']; cur['r']=(cur['r']+d)%len(SHAPES[s])
    if coll(cells(cur)):
        for dx in (-1,1,-2,2):
            cur['x']+=dx
            if not coll(cells(cur)): draw(); return
            cur['x']-=dx
        cur['r']=(cur['r']-d)%len(SHAPES[s])
    draw()
def soft():
    global score
    if game_over: return
    cur['y']+=1
    if coll(cells(cur)): cur['y']-=1; lock()
    else: score+=1
    draw()
def restart():
    global board,score,drop,game_over
    board=[[None]*COLS for _ in range(ROWS)]; score=0; drop=700; game_over=False
    spawn(); draw()
def tick():
    if not game_over:
        cur['y']+=1
        if coll(cells(cur)): cur['y']-=1; lock()
        draw()
    root.after(drop,tick)
def draw_cell(x,y,color):
    x0=x*CELL; y0=y*CELL; x1=x0+CELL; y1=y0+CELL
    cv.create_rectangle(x0+1,y0+1,x1-1,y1-1,fill=color,outline='black')
def draw():
    cv.delete('all'); cv.create_rectangle(0,0,W,H,fill='#111',outline='')
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x]: draw_cell(x,y,board[y][x])
    if cur:
        for x,y in cells(cur):
            if y>=0: draw_cell(x,y,COLOR)
    for c in range(COLS+1): cv.create_line(c*CELL,0,c*CELL,H,fill='#222')
    for r in range(ROWS+1): cv.create_line(0,r*CELL,W,r*CELL,fill='#222')
    cv.create_text(W+30,120,text=f'Score: {score}',fill='white',font=('Arial',12))
    if game_over: cv.create_text(W//2,H//2-20,text='GAME OVER',fill='red',font=('Arial',32))
def key(e):
    k=e.keysym
    if k=='Left': move(-1)
    elif k=='Right': move(1)
    elif k=='Up': rotate(1)
    elif k=='Down': soft()
    elif k in ('r','R'): restart()
def main():
    global root,cv
    root=tk.Tk(); root.title('Tetris'); cv=tk.Canvas(root,width=W+80,height=H,bg='black'); cv.pack()
    root.bind('<Key>',key)
    spawn(); draw(); tick(); root.mainloop()
if __name__=='__main__': main()
