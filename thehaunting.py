import pygame
import sys
import random
import time
import os

pygame.init()
pygame.mixer.init()

# Fullscreen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("The Haunting - Fullscreen")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (100, 0, 0)
PURPLE = (120, 0, 120)

# Fonts
font_big = pygame.font.SysFont('Arial', 64)
font_med = pygame.font.SysFont('Arial', 42)
font_small = pygame.font.SysFont('Arial', 32)

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
def safe_path(filename): 
    return os.path.join(script_dir, filename)

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"Failed to load sound: {path}")
        return None

screech = load_sound(safe_path("screech.mp3"))
heartbeat = load_sound(safe_path("heartbeat.mp3"))
creak = load_sound(safe_path("creak.mp3"))

def draw_text_center(text, font, color, y_ratio):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen_width // 2, int(screen_height * y_ratio)))
    screen.blit(surface, rect)

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def flash_screen(times=10, speed=50):
    colors = [RED, BLACK, WHITE, DARK_RED, PURPLE]
    for _ in range(times):
        screen.fill(random.choice(colors))
        pygame.display.flip()
        pygame.time.delay(speed)

def jumpscare():
    if screech:
        screech.play()
    if heartbeat:
        heartbeat.play(-1)  # loop heartbeat

    for i in range(30):
        color = RED if i % 2 == 0 else BLACK
        screen.fill(color)
        jitter_x = random.randint(-15, 15)
        jitter_y = random.randint(-15, 15)

        text_surface = font_big.render("YOU'RE DEAD", True, RED)
        rect = text_surface.get_rect(center=(screen_width // 2 + jitter_x, screen_height // 2 + jitter_y))
        screen.blit(text_surface, rect)

        pygame.display.flip()
        pygame.time.delay(50)

    if heartbeat:
        heartbeat.stop()

    screen.fill(BLACK)
    final_surface = font_big.render("YOU'RE DEAD", True, RED)
    final_rect = final_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(final_surface, final_rect)
    pygame.display.flip()
    pygame.time.delay(4000)

def creepy_text(text, delay=2000):
    screen.fill(BLACK)
    draw_text_center(text, font_med, RED, 0.5)
    pygame.display.flip()
    pygame.time.delay(delay)

def choice_prompt(choices):
    screen.fill(BLACK)
    draw_text_center("Make a choice:", font_med, WHITE, 0.15)
    for i, (text, _) in enumerate(choices):
        draw_text_center(f"{i + 1}. {text}", font_small, WHITE, 0.25 + i * 0.07)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(choices):
                        return choices[idx][1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def random_jumpscare_chance(chance=0.1):
    if random.random() < chance:
        jumpscare()

# Story functions
def hallway():
    creepy_text("You stand in a dark, narrow hallway. The air is thick and cold...")
    random_jumpscare_chance(0.2)

    func = choice_prompt([
        ("Open the door to the left", door_left),
        ("Open the door to the right", door_right),
        ("Walk forward into the darkness", walk_forward),
    ])
    func()

def door_left():
    creepy_text("You open the left door. A faint whisper calls your name...")
    random_jumpscare_chance(0.3)

    func = choice_prompt([
        ("Enter the room", room_left_inside),
        ("Close the door and go back", hallway),
    ])
    func()

def door_right():
    creepy_text("You open the right door. It's empty... or is it?")
    random_jumpscare_chance(0.25)

    func = choice_prompt([
        ("Search the room", search_right_room),
        ("Close the door and go back", hallway),
    ])
    func()

def walk_forward():
    creepy_text("You venture deeper down the hall. The walls seem to close in...")
    random_jumpscare_chance(0.35)

    func = choice_prompt([
        ("Keep walking", deep_hallway),
        ("Run back", hallway),
    ])
    func()

def room_left_inside():
    creepy_text("The room is filled with old portraits whose eyes seem to follow you.")
    if creak:
        creak.play()
    pygame.time.delay(1500)
    random_jumpscare_chance(0.4)

    func = choice_prompt([
        ("Touch one of the portraits", portrait_touch),
        ("Leave the room", hallway),
    ])
    func()

def search_right_room():
    creepy_text("You find a dusty diary on the floor.")
    pygame.time.delay(1000)
    random_jumpscare_chance(0.3)

    func = choice_prompt([
        ("Read the diary", read_diary),
        ("Ignore it and leave", hallway),
    ])
    func()

def deep_hallway():
    creepy_text("The darkness is overwhelming. You hear footsteps behind you...")
    random_jumpscare_chance(0.5)

    func = choice_prompt([
        ("Turn around", turn_around),
        ("Keep walking", lost_in_darkness),
    ])
    func()

def portrait_touch():
    creepy_text("As you touch the portrait, the eyes bleed red!")
    jumpscare()
    game_over()

def read_diary():
    creepy_text("The diary reveals the house’s dark past... Madness and murder.")
    pygame.time.delay(2000)
    random_jumpscare_chance(0.3)

    func = choice_prompt([
        ("Keep reading", diary_continued),
        ("Put it down and leave", hallway),
    ])
    func()

def diary_continued():
    creepy_text("You feel a cold hand on your shoulder.")
    jumpscare()
    game_over()

def turn_around():
    creepy_text("Nothing but shadows. You feel your heartbeat in your ears.")
    pygame.time.delay(1500)
    random_jumpscare_chance(0.4)

    func = choice_prompt([
        ("Call out", call_out),
        ("Run forward", lost_in_darkness),
    ])
    func()

def call_out():
    creepy_text("A whisper responds: 'Leave now...'")
    random_jumpscare_chance(0.3)

    func = choice_prompt([
        ("Listen and leave", hallway),
        ("Ignore and explore further", lost_in_darkness),
    ])
    func()

def lost_in_darkness():
    creepy_text("You stumble and fall... The darkness consumes you.")
    jumpscare()
    game_over()

def game_over():
    creepy_text("GAME OVER", delay=4000)
    pygame.quit()
    sys.exit()

def game_won():
    creepy_text("You escaped the haunted house... for now.", delay=4000)
    pygame.quit()
    sys.exit()

def main():
    start_time = time.time()
    duration_seconds = 1800  # 30 minutes
    end_time = start_time + duration_seconds

    hallway()

    while True:
        if time.time() >= end_time:
            game_won()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)

if __name__ == "__main__":
    main()
