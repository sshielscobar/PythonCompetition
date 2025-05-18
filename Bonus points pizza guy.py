from xml.dom import registerDOMImplementation

import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Delivery Game")

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_GRAY = (100, 100, 100)

# Clock
clock = pygame.time.Clock()

# Load delivery sound
delivery_sound = pygame.mixer.Sound("delivery.mp3")  # Replace with your sound file name

# Load pizza bike image (facing right as default)
pizza_bike_original = pygame.image.load("pizza_bike.png")
pizza_bike_original = pygame.transform.scale(pizza_bike_original, (55, 55))

# Create direction versions
pizza_bike_up = pizza_bike_original
pizza_bike_down = pygame.transform.rotate(pizza_bike_original, 180)
pizza_bike_left = pygame.transform.rotate(pizza_bike_original, 90)
pizza_bike_right = pygame.transform.rotate(pizza_bike_original, -90)

# Start with right-facing image
pizza_bike_image = pizza_bike_right

# Load house image
house_image = pygame.image.load("house.png")  # Replace with your actual file name
house_image = pygame.transform.scale(house_image, (90, 90))  # Resize to match house rect size

# Roads - more complex maze with diagonal paths (approximate with rotated rectangles not supported by pygame.draw.rect)
roads = [
    pygame.Rect(0, 100, 800, 30),
    pygame.Rect(0, 300, 800, 30),
    pygame.Rect(0, 500, 800, 30),
    pygame.Rect(100, 0, 30, 600),
    pygame.Rect(300, 0, 30, 600),
    pygame.Rect(500, 0, 30, 600),
    pygame.Rect(700, 0, 30, 600),
    pygame.Rect(200, 200, 400, 30),
    pygame.Rect(400, 400, 30, 200),
    pygame.Rect(150, 150, 30, 200),
    pygame.Rect(550, 350, 200, 30),
    pygame.Rect(650, 150, 30, 200),
    pygame.Rect(350, 100, 30, 150),
    pygame.Rect(250, 400, 200, 30),
    pygame.Rect(100, 250, 150, 30),
    pygame.Rect(600, 250, 150, 30)
]

# Pizza guy - start on a road
player = pygame.Rect(110, 110, 20, 20)  # Inside first horizontal and vertical road intersection
player_speed = 4
fuel = 100

# Houses - now increased and placed on roads
houses = [
    pygame.Rect(600, 105, 30, 30),  # on first horizontal road
    pygame.Rect(200, 305, 30, 30),  # on second horizontal road
    pygame.Rect(500, 505, 30, 30),  # on third horizontal road
    pygame.Rect(150, 255, 30, 30),  # on small crossroad
    pygame.Rect(650, 355, 30, 30),  # right maze arm
    pygame.Rect(300, 405, 30, 30),  # lower left maze
    pygame.Rect(700, 255, 30, 30)   # right-top path
]
# 0 = visible, 1 = fading, 2 = fully delivered
house_states = [0] * len(houses)
house_alpha = [255] * len(houses)

# Obstacles removed
obstacles = []

font = pygame.font.SysFont(None, 24)

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moved = False

    if fuel > 0:
        old_position = player.copy()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
            pizza_bike_image = pizza_bike_left
            moved = True
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
            pizza_bike_image = pizza_bike_right
            moved = True
        if keys[pygame.K_UP]:
            player.y -= player_speed
            pizza_bike_image = pizza_bike_up
            moved = True
        if keys[pygame.K_DOWN]:
            player.y += player_speed
            pizza_bike_image = pizza_bike_down
            moved = True

        # Player must stay on roads
        if not any(player.colliderect(road) for road in roads):
            player = old_position
            moved = False

    if moved:
        fuel = max(fuel - 0.26, 0)

    for i, house in enumerate(houses):
        if house_states[i] == 0 and player.colliderect(house):
            house_states[i] = 1  # Start fading
            delivery_sound.play()

    # Draw background
    screen.fill((180, 230, 180))  # green grass background

    # Draw roads
    for road in roads:
        pygame.draw.rect(screen, DARK_GRAY, road)

    # Draw houses with fade effect
    for i, house in enumerate(houses):
        if house_states[i] < 2:
            if house_states[i] == 1:  # Fading
                house_alpha[i] = max(house_alpha[i] - 5, 0)
                if house_alpha[i] == 0:
                    house_states[i] = 2  # Fully faded/delivered

            faded_image = house_image.copy()
            faded_image.set_alpha(house_alpha[i])
            screen.blit(faded_image, house.topleft)

    # Draw pizza guy
    screen.blit(pizza_bike_image, (player.x, player.y))


    # Draw fuel bar
    pygame.draw.rect(screen, GRAY, (20, 20, 100, 10))
    pygame.draw.rect(screen, GREEN, (20, 20, fuel, 10))

    # Draw status
    delivered_count = sum(1 for state in house_states if state == 2)
    text = font.render(f"Deliveries: {delivered_count}/{len(houses)}", True, BLACK)
    screen.blit(text, (20, 40))

    if fuel <= 0 and delivered_count < len(houses):
        game_over = font.render("Out of fuel! Game Over.", True, BLACK)
        screen.blit(game_over, (20, 70))
    if delivered_count == len(houses):
        win = font.render("All pizzas delivered! You win!", True, BLACK)
        screen.blit(win, (20, 70))

    pygame.display.flip()

pygame.quit()
sys.exit()