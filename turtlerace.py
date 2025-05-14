#timmy=Turtle object is tim and class is turtle

#state instances
#turtle co-ordinate system
import random
from turtle import Turtle,Screen
# tim=Turtle()
is_race_on=False
screen=Screen()
screen.setup(500,400)
user=screen.textinput("Make your bet","Which turtle will wun the race? Enter a color:")
print(user)

colors=["red","brown","black","green","blue","purple"]
y_position=[-70,-40,-10,20,50,80]
all_turtle=[]
for turtle_index in range(0,6):
    new_turtle=Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=y_position[turtle_index])
    all_turtle.append(new_turtle)

if user:
    is_race_on= True

while is_race_on:

    for turtle in all_turtle:
        if turtle.xcor()>230:
            is_race_on=False
            winning=turtle.pencolor()
            if winning==user:
                print(f"you've won! The {winning} turtle is the winner")
            else:
                print(f"you've lose the game. The {winning} turtle is the winner")

        rand_dist=random.randint(0,10)
        turtle.forward(rand_dist)





screen.exitonclick()
