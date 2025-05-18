import pygame
import random

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

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Thief")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load images
motorcycle_img = pygame.image.load("pizza_bike.jpg")
motorcycle_img = pygame.transform.scale(motorcycle_img, (0.5 * PLAYER_SIZE, PLAYER_SIZE))

helicopter_img = pygame.image.load("police_helicopter.png")
helicopter_img = pygame.transform.scale(helicopter_img, (PLAYER_SIZE, PLAYER_SIZE))

pizza_img = pygame.image.load("pizzathing.png")
pizza_img = pygame.transform.scale(pizza_img, (PIZZA_SIZE, PIZZA_SIZE))

# Play background music
play_song("Minecraftsong.mp3")

# Player objects
thief = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)
cop = pygame.Rect(600, 400, PLAYER_SIZE, PLAYER_SIZE)

# Pizza list
pizzas = []

def spawn_pizzas(count):
    for _ in range(count):
        x = random.randint(0, WIDTH - PIZZA_SIZE)
        y = random.randint(0, HEIGHT - PIZZA_SIZE)
        pizzas.append(pygame.Rect(x, y, PIZZA_SIZE, PIZZA_SIZE))

# Game state
thief_score = 0
thief_health = THIEF_MAX_HEALTH
game_over = False
winner = ""
thief_direction = 0
cop_direction = 0

# Start game
running = True
spawn_pizzas(4)

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

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

        # Check pizza collision
        for pizza in pizzas[:]:
            if thief.colliderect(pizza):
                pizzas.remove(pizza)
                thief_score += 1

        # Spawn more pizzas if needed
        while len(pizzas) < 4 and thief_score < TOTAL_PIZZAS:
            spawn_pizzas(1)

        # Check cop damaging thief
        if cop.colliderect(thief):
            thief_health -= THIEF_DAMAGE_PER_FRAME

        # Win conditions
        if thief_score >= TOTAL_PIZZAS:
            winner = "Thief wins!"
            game_over = True
        elif thief_health <= 0:
            winner = "Cop wins by damage!"
            game_over = True

    # Draw rotating images
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

    # Win Message
    if game_over:
        msg = font.render(winner, True, (0, 150, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
