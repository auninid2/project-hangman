import pygame
import constants
import random
import json

# ---------------------------------- #
# -------- Initialization ---------- #
# ---------------------------------- #
pygame.init()
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Project Hangman")

bg_image = pygame.image.load("assets/Background_Blue.png")
button_image = pygame.image.load("assets/button2.png")
button_pressed_image = pygame.image.load("assets/button_pressed.png")
category_button = pygame.image.load("assets/category_button.png")
category_button_pressed = pygame.image.load("assets/category_button_pressed.png")
play_button_image = pygame.image.load("assets/base.png")
font = pygame.font.Font("assets/Gluten-light.ttf", 32)

clock = pygame.time.Clock()
current_frame = "main_menu"


# ---------------------------------- #
# -------- Helper functions -------- #
# ---------------------------------- #
def create_letter_buttons():
    letters = []
    startx = round(
        (constants.WINDOW_WIDTH - (constants.DIAMETER * 2 + constants.GAP) * 13) / 2
    )
    starty = 400
    A = 65
    for i in range(26):
        x = (
            startx
            + constants.GAP * 2
            + ((constants.DIAMETER * 2 + constants.GAP) * (i % 13))
        )
        y = starty + ((i // 13) * (constants.GAP + constants.DIAMETER * 2))
        letters.append({"x": x, "y": y, "pressed": False, "letter": chr(A + i)})
    return letters


def create_category_buttons():
    buttons = []
    cols = 3
    rows = 2
    spacing = 40
    button_w, button_h = category_button.get_size()
    categories = ["Animals", "Sports", "Food", "Cities", "Jobs", "Brands"]
    categories_pointer = 0

    total_width = cols * button_w + (cols - 1) * spacing
    total_height = rows * button_h + (rows - 1) * spacing
    startx = (constants.WINDOW_WIDTH - total_width) // 2
    starty = (constants.WINDOW_HEIGHT - total_height) // 2

    for r in range(rows):
        for c in range(cols):
            x = startx + c * (button_w + spacing)
            y = starty + r * (button_h + spacing)
            buttons.append(
                {
                    "x": x,
                    "y": y,
                    "pressed": False,
                    "label": categories[categories_pointer],
                }
            )
            categories_pointer += 1
    return buttons


def game_logic(categories):
    with open("dictionary.json", "r") as f:
        data = json.load(f)

    words = []
    for category in categories:
        if category in data:
            for entry in data[category]:
                word = list(entry.values())[0]
                words.append(word)

    chosen_word = random.choice(words)

    letter_occurrences = {
        letter.lower(): False for letter in chosen_word if letter.isalpha()
    }

    return chosen_word, letter_occurrences


play_buttonx, play_buttony = constants.WINDOW_WIDTH / 2 - 180, 50


# ---------------------------------- #
# ------- Drawing functions -------- #
# ---------------------------------- #
def draw_main_menu(buttons):
    window.blit(bg_image, (0, 0))
    window.blit(play_button_image, (play_buttonx, play_buttony))
    for btn in buttons:
        x, y, pressed, label = btn["x"], btn["y"], btn["pressed"], btn["label"]
        if pressed:
            window.blit(category_button_pressed, (x, y))
        else:
            window.blit(category_button, (x, y))

        text = font.render(label, True, constants.BLACK)
        btn_rect = category_button.get_rect(topleft=(x, y))
        text_rect = text.get_rect(center=btn_rect.center)
        window.blit(text, text_rect)

    pygame.display.update()


def draw_game_screen(letters):
    window.blit(bg_image, (0, 0))
    for letter in letters:
        x, y = letter["x"], letter["y"]
        pressed = letter["pressed"]
        ltr = letter["letter"]

        if pressed:
            window.blit(button_pressed_image, (x, y))
        else:
            window.blit(button_image, (x, y))

        text = font.render(ltr, True, constants.BLACK)
        btn_rect = button_image.get_rect(topleft=(x, y))
        text_rect = text.get_rect(center=btn_rect.center)
        window.blit(text, text_rect)

    pygame.display.update()


# ---------------------------------- #
# ----------- Main Loop ------------ #
# ---------------------------------- #
def game_loop():
    global current_frame
    letters = create_letter_buttons()
    menu_buttons = create_category_buttons()
    run = True

    while run:
        clock.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_frame == "main_menu":
                    play_button_rect = play_button_image.get_rect(
                        topleft=(play_buttonx, play_buttony)
                    )
                    if play_button_rect.collidepoint(pos):
                        current_frame = "game"

                    for btn in menu_buttons:
                        btn_rect = category_button.get_rect(
                            topleft=(btn["x"], btn["y"])
                        )
                        if btn_rect.collidepoint(pos):
                            if btn["pressed"]:
                                btn["pressed"] = False
                            else:
                                btn["pressed"] = True

                elif current_frame == "game":
                    for letter in letters:
                        btn_rect = button_image.get_rect(
                            topleft=(letter["x"], letter["y"])
                        )
                        if btn_rect.collidepoint(pos) and not letter["pressed"]:
                            letter["pressed"] = True

        if current_frame == "main_menu":
            draw_main_menu(menu_buttons)
        elif current_frame == "game":
            draw_game_screen(letters)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
