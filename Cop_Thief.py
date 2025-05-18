import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 70
PIZZA_SIZE = 70
FPS = 60
TOTAL_PIZZAS = 1000
THIEF_MAX_HEALTH = 100
THIEF_DAMAGE_PER_FRAME = 0.3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Music
def play_song(path, loop=True):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1 if loop else 0)

# High score system
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Pregame menu
def show_menu():
    while True:
        screen.blit(background_img, (0, 0))
        title = font.render("PIZZA THIEF", True, WHITE)
        prompt = font.render("Press SPACE to Start", True, WHITE)
        hs_text = font.render(f"High Score: {load_high_score()}", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 250))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Thief")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load assets
background_img = pygame.image.load("parkinglot.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

motorcycle_img = pygame.image.load("pizza_bike.png")
motorcycle_img = pygame.transform.scale(motorcycle_img, (int(0.5 * PLAYER_SIZE), PLAYER_SIZE))

helicopter_img = pygame.image.load("police_helicopter.png")
helicopter_img = pygame.transform.scale(helicopter_img, (1.2 * PLAYER_SIZE,1.5 * PLAYER_SIZE))

pizza_img = pygame.image.load("pizzathing.png")
pizza_img = pygame.transform.scale(pizza_img, (PIZZA_SIZE, PIZZA_SIZE))

# Play music
play_song("Minecraftsong.mp3")

# Show pregame menu
show_menu()

# Game state
thief = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)
cop = pygame.Rect(600, 400, PLAYER_SIZE, PLAYER_SIZE)
pizzas = []
thief_score = 0
thief_health = THIEF_MAX_HEALTH
game_over = False
winner = ""
thief_direction = 0
cop_direction = 0

def spawn_pizzas(count):
    for _ in range(count):
        x = random.randint(0, WIDTH - PIZZA_SIZE)
        y = random.randint(0, HEIGHT - PIZZA_SIZE)
        pizzas.append(pygame.Rect(x, y, PIZZA_SIZE, PIZZA_SIZE))

# Start game
running = True
spawn_pizzas(4)

while running:
    clock.tick(FPS)
    screen.blit(background_img, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Movement - Thief (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            thief.y -= 4
            thief_direction = 0
        if keys[pygame.K_s]:
            thief.y += 4
            thief_direction = 180
        if keys[pygame.K_a]:
            thief.x -= 4
            thief_direction = 90
        if keys[pygame.K_d]:
            thief.x += 4
            thief_direction = -90

        # Movement - Cop (Arrow Keys)
        if keys[pygame.K_UP]:
            cop.y -= 4
            cop_direction = 0
        if keys[pygame.K_DOWN]:
            cop.y += 4
            cop_direction = 180
        if keys[pygame.K_LEFT]:
            cop.x -= 4
            cop_direction = 90
        if keys[pygame.K_RIGHT]:
            cop.x += 4
            cop_direction = -90

        # Boundaries
        thief.clamp_ip(screen.get_rect())
        cop.clamp_ip(screen.get_rect())

        # Pizza collision
        for pizza in pizzas[:]:
            if thief.colliderect(pizza):
                pizzas.remove(pizza)
                thief_score += 1

        while len(pizzas) < 4 and thief_score < TOTAL_PIZZAS:
            spawn_pizzas(1)

        # Cop damages thief
        if cop.colliderect(thief):
            thief_health -= THIEF_DAMAGE_PER_FRAME

        # Win check
        if thief_score >= TOTAL_PIZZAS:
            winner = "Thief wins!"
            game_over = True
        elif thief_health <= 0:
            winner = "Cop wins by damage!"
            game_over = True
            if thief_score > load_high_score():
                save_high_score(thief_score)

    # Draw rotated thief and cop
    rotated_thief = pygame.transform.rotate(motorcycle_img, thief_direction)
    screen.blit(rotated_thief, rotated_thief.get_rect(center=thief.center))

    rotated_cop = pygame.transform.rotate(helicopter_img, cop_direction)
    screen.blit(rotated_cop, rotated_cop.get_rect(center=cop.center))

    # Draw pizzas
    for pizza in pizzas:
        screen.blit(pizza_img, pizza)

    # UI
    score_text = font.render(f"Pizzas: {thief_score}", True, BLACK)
    health_text = font.render(f"Thief Health: {int(thief_health)}%", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(health_text, (20, 60))

    if game_over:
        msg = font.render(winner, True, (0, 150, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
