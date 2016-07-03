import turtle

canvas = turtle.Screen()
canvas.bgcolor("red")

pencil = turtle.Turtle()
pencil.shape("turtle")
pencil.speed(0)

def draw_trianlge_up(color, size):
    pencil.color(color, color)
    pencil.begin_fill()
    pencil.right(60)
    for i in range(3):
        pencil.forward(size)
        pencil.right(120)
    pencil.end_fill()

    
def draw_trianlge_down(color, size):
    pencil.color(color, color)
    pencil.begin_fill()
    for i in range(3):
        pencil.forward(size)
        pencil.right(120)
    pencil.end_fill()

draw_trianlge_up("green", 200)

for i in range(4):
    pencil.forward(25)
    draw_trianlge_up("white", 25)

            
##for j in range(72):
##    draw_trianlge("blue")
##    pencil.right(5)
##
##pencil.right(90)
##pencil.forward(200)

#canvas.exitonclick()



