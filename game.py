import pygame
import sys
import random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, power_up_active, power_up_timer
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # player score
    if ball.left <= 0:
        player_score += 1
        if player_score - opponent_score >= 3:
            power_up_active = True
            power_up_timer = pygame.time.get_ticks()
        score_time = pygame.time.get_ticks()

    # opponent score
    if ball.right >= screen_width:
        opponent_score += 1
        if opponent_score - player_score >= 3:
            power_up_active = True
            power_up_timer = pygame.time.get_ticks()
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, white)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_number = game_font.render("2", False, white)
        screen.blit(number_number, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, white)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

def activate_power_up():
    global ball_color, ball_speed_x, ball_speed_y, power_up_active, power_up_timer
    if power_up_active:
        ball_color = [random.randint(0, 255) for _ in range(3)]
        ball_speed_x *= 1.3
        ball_speed_y *= 1.3
        if pygame.time.get_ticks() - power_up_timer >= 5000:
            ball_color = (255, 255, 255)
            ball_speed_x /= 1.3
            ball_speed_y /= 1.3
            power_up_active = False

# normal game set up
pygame.init()
clock = pygame.time.Clock()

# to set the screen size of the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Rectangles for the game
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = pygame.Color(0, 0, 0)
ball_color = (255, 255, 255)
line_color = (132, 132, 130)
player_color = (0, 255, 0)
opponent_color = (255, 0, 0)
white = (255, 255, 255)

# game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
power_up_active = False
power_up_timer = 0

# score timer
score_time = True

# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# condition for the game to run
running = False
paused = False

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Start
                running = True
            elif event.key == pygame.K_p:  # Pause
                paused = not paused
            elif event.key == pygame.K_q:  # Stop
                running = False
                player_score = 0
                opponent_score = 0
            elif event.key == pygame.K_UP:  # Move player paddle up
                if running and not paused:
                    player_speed -= 7
            elif event.key == pygame.K_DOWN:  # Move player paddle down
                if running and not paused:
                    player_speed += 7

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:  # Stop player paddle movement
                player_speed = 0

    if running and not paused:
        ball_animation()
        player_animation()
        opponent_animation()
        activate_power_up()

    # game visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, opponent_color, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, line_color, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_start()

    player_text = game_font.render(f"{player_score}", False, white)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, white)
    screen.blit(opponent_text, (600, 470))

    # updating the game window
    pygame.display.flip()
    clock.tick(75)