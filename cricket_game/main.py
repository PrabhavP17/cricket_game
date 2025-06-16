import pygame
import random
import sys
import math

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cricket Batting Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Load sounds
hit_sound = pygame.mixer.Sound("hit.mp3")

# Load background image
stadium_img = pygame.transform.scale(pygame.image.load("stadium.webp"), (WIDTH, HEIGHT))

# Load and scale batsman image
batsman_img = pygame.transform.scale(pygame.image.load("batsman.png"), (150, 240))

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)

# Menu function
def show_menu():
    while True:
        screen.fill(BLACK)
        title = big_font.render("Cricket Batting Game", True, YELLOW)
        start = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Pause function
def show_pause():
    paused = True
    while paused:
        screen.fill(BLACK)
        pause_text = big_font.render("Paused", True, YELLOW)
        cont = font.render("Press C to Continue or Q to Quit", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
        screen.blit(cont, (WIDTH // 2 - cont.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Call the menu at start
show_menu()

# Game variables
target = random.randint(10, 19)  # target below 20
balls_left = 6
score = 0
ball_speed = 10  # ball speed constant

# Batsman position
batsman_width, batsman_height = 150, 240
batsman_x = 80
batsman_y = HEIGHT // 2 - batsman_height // 2 + 50
batsman_pos = pygame.Rect(batsman_x, batsman_y, batsman_width, batsman_height)

# Ball position and initial speed
ball_start_y = batsman_y + batsman_height // 2 + 20
ball = pygame.Rect(WIDTH - 30, ball_start_y, 10, 10)

# Bubble positions
bubble_x = WIDTH - 80
bubble_scores = [6, 4, 3, 2, 1]
bubble_radius = 30
bubble_positions = [
    (bubble_x, 100),
    (bubble_x, 180),
    (bubble_x, 260),
    (bubble_x, 340),
    (bubble_x, 420),
]

# State variables
ball_moving_left = True
ball_hit = False
hit_valid = False
runs_to_score = 0
message = ""
message_timer = 0
target_bubble_pos = None

def reset_ball():
    global ball_speed_x, ball_speed_y, ball_moving_left, ball_hit, hit_valid, runs_to_score, message, message_timer, target_bubble_pos
    ball.x = WIDTH - 30
    ball.y = ball_start_y
    ball_speed_x = -ball_speed
    ball_speed_y = 0
    ball_moving_left = True
    ball_hit = False
    hit_valid = False
    runs_to_score = 0
    message = ""
    message_timer = 0
    target_bubble_pos = None

def calculate_runs_from_x(x):
    if 105 <= x <= 119:
        return 6
    elif 120 <= x <= 134:
        return 4
    elif 135 <= x <= 149:
        return 3
    elif 150 <= x <= 164:
        return 2
    elif 165 <= x <= 179:
        return 1
    else:
        return 0

def draw_scoreboard():
    pygame.draw.rect(screen, BLACK, (20, 20, 250, 120))
    screen.blit(font.render(f"TARGET: {target}", True, YELLOW), (30, 30))
    screen.blit(font.render(f"BALLS LEFT: {balls_left}", True, WHITE), (30, 60))
    screen.blit(font.render(f"SCORE: {score}", True, GREEN), (30, 90))
    if message:
        screen.blit(font.render(message, True, RED), (30, 120))

def draw_bubbles():
    for idx, (bx, by) in enumerate(bubble_positions):
        pygame.draw.circle(screen, BLUE, (bx, by), bubble_radius)
        text = font.render(str(bubble_scores[idx]), True, WHITE)
        text_rect = text.get_rect(center=(bx, by))
        screen.blit(text, text_rect)

def move_ball_towards_target():
    global ball_speed_x, ball_speed_y, ball_hit, balls_left, score, message, message_timer, runs_to_score, hit_valid, ball_moving_left, target_bubble_pos

    dx = target_bubble_pos[0] - ball.x
    dy = target_bubble_pos[1] - ball.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        dist = 1

    move_x = (dx / dist) * ball_speed
    move_y = (dy / dist) * ball_speed
    ball.x += move_x
    ball.y += move_y

    if dist < ball_speed:
        if hit_valid:
            score += runs_to_score
            if score >= target:
                message = "You Win!"
                screen.blit(big_font.render(message, True, RED), (WIDTH // 2 - 80, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
        balls_left -= 1
        reset_ball()

reset_ball()
running = True

while running:
    screen.blit(stadium_img, (0, 0))
    draw_scoreboard()
    screen.blit(batsman_img, (batsman_pos.x, batsman_pos.y))
    draw_bubbles()
    pygame.draw.ellipse(screen, RED, ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ball_moving_left:
                    if ball.right > batsman_pos.left:
                        ball_hit = True
                        ball_moving_left = False
                        hit_valid = True
                        hit_sound.play()  # 🎵 Play sound on hit
                        runs_to_score = calculate_runs_from_x(ball.x)
                        if runs_to_score > 0:
                            index = bubble_scores.index(runs_to_score)
                            target_bubble_pos = bubble_positions[index]
                        else:
                            target_bubble_pos = (batsman_pos.right + 50, ball.y)
                        message = f"Runs Scored: {runs_to_score}"
                        message_timer = 60
                    else:
                        message = "Too Late!"
                        message_timer = 60
                        hit_valid = False
                else:
                    message = "Too Early!"
                    message_timer = 60
                    hit_valid = False
            elif event.key == pygame.K_p:
                show_pause()

    if ball_moving_left:
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.right < batsman_pos.left:
            balls_left -= 1
            message = "Missed!"
            message_timer = 60
            reset_ball()
    else:
        if target_bubble_pos:
            move_ball_towards_target()
        else:
            ball.x += ball_speed
            if ball.left > WIDTH:
                if hit_valid:
                    score += runs_to_score
                balls_left -= 1
                reset_ball()

    if message_timer > 0:
        message_timer -= 1
    else:
        message = ""

    if balls_left == 0 and running:
        result_text = "You Win!" if score >= target else "You Lose!"
        end_msg = big_font.render(result_text, True, RED)
        screen.blit(end_msg, (WIDTH // 2 - end_msg.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
