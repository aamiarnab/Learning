import turtle

canvas = turtle.Screen()
canvas.bgcolor("white")

pencil = turtle.Turtle()
pencil.shape("turtle")
pencil.speed(0)

def draw_rhombus(color):
    pencil.color(color)
    for i in range(2):
        pencil.forward(50)
        pencil.right(30)
        pencil.forward(50)
        pencil.right(150)
            
for j in range(72):
    draw_rhombus("blue")
    pencil.right(5)

pencil.right(90)
pencil.forward(200)

#canvas.exitonclick()



