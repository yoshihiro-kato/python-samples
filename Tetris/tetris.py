import tkinter as tk,random as r
C=30;CO=10;RO=20;W=C*CO;H=C*RO
S={'I':[[(0,1),(1,1),(2,1),(3,1)],[(2,0),(2,1),(2,2),(2,3)]],'J':[[(0,0),(0,1),(1,1),(2,1)],[(1,0),(2,0),(1,1),(1,2)],[(0,1),(1,1),(2,1),(2,2)],[(1,0),(1,1),(0,2),(1,2)]],'L':[[(2,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(1,2),(2,2)],[(0,1),(1,1),(2,1),(0,2)],[(0,0),(1,0),(1,1),(1,2)]],'O':[[(1,0),(2,0),(1,1),(2,1)]],'S':[[(1,0),(2,0),(0,1),(1,1)],[(1,0),(1,1),(2,1),(2,2)]],'T':[[(1,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(2,1),(1,2)],[(0,1),(1,1),(2,1),(1,2)],[(1,0),(0,1),(1,1),(1,2)]],'Z':[[(0,0),(1,0),(1,1),(2,1)],[(2,0),(1,1),(2,1),(1,2)]]}
B=[[0]*CO for _ in range(RO)];cur={'s':'I','r':0,'x':3,'y':0};d=700;rt=cv=0;go=0
c=lambda p:[(p['x']+x,p['y']+y)for x,y in S[p['s']][p['r']%len(S[p['s']])]]
coll=lambda p:any(x<0 or x>=CO or y<0 or y>=RO or y>=0 and B[y][x] for x,y in p)
def spawn():
 global cur,go;cur={'s':r.choice(list(S)),'r':0,'x':3,'y':0};go=coll(c(cur))
def lock():
 [B[y].__setitem__(x,1)for x,y in c(cur)if 0<=y<RO and 0<=x<CO];spawn();draw()
def cl():
 global B,d;nb=[r[:] for r in B];l=0
 for y in range(RO-1,-1,-1):[None for x in range(CO)if not nb[y][x]]or(nb.pop(y),nb.insert(0,[0]*CO),l:=l+1)
 l and(d:=max(80,d-l*60),B:=nb)
def move(dx):go or(cur.__setitem__('x',cur['x']+dx),coll(c(cur))and cur.__setitem__('x',cur['x']-dx),draw())
def rotate(d=1):
 if go:return
 s=cur['s'];cur['r']=(cur['r']+d)%len(S[s])
 coll(c(cur))and[cur.__setitem__('x',cur['x']+dx)or not coll(c(cur))or(cur.__setitem__('x',cur['x']-dx))for dx in(-1,1,-2,2)]or 1;draw()
def soft():go or(cur.__setitem__('y',cur['y']+1),coll(c(cur))and(cur.__setitem__('y',cur['y']-1),lock()or cl())or 1,draw())
def tick():
 not go and(cur.__setitem__('y',cur['y']+1),coll(c(cur))and(cur.__setitem__('y',cur['y']-1),lock()or cl()),draw());rt.after(d,tick)
def draw():
 cv.delete('all');cv.create_rectangle(0,0,W,H,fill='#111')
 for y in range(RO):
  for x in range(CO):
   if B[y][x]:cv.create_rectangle(x*C+1,y*C+1,x*C+C-1,y*C+C-1,fill='#D3D3D3',outline='black')
 for x,y in c(cur):
  if y>=0:cv.create_rectangle(x*C+1,y*C+1,x*C+C-1,y*C+C-1,fill='#D3D3D3',outline='black')
def key(e):
 {'Left':lambda:move(-1),'Right':lambda:move(1),'Up':lambda:rotate(),'Down':lambda:soft()}.get(e.keysym,lambda:0)()
rt=tk.Tk();rt.title('T');cv=tk.Canvas(rt,width=W,height=H,bg='#111');cv.pack();rt.bind('<Key>',key);spawn();draw();rt.after(d,tick);rt.mainloop()
