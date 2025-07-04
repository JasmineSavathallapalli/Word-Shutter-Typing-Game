import pygame
import random
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Shutter Typing Game")
clock = pygame.time.Clock()

WHITE = (240, 240, 240)
RED = (255, 60, 60)
YELLOW = (255, 200, 0)
ACCENT = (0, 150, 255)

font_large = pygame.font.Font(None, 52)
font_medium = pygame.font.Font(None, 36)

try:
    correct_sound = pygame.mixer.Sound("correct.wav")
    error_sound = pygame.mixer.Sound("error.wav")
except FileNotFoundError:
    pass

word_list = [
    "python", "game", "typing", "code", "shooter", "keyboard", "project",
    "function", "loop", "array", "class", "object", "string", "input",
    "compile", "binary", "syntax", "debug", "network", "screen", "random",
    "logic", "buffer", "static", "global", "import", "method", "event",
    "render", "score", "level", "pygame", "module", "script", "thread",
    "timer", "index", "cursor", "execute", "boolean", "display", "design"
]
random.shuffle(word_list)
last_word = None

active_words = []
current_input = ""
score = 0
high_score = 0
game_over = False
level = 1
base_speed = 1.0
explosions = []

def draw_gradient_background():
    for i in range(HEIGHT):
        r = 20
        g = 20
        b = 40 + int((i / HEIGHT) * 60)
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

def spawn_word():
    global last_word
    while True:
        word = random.choice(word_list)
        if word != last_word:
            break
    last_word = word
    x = random.randint(50, WIDTH - 200)
    y = 0
    speed = random.uniform(base_speed, base_speed + 2)
    active_words.append({"text": word, "x": x, "y": y, "speed": speed})

def create_explosion(x, y):
    for _ in range(10):
        explosions.append({
            "x": x + random.randint(-20, 20),
            "y": y + random.randint(-20, 20),
            "vx": random.uniform(-2, 2),
            "vy": random.uniform(-5, 0),
            "life": 30
        })

running = True
while running:
    draw_gradient_background()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if game_over:
                if event.key == K_RETURN:
                    game_over = False
                    score = 0
                    level = 1
                    base_speed = 1.0
                    active_words = []
            else:
                if event.key == K_RETURN:
                    matched = False
                    for word in active_words[:]:
                        if current_input == word["text"]:
                            active_words.remove(word)
                            score += 10
                            matched = True
                            create_explosion(word["x"], word["y"] + 10)
                            if 'correct_sound' in locals():
                                correct_sound.play()
                    if not matched and 'error_sound' in locals():
                        error_sound.play()
                    current_input = ""
                elif event.key == K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    current_input += event.unicode.lower()

    if not game_over:
        if score // 50 >= level:
            level += 1
            base_speed *= 1.15

        if random.randint(1, 100) < 2 + level:
            spawn_word()

        for word in active_words:
            word["y"] += word["speed"]
            if word["y"] > HEIGHT:
                game_over = True

        for explosion in explosions[:]:
            explosion["x"] += explosion["vx"]
            explosion["y"] += explosion["vy"]
            explosion["life"] -= 1
            if explosion["life"] <= 0:
                explosions.remove(explosion)

        for word in active_words:
            text_surface = font_medium.render(word["text"], True, WHITE)
            screen.blit(text_surface, (word["x"], word["y"]))

        for explosion in explosions:
            pygame.draw.circle(screen, YELLOW, 
                (int(explosion["x"]), int(explosion["y"])), 
                int(explosion["life"] / 6))

        input_surface = font_medium.render(f"Type: {current_input}", True, ACCENT)
        screen.blit(input_surface, (40, HEIGHT - 60))
        score_surface = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (WIDTH - 180, 30))
        level_surface = font_medium.render(f"Level: {level}", True, WHITE)
        screen.blit(level_surface, (40, 30))
    else:
        if score > high_score:
            high_score = score

        game_over_text = font_large.render("Game Over! Press Enter to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 270, HEIGHT//2 - 50))
        final_score = font_medium.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 + 20))
        high_score_surface = font_medium.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(high_score_surface, (WIDTH//2 - 100, HEIGHT//2 + 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
