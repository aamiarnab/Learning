import turtle

canvas = turtle.Screen()
canvas.bgcolor("blue")

pencil = turtle.Turtle()
pencil.shape("turtle")
pencil.speed(3)

def draw_square():
    pencil.color("red")
    i = 0
    while i < 4:
        pencil.forward(100)
        pencil.right(90)
        i +=1

def draw_circle():
    pencil.color("yellow")
    pencil.circle(100)

def draw_triangle():
    pencil.color("white")
    i = 0
    while i < 3:
        pencil.forward(100)
        pencil.right(120)
        i +=1
        
draw_square()
draw_circle()
draw_triangle()
canvas.exitonclick()



