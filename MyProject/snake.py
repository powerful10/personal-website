import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 25
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
DARK_GREEN = (0, 100, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 215, 0)

# Fonts
FONT = pygame.font.SysFont('arial', 32, True)
BIG_FONT = pygame.font.SysFont('arial', 60, True)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, pos in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=8)

def draw_food(position):
    pygame.draw.rect(screen, RED, (position[0]*CELL_SIZE, position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=8)

def draw_score(score):
    score_text = FONT.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))

def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos

def show_start_screen():
    screen.fill(BLACK)
    title = BIG_FONT.render("SNAKE GAME", True, GREEN)
    start_btn = FONT.render("START", True, WHITE, DARK_GREEN)
    btn_rect = start_btn.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(start_btn, btn_rect)
    pygame.display.flip()
    return btn_rect

def show_game_over(score):
    screen.fill(BLACK)
    over_text = BIG_FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Score: {score}", True, YELLOW)
    restart_text = FONT.render("Press R to Restart", True, WHITE)
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    pygame.display.flip()

def main():
    # Start screen
    while True:
        btn_rect = show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    game_loop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

def game_loop():
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (0, -1)
    food = random_food(snake)
    score = 0
    speed = 8  # Start slow
    grow = False
    running = True

    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check collisions
        if (new_head in snake or
            not (0 <= new_head[0] < GRID_WIDTH) or
            not (0 <= new_head[1] < GRID_HEIGHT)):
            show_game_over(score)
            wait_for_restart()
            return

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food(snake)
            speed = min(speed + 0.5, 25)  # Increase speed, max 25
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.flip()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()