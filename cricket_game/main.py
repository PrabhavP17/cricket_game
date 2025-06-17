import pygame
import random
import sys
import math

# Initialize Pygame and sound mixer
pygame.init()
pygame.mixer.init()

# Set screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cricket Batting Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Load sound effects
hit_sound = pygame.mixer.Sound("hit.mp3")
cheer_sound = pygame.mixer.Sound("cheer.mp3")
cheer_sound.set_volume(1.0)

# Load images
stadium_img = pygame.transform.scale(pygame.image.load("stadium.webp"), (WIDTH, HEIGHT))
batsman_img = pygame.transform.scale(pygame.image.load("batsman.png"), (150, 240))

# Define colors
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)

# Let user choose number of overs
def get_overs_selection():
    while True:
        screen.blit(stadium_img, (0, 0))
        # Display overs options
        title = big_font.render("Choose Overs", True, YELLOW)
        option1 = font.render("1. Press 1 for 1 Over (6 balls)", True, WHITE)
        option2 = font.render("2. Press 2 for 2 Overs (12 balls)", True, WHITE)
        option3 = font.render("3. Press 5 for 5 Overs (30 balls)", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, HEIGHT // 2))
        screen.blit(option3, (WIDTH // 2 - option3.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        # Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 6, random.randint(10, 20)
                elif event.key == pygame.K_2:
                    return 12, random.randint(25, 40)
                elif event.key == pygame.K_5:
                    return 30, random.randint(45, 60)

# Show game instructions before play
def show_instructions(balls_left, target):
    screen.blit(stadium_img, (0, 0))
    target_text = big_font.render(f"Target: {target} in {balls_left} balls", True, YELLOW)
    instruction1 = font.render("Press SPACEBAR to hit the ball", True, WHITE)
    instruction2 = font.render("Press P to Pause", True, WHITE)
    instruction3 = font.render("Press Q to Quit", True, WHITE)
    screen.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 2))
    screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(instruction3, (WIDTH // 2 - instruction3.get_width() // 2, HEIGHT // 2 + 80))
    pygame.display.flip()
    pygame.time.wait(7000)

# Main menu screen
def show_menu():
    while True:
        screen.blit(stadium_img, (0, 0))
        pygame.draw.rect(screen, LIGHT_BLUE, (200, 150, 400, 300), border_radius=20)
        title = big_font.render("🏏 Cricket Batting Game 🏏", True, ORANGE)
        start = font.render("Press ENTER to Start", True, BLUE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Pause screen
def show_pause():
    paused = True
    while paused:
        screen.blit(stadium_img, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0, 180), (150, 200, 500, 200), border_radius=15)
        pause_text = big_font.render("⏸️ Paused", True, RED)
        cont = font.render("Press C to Continue or Q to Quit", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(cont, (WIDTH // 2 - cont.get_width() // 2, HEIGHT // 2 + 20))
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

# Start game setup
show_menu()
balls_left, target = get_overs_selection()
show_instructions(balls_left, target)

# Game variables
score = 0
ball_speed = 10

# Batsman setup
batsman_width, batsman_height = 150, 240
batsman_x = 80
batsman_y = HEIGHT // 2 - batsman_height // 2 + 50
batsman_pos = pygame.Rect(batsman_x, batsman_y, batsman_width, batsman_height)

# Ball setup
ball_start_y = batsman_y + batsman_height // 2 + 20
ball = pygame.Rect(WIDTH - 30, ball_start_y, 10, 10)

# Bubbles showing scoring zones
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

# State flags and counters
ball_moving_left = True
ball_hit = False
hit_valid = False
runs_to_score = 0
message = ""
message_timer = 0
target_bubble_pos = None

# Reset ball after each turn
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

# Decide runs based on ball's x position
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

# Draw scoreboard on top-left
def draw_scoreboard():
    pygame.draw.rect(screen, BLACK, (20, 20, 250, 120))
    screen.blit(font.render(f"TARGET: {target}", True, YELLOW), (30, 30))
    screen.blit(font.render(f"BALLS LEFT: {balls_left}", True, WHITE), (30, 60))
    screen.blit(font.render(f"SCORE: {score}", True, GREEN), (30, 90))
    if message:
        screen.blit(font.render(message, True, RED), (30, 120))

# Draw scoring bubbles
def draw_bubbles():
    for idx, (bx, by) in enumerate(bubble_positions):
        pygame.draw.circle(screen, BLUE, (bx, by), bubble_radius)
        text = font.render(str(bubble_scores[idx]), True, WHITE)
        text_rect = text.get_rect(center=(bx, by))
        screen.blit(text, text_rect)

# Move the hit ball toward the bubble
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
                cheer_sound.play()
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

# Main game loop
while running:
    screen.blit(stadium_img, (0, 0))
    draw_scoreboard()
    screen.blit(batsman_img, (batsman_pos.x, batsman_pos.y))
    draw_bubbles()
    pygame.draw.ellipse(screen, RED, ball)

    # Handle inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ball_moving_left:
                    if ball.right > batsman_pos.left:
                        # Valid hit
                        ball_hit = True
                        ball_moving_left = False
                        hit_valid = True
                        hit_sound.play()
                        runs_to_score = calculate_runs_from_x(ball.x)
                        if runs_to_score > 0:
                            index = bubble_scores.index(runs_to_score)
                            target_bubble_pos = bubble_positions[index]
                            if runs_to_score >= 4:
                                cheer_sound.play()
                        else:
                            target_bubble_pos = (batsman_pos.right + 50, ball.y)
                        message = f"Runs Scored: {runs_to_score}"
                        message_timer = 60
                    else:
                        # Too late
                        message = "Too Late!"
                        message_timer = 60
                        hit_valid = False
                else:
                    # Too early
                    message = "Too Early!"
                    message_timer = 60
                    hit_valid = False
            elif event.key == pygame.K_p:
                show_pause()

    # Move ball
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

    # Countdown message display
    if message_timer > 0:
        message_timer -= 1
    else:
        message = ""

    # Check for game end
    if balls_left == 0 and running:
        result_text = "You Win!" if score >= target else "You Lose!"
        if score >= target:
            cheer_sound.play()
        end_msg = big_font.render(result_text, True, RED)
        screen.blit(end_msg, (WIDTH // 2 - end_msg.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
