import turtle

# Define paramters for art
num_rects = 22
r_width = 80
r_length = 160

def draw_rect(_turtle, _length, _width):
    '''
    :param _turtle: turtle to use
    :param _length: length of the rectangle
    :param _width: width of the rectangle
    :return:
    '''
    for i in range(0, 4):
        if i % 2 == 0:
            _turtle.forward(_length)
        else:
            _turtle.forward(_width)
        _turtle.right(90)

def draw_art():
    # Create a window and set background color
    window = turtle.Screen()
    window.bgcolor("white")

    # Create a turtle
    myTurtle = turtle.Turtle()
    myTurtle.shape("classic")
    myTurtle.color("red")
    myTurtle.speed(4)

    # loop through number of rects
    for i in range(0, num_rects):
        draw_rect(myTurtle, r_length, r_width)
        myTurtle.right(360/num_rects)

    window.exitonclick()

draw_art()