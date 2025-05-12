import turtle as t
import random

tim=t.Turtle()
t.colormode(255)
def random_color():
    r=random.randint(0,255)
    g= random.randint(0, 255)
    b= random.randint(0, 255)
    color=(r,g,b)
    return color
def draw(size):
    for _ in range(int(360 /size)):
        tim.speed("fastest")
        tim.color(random_color())
        tim.circle(100)
        current_heading=tim.heading()
        tim.setheading(tim.heading()+size)
draw(5)

screen=t.Screen()
screen.exitonclick()
