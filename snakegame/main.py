from turtle import Screen
import time
from snake import Snake
from Food import Food
from scoreboard import Scoreboard

screen=Screen()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title(" our snake game")
screen.tracer(0)

snake=Snake()
food= Food()
scoreboard=Scoreboard()

screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")



game_is_on=True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #detect collision with food and the distance between food and head
    if snake.head.distance(food) <15:
        food.refresh()
        scoreboard.increase_score()






screen.exitonclick()






