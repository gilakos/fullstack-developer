import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("white")

    myTurtle = turtle.Turtle()
    myTurtle.shape("classic")
    myTurtle.color("red")
    myTurtle.speed(1)

    myTurtle.forward(100)
    myTurtle.right(90)
    myTurtle.forward(100)
    myTurtle.right(90)
    myTurtle.forward(100)
    myTurtle.right(90)
    myTurtle.forward(100)

    window.exitonclick()

draw_square()