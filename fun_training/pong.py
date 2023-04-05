import pygame
import random

# Set up the colors we will use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the dimensions of the game window
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
PADDLE_HEIGHT = 100

# Set up the starting positions for the paddles and the ball
LEFT_PADDLE_POS = [30, (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2]
RIGHT_PADDLE_POS = [WINDOW_WIDTH - 30, (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2]
BALL_POS = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]

# Set up the movement speeds for the paddles and the ball
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the game window
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the window title
pygame.display.set_caption("Pong")

# Set up the game clock
clock = pygame.time.Clock()

# Create the paddles and the ball as Rectangles
left_paddle = pygame.Rect(LEFT_PADDLE_POS[0], LEFT_PADDLE_POS[1], 10, PADDLE_HEIGHT)
right_paddle = pygame.Rect(RIGHT_PADDLE_POS[0], RIGHT_PADDLE_POS[1], 10, PADDLE_HEIGHT)
ball = pygame.Rect(BALL_POS[0], BALL_POS[1], 10, 10)

# Set up the starting scores for each player
left_score = 0
right_score = 0

# Create the font object for displaying the scores
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:

    # Handle events (such as quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles when the corresponding keys are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_s] and left_paddle.bottom < WINDOW_HEIGHT:
        left_paddle.move_ip(0, PADDLE_SPEED)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_DOWN] and right_paddle.bottom < WINDOW_HEIGHT:
        right_paddle.move_ip(0, PADDLE_SPEED)
    


    # Move the ball
    ball.move_ip(BALL_SPEED_X, BALL_SPEED_Y)

    # Bounce off the top and bottom of the screen
    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        BALL_SPEED_Y *= -1.02

    # Bounce off the left and right paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X *= -1

    # Detect when the ball goes past a paddle
    if ball.left <= 0:
        right_score += 1
        ball.center = BALL_POS
        BALL_SPEED_X *= -1
    elif ball.right >= WINDOW_WIDTH:
        left_score += 1
        ball.center = BALL_POS
        BALL_SPEED_X *= -1

    # Fill the background color
    screen.fill(BLACK)

    # Draw the paddles, ball and scores on the screen
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (WINDOW_WIDTH / 4, 10))
    screen.blit(right_score_text, (WINDOW_WIDTH * 3 / 4, 10))

    # Update the game display
    pygame.display.flip()

    # Set the game clock framerate
    clock.tick(60)

# Quit Pygame and the program
pygame.quit()
quit()
