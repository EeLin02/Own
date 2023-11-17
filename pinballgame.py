# Importing the turtle and random library
import turtle
from random import randint

# Creating the screen with name and size
screen = turtle.Screen()
screen.title("DataFlair Pinball game")
screen.setup(width=1000, height=600)

# Creating the paddle
paddle = turtle.Turtle()
# Setting its speed as zero, it moves only when a key is pressed
paddle.speed(0)
# Setting shape, color, and size
paddle.shape("square")
paddle.color("blue")
paddle.shapesize(stretch_wid=2, stretch_len=6)
paddle.penup()
# The paddle is left-centered initially
paddle.goto(-400, -250)

# Creating the ball of circle shape
ball = turtle.Turtle()
# Setting the speed of the ball to 0, it moves based on the dx and dy values
ball.speed(0)
# Setting shape, color, and size
ball.shape("circle")
ball.color("red")
ball.penup()
# Ball starts from a random position from the top of the screen
x = randint(-400, 400)
ball.goto(x, 260)
# Setting dx and dy that decide the speed of the ball
ball.dx = 2
ball.dy = -2

score = 0

# Displaying the score
scoreBoard = turtle.Turtle()
scoreBoard.speed(0)
scoreBoard.penup()
# Hiding the turtle to show text
scoreBoard.hideturtle()
# Locating the score board on top of the screen
scoreBoard.goto(0, 260)
# Showing the score
scoreBoard.write("Score: 0", align="center", font=("Courier", 20, "bold"))

# Function to display the game over message and ask for a play again
def game_over():
    screen.update()
    ball.goto(0, 0)
    scoreBoard.clear()
    message = "Game Over\nYour Score: " + str(score)
    message += "\nPlay again? (yes or no):"
    play_again = screen.textinput("Game Over", message)
    if play_again and play_again.lower() == "yes":
        reset_game()
    else:
        screen.bye()

# Function to rebind the keyboard commands
def rebind_keyboard():
    screen.onkeypress(movePadRight, "Right")
    screen.onkeypress(movePadLeft, "Left")
    screen.listen()  # Re-listen for keyboard input

# Function to reset the game
def reset_game():
    ball.goto(randint(-400, 400), 260)
    ball.dy = -2
    ball.dx = 2
    global score
    score = 0
    scoreBoard.clear()
    scoreBoard.write("Score: 0", align="center", font=("Courier", 20, "bold"))
    rebind_keyboard()  # Rebind the keyboard commands


# Functions to move the paddle left and right
def movePadRight():
    x = paddle.xcor()  # Getting the current x-coordinate of the paddle
    x += 15
    paddle.setx(x)  # Updating the x-coordinate of the paddle

# Function to move the left paddle down
def movePadLeft():
    x = paddle.xcor()  # Getting the current x-coordinate of the paddle
    x -= 15
    paddle.setx(x)  # Updating the x-coordinate of the paddle

def game_over():
    screen.update()
    ball.goto(0, 0)
    scoreBoard.clear()
    message = "Game Over\nYour Score: " + str(score)
    if score>=5 and score<=10:
        message += "\nCongratulations! You've earned a 10% discount voucher."
    elif score > 20:
        message += "\nCongratulations! You've earned a 20% discount voucher."
    else:
        message += "\nTry again."
    message += "\nPlay again? (yes or no):"
    play_again = screen.textinput("Game Over", message)
    if play_again and play_again.lower() == "yes":
        reset_game()
    else:
        screen.bye()

# Mapping the functions to the keyboard buttons
screen.listen()
screen.onkeypress(movePadRight, "Right")
screen.onkeypress(movePadLeft, "Left")

# Game loop
while True:
    # Rebind keyboard inputs continuously
    rebind_keyboard()

    # Updating the screen every time with the new changes
    screen.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Checking if ball hits the left, right, and top walls of the screen
    if ball.xcor() > 480:
        ball.setx(480)
        ball.dx *= -1  # Bouncing the ball

    if ball.xcor() < -480:
        ball.setx(-480)
        ball.dx *= -1  # Bouncing the ball

    if ball.ycor() > 280:
        ball.sety(280)
        ball.dy *= -1  # Bouncing the ball

    # Checking if the ball hits the bottom and ending the game
    if ball.ycor() < -280:
        game_over()

    # Checking if the paddle hits the ball, updating the score, increasing speed, and bouncing the ball
    if (paddle.ycor() + 30 > ball.ycor() > paddle.ycor() - 30 and
            paddle.xcor() + 50 > ball.xcor() > paddle.xcor() - 50):

        # Increasing the score
        score += 1
        scoreBoard.clear()
        scoreBoard.write("Score: {}".format(score), align="center", font=("Courier", 20, "bold"))

        # Increasing the speed of the ball with a limit
        if ball.dx > 0:
            ball.dx += 0.5
        else:
            ball.dx -= 0.5

        if ball.dy > 0:
            ball.dy += 0.5
        else:
            ball.dy -= 0.5

        if score >= 10 and score < 15:
            game_over()

        # Bouncing the ball
        ball.dy *= -1
