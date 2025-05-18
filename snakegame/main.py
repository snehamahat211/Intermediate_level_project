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
screen.onkey(snake.up,"w")
screen.onkey(snake.down,"s")
screen.onkey(snake.left,"a")
screen.onkey(snake.right,"d")



game_is_on=True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #detect collision with food and the distance between food and head
    if snake.head.distance(food) <15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()


    if snake.head.xcor()>290 or snake.head.xcor()<-290 or snake.head.ycor()>290 or snake.head.ycor()<-290:
        game_is_on=False
        scoreboard.game_over()

    #Detect the collision with tall.
    # for segment in snake.segments:
    #     if segment ==snake.head:
    #         pass
    #     elif snake.head.distance(segment)<10:
    #         game_is_on=False
    #         scoreboard.game_over()

    for segment in snake.segments[1:]:
        if snake.head.distance(segment)<10:
            game_is_on=False
            scoreboard.game_over()








screen.exitonclick()






