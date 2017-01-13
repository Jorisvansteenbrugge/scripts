from Tkinter import *
global x0,x1,y0,y1
x0=20
y0=0
x1=50
y1=50

def upKey(event):
    global x0,x1,y0,y1, rect
    y0 -= 5
    y1 -= 5
    if(rect):
        w.delete(rect)
    rect = w.create_rectangle(x0,y0,x1,y1, fill="blue")
    w.update()
    #paint()

def downKey(event):
    global x0,x1,y0,y1, rect
    y0 += 5
    y1 += 5
    if(rect):
        w.delete(rect)
    rect = w.create_rectangle(x0,y0,x1,y1, fill="blue")
    w.update()
    #paint()

def leftKey(event):
    global x0,x1,y0,y1, rect
    x0 -= 5
    x1 -= 5
    if(rect):
        w.delete(rect)
    rect = w.create_rectangle(x0,y0,x1,y1, fill="blue")
    w.update()
    #paint())

def rightKey(event):
    global x0,x1,y0,y1, rect
    x0 += 5
    x1 += 5
    if(rect):
        w.delete(rect)
    rect = w.create_rectangle(x0,y0,x1,y1, fill="blue")
    w.update()

def paint():
    global w, rect
    
    w = Canvas(master, width=400, height=400)
    w.pack()
    rect = w.create_rectangle(x0,y0,x1,y1, fill="blue")


if __name__ == "__main__" :
    master = Tk()
    master.title("Rstudio")

    paint()

    master.bind('<Up>', upKey)
    master.bind('<Down>', downKey)
    master.bind('<Left>', leftKey)
    master.bind('<Right>', rightKey)
    mainloop()
