import tkinter as tk,random as r
w,h=10,20
b=[[0]*w for _ in range(h)]
shapes=[[[(0,0),(0,1),(1,0),(1,1)]],[[(0,0),(0,1),(0,2),(0,3)]],[[(0,0),(1,0),(1,1),(1,2)]],[[(0,0),(0,1),(1,1),(1,2)]],[[(0,1),(1,0),(1,1),(2,0)]],[[(0,0),(1,0),(2,0),(2,1)]],[[(0,0),(1,0),(2,0),(0,1)]]]
p=r.choice(shapes)[0]
x,y,t=w//2-1,0,0
root=tk.Tk();root.title('Tetris Golf');c=tk.Canvas(root,width=200,height=400,bg='black');c.pack()
def d():
 c.delete('all')
 for i in range(h):
  for j in range(w):c.create_rectangle(j*20,i*20,j*20+20,i*20+20,fill='white'if b[i][j]else'gray20',outline='gray30')
 [c.create_rectangle((x+px)*20,(y+py)*20,(x+px)*20+20,(y+py)*20+20,fill='yellow')for px,py in p if 0<=y+py<h]
 root.title(f'Score:{t}')
def r_():global p;p=[(py,-px)for px,py in p]
def m(dx):global x;x=max(0,min(x+dx,w-2))
def c_():
 global t
 for i,row in enumerate(b):
  if all(row):b.pop(i);b.insert(0,[0]*w);t+=10
def chk():return all(0<=x+px<w and(y+py<0 or y+py<h and not b[y+py][x+px])for px,py in p)
def loop():
 global x,y,p,t
 y+=1
 if not chk():y-=1;[b[y+py].__setitem__(x+px,1)for px,py in p if 0<=x+px<w and 0<=y+py<h];c_();p=r.choice(shapes)[0];x,y=w//2-1,0;chk()or root.quit()
 d();root.after(300,loop)
root.bind('<a>',lambda e:m(-1));root.bind('<d>',lambda e:m(1));root.bind('<w>',lambda e:r_());loop();root.mainloop()
