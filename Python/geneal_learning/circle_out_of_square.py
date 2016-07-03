import turtle

canvas = turtle.Screen()
canvas.bgcolor("blue")

pencil = turtle.Turtle()
pencil.shape("turtle")
pencil.speed(0)

def draw_square():
    pencil.color("red")
    j = 0
    for j in range(72):
        i = 0
        while i < 4:
            pencil.forward(100)
            pencil.right(90)
            i +=1
        pencil.right(5)
        
draw_square()
canvas.exitonclick()



