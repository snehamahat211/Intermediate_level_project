from turtle import Screen,Turtle
import time

screen=Screen()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title(" our snake game")
screen.tracer(0)

starting_position=[(0,0),(-20,0),(-40,0)]  #placing
segments=[]
#creates snake
for position in starting_position:
    new_segment=Turtle("square")
    new_segment.color("white")
    new_segment.penup()
    new_segment.goto(position)
    segments.append(new_segment)

game_is_on=True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    for segment in range(len(segments)-1,0,-1):
        new_x=segments[segment-1].xcor()
        new_y=segments[segment-1].ycor()
        segments[segment].goto(new_x,new_y)
    segments[0].forward(20)
    segments[0].left(90)




