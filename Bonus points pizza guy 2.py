import pygame
import sys
import random

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

# Load assets
delivery_sound = pygame.mixer.Sound("delivery.mp3")
pizza_bike_original = pygame.image.load("pizza_bike.png")
pizza_bike_original = pygame.transform.scale(pizza_bike_original, (55, 55))
pizza_bike_up = pizza_bike_original
pizza_bike_down = pygame.transform.rotate(pizza_bike_original, 180)
pizza_bike_left = pygame.transform.rotate(pizza_bike_original, 90)
pizza_bike_right = pygame.transform.rotate(pizza_bike_original, -90)
pizza_bike_image = pizza_bike_right
house_image = pygame.image.load("house.png")
house_image = pygame.transform.scale(house_image, (90, 90))

# Fonts
font = pygame.font.SysFont(None, 24)
large_font = pygame.font.SysFont(None, 48)

# Roads
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

def spawn_houses_on_roads(num_houses):
    positions = []
    attempts = 0
    while len(positions) < num_houses and attempts < 1000:
        road = random.choice(roads)
        x = random.randint(road.left, road.right - 30)
        y = random.randint(road.top, road.bottom - 30)
        house_rect = pygame.Rect(x, y, 30, 30)
        if all(not house_rect.colliderect(existing) for existing in positions):
            positions.append(house_rect)
        attempts += 1
    return positions

def game_loop():
    global pizza_bike_image

    player = pygame.Rect(110, 110, 20, 20)
    player_speed = 4
    fuel = 100
    houses = spawn_houses_on_roads(7)
    house_states = [0] * len(houses)
    house_alpha = [255] * len(houses)

    running = True
    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

            if not any(player.colliderect(road) for road in roads):
                player = old_position
                moved = False

        if moved:
            fuel = max(fuel - 0.20, 0)

        for i, house in enumerate(houses):
            if house_states[i] == 0 and player.colliderect(house):
                house_states[i] = 1
                delivery_sound.play()

        screen.fill((180, 230, 180))

        for road in roads:
            pygame.draw.rect(screen, DARK_GRAY, road)

        for i, house in enumerate(houses):
            if house_states[i] < 2:
                if house_states[i] == 1:
                    house_alpha[i] = max(house_alpha[i] - 5, 0)
                    if house_alpha[i] == 0:
                        house_states[i] = 2

                faded_image = house_image.copy()
                faded_image.set_alpha(house_alpha[i])
                screen.blit(faded_image, house.topleft)

        screen.blit(pizza_bike_image, (player.x, player.y))
        pygame.draw.rect(screen, GRAY, (20, 20, 100, 10))
        pygame.draw.rect(screen, GREEN, (20, 20, fuel, 10))

        delivered_count = sum(1 for state in house_states if state == 2)
        text = font.render(f"Deliveries: {delivered_count}/{len(houses)}", True, BLACK)
        screen.blit(text, (20, 40))

        if fuel <= 0 and delivered_count < len(houses):
            msg = "Out of fuel! Game Over."
            screen.blit(font.render(msg, True, BLACK), (20, 70))
            pygame.display.flip()
            pygame.time.wait(1500)
            return

        if delivered_count == len(houses):
            msg = "All pizzas delivered! You win!"
            screen.blit(font.render(msg, True, BLACK), (20, 70))
            pygame.display.flip()
            pygame.time.wait(1500)
            return

        pygame.display.flip()

def show_menu():
    while True:
        screen.fill(WHITE)
        title = large_font.render("Pizza Delivery Game", True, BLUE)
        play_text = font.render("Press ENTER to Play", True, GREEN)
        quit_text = font.render("Press ESC to Quit", True, RED)
        desc1 = font.render("Deliver the pizzas to the backdoor of the houses.", True, BLACK)
        desc2 = font.render("Be careful with the invisible obstacles on the road!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 300))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 340))
        screen.blit(desc1, (WIDTH // 2 - desc1.get_width() // 2, 390))
        screen.blit(desc2, (WIDTH // 2 - desc2.get_width() // 2, 420))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Main loop
while True:
    if show_menu():
        game_loop()



