import pygame
import random


# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
PIZZA_SIZE = 30
FPS = 60
TOTAL_PIZZAS = 1000
THIEF_MAX_HEALTH = 100
THIEF_DAMAGE_PER_FRAME = 0.3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THIEF_COLOR = (255, 200, 0)
COP_COLOR = (0, 100, 255)
PIZZA_COLOR = (255, 0, 0)

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Thief")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load and play background music
pygame.mixer.music.load("Minecraftsong.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

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

# Main game loop
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
        if keys[pygame.K_w]: thief.y -= 4
        if keys[pygame.K_s]: thief.y += 4
        if keys[pygame.K_a]: thief.x -= 4
        if keys[pygame.K_d]: thief.x += 4

        # Movement - Cop (Arrow Keys)
        if keys[pygame.K_UP]: cop.y -= 4
        if keys[pygame.K_DOWN]: cop.y += 4
        if keys[pygame.K_LEFT]: cop.x -= 4
        if keys[pygame.K_RIGHT]: cop.x += 4

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

    # Draw players
    pygame.draw.rect(screen, THIEF_COLOR, thief)
    pygame.draw.rect(screen, COP_COLOR, cop)

    # Draw pizzas
    for pizza in pizzas:
        pygame.draw.rect(screen, PIZZA_COLOR, pizza)

    # UI
    score_text = font.render(f"Pizzas: {thief_score}/{TOTAL_PIZZAS}", True, BLACK)
    health_text = font.render(f"Thief Health: {int(thief_health)}%", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(health_text, (20, 60))

    # Win Message
    if game_over:
        msg = font.render(winner, True, (0, 150, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
