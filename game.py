import pygame
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600  # Smaller resolution

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 128)
TRANSLUCENT_WHITE = (255, 255, 255, 200)

FONT = pygame.font.Font(None, 100)
BUTTON_FONT = pygame.font.Font(None, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Windowed mode
pygame.display.set_caption("Bubble Typing Game")

FPS = 60
clock = pygame.time.Clock()

bubble_image_path = os.path.join(os.path.dirname(__file__), "bubble.png")
try:
    bubble_image = pygame.image.load(bubble_image_path)
    bubble_image = pygame.transform.scale(bubble_image, (150, 150))
except pygame.error:
    print(f"Error: Could not load 'bubble.png' from {bubble_image_path}")
    pygame.quit()
    sys.exit()

background_image_path = os.path.join(os.path.dirname(__file__), "bg.jpg")
try:
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    print(f"Error: Could not load 'bg.jpg' from {background_image_path}")
    pygame.quit()
    sys.exit()

class Bubble:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.image = pygame.transform.scale(bubble_image, (150, 150))
        self.speed = random.uniform(1.5, 3.5)
        self.popping = False
        self.pop_frame = 0

    def draw(self):
        if not self.popping:
            screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
            text_surface = FONT.render(self.letter, True, WHITE)
            text_surface.set_alpha(200)
            screen.blit(text_surface, (self.x - text_surface.get_width() // 2, self.y - text_surface.get_height() // 2))
        else:
            if self.pop_frame < 10:
                pop_size = 150 + self.pop_frame * 10
                pop_image = pygame.transform.scale(self.image, (pop_size, pop_size))
                screen.blit(pop_image, (self.x - pop_image.get_width() // 2, self.y - pop_image.get_height() // 2))
                self.pop_frame += 1

    def move(self):
        if not self.popping:
            self.y += self.speed

    def pop(self):
        self.popping = True

def draw_menu():
    screen.blit(background_image, (0, 0))
    title = FONT.render("Bubble Typing Game", True, WHITE)
    title.set_alpha(200)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    close_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

    pygame.draw.rect(screen, TRANSPARENT_BLACK, start_button)
    pygame.draw.rect(screen, TRANSPARENT_BLACK, close_button)

    start_text = BUTTON_FONT.render("Start", True, WHITE)
    start_text.set_alpha(200)
    close_text = BUTTON_FONT.render("Close", True, WHITE)
    close_text.set_alpha(200)

    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2 - 50))
    screen.blit(close_text, (WIDTH // 2 - close_text.get_width() // 2, HEIGHT // 2 - close_text.get_height() // 2 + 20))

    pygame.display.flip()
    return start_button, close_button

def main_game():
    global WIDTH, HEIGHT, screen, background_image
    bubbles = []
    score = 0

    ADD_BUBBLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_BUBBLE, 1000)

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ADD_BUBBLE:
                x = random.randint(50, WIDTH - 50)
                y = -50
                letter = chr(random.randint(65, 90))
                bubbles.append(Bubble(x, y, letter))
            if event.type == pygame.KEYDOWN:
                for bubble in bubbles:
                    if event.unicode.upper() == bubble.letter:
                        bubble.pop()
                        score += 1
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                background_image = pygame.transform.scale(pygame.image.load(background_image_path), (WIDTH, HEIGHT))

        for bubble in bubbles[:]:
            if bubble.popping and bubble.pop_frame >= 10:
                bubbles.remove(bubble)
            else:
                bubble.move()
                bubble.draw()
                if bubble.y - bubble.image.get_height() > HEIGHT:
                    running = False

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        score_text.set_alpha(200)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    running = True
    while running:
        start_button, close_button = draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main_game()
                if close_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
