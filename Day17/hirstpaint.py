# import colorgram
#
# rgb_colors=[]
# colors=colorgram.extract('image.jpg',30)
# for color in colors:
#     r=color.rgb.r
#     g=color.rgb.g
#     b=color.rgb.b
#     new_color=(r,g,b)
#     rgb_colors.append(new_color)
#
# print(rgb_colors)

import turtle as turtle_module
import random
turtle_module.colormode(255)
tim=turtle_module.Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()
color_list=[(0, 0, 0), (241, 229, 215), (229, 152, 90), (237, 215, 81), (120, 176, 201), (23, 115, 164), (206, 228, 220), (214, 131, 162), (234, 206, 215), (117, 192, 160), (216, 76, 116), (195, 215, 224), (35, 181, 133), (18, 174, 200), (207, 67, 19), (156, 59, 108), (240, 159, 180), (161, 182, 23), (144, 216, 197), (25, 140, 101), (237, 85, 44), (239, 214, 5), (160, 21, 59), (244, 169, 152), (146, 210, 219), (15, 62, 136), (109, 117, 170), (10, 95, 62), (181, 183, 217), (69, 27, 76)]

tim.setheading(225)
tim.forward(300)
tim.setheading(0)
num=100

for dot in range(1,num+1):
    tim.dot(20,random.choice(color_list))
    tim.forward(50)

    if dot %10==0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)