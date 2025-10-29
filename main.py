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

player_life = 7
user_points = 0


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


def draw_user_info(player_life, user_points):
    life = font.render(str(player_life), True, (0, 0, 0))
    points = font.render(str(user_points), True, (0, 0, 0))
    window.blit(life, (100, 50))
    window.blit(points, (200, 50))


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


def draw_user_input(chosen_word, letter_occurrences):
    x_start = 100
    y_underscore = 200
    y_letter = 150
    spacing = 50

    for i, letter in enumerate(chosen_word):
        if letter.isalpha():
            underscore = font.render("_", True, (0, 0, 0))
            window.blit(underscore, (x_start + i * spacing, y_underscore))

            if (
                letter.lower() in letter_occurrences
                and letter_occurrences[letter.lower()]
            ):
                text = font.render(letter.upper(), True, (0, 0, 0))
                window.blit(text, (x_start + i * spacing, y_letter))
        else:
            space = font.render(" ", True, (0, 0, 0))
            window.blit(space, (x_start + i * spacing, y_underscore))


def draw_end_screen(result, chosen_word):
    window.blit(bg_image, (0, 0))

    if result == "win":
        text = font.render("You Win", True, (0, 150, 0))
    else:
        text = font.render(f"You Lose. Word: {chosen_word.upper()}", True, (200, 0, 0))

    text_rect = text.get_rect(
        center=(constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2)
    )
    window.blit(text, text_rect)

    subtext = font.render("Click anywhere to return to menu", True, (0, 0, 0))
    sub_rect = subtext.get_rect(
        center=(constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 + 80)
    )
    window.blit(subtext, sub_rect)

    pygame.display.update()


def check_game_state(letter_occurrences, player_life):
    """
    Returns "win" if all letters guessed,
    "lose" if lives are gone,
    otherwise "playing".
    """
    if all(letter_occurrences.values()):
        return "win"
    elif player_life <= 0:
        return "lose"
    else:
        return "playing"


# ---------------------------------- #
# ----------- Main Loop ------------ #
# ---------------------------------- #
def game_loop():
    global current_frame, player_life, user_points
    letters = create_letter_buttons()
    menu_buttons = create_category_buttons()
    run = True
    chosen_word = ""
    letter_occurrences = {}
    game_result = "playing"

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
                        categories = [
                            category["label"]
                            for category in menu_buttons
                            if category["pressed"]
                        ]
                        if not categories:
                            continue
                        current_frame = "game"
                        chosen_word, letter_occurrences = game_logic(categories)
                        letters = create_letter_buttons()
                        player_life = 7
                        user_points = 0
                        game_result = "playing"

                    for btn in menu_buttons:
                        btn_rect = category_button.get_rect(
                            topleft=(btn["x"], btn["y"])
                        )
                        if btn_rect.collidepoint(pos):
                            btn["pressed"] = not btn["pressed"]

                elif current_frame == "game" and game_result == "playing":
                    for letter in letters:
                        btn_rect = button_image.get_rect(
                            topleft=(letter["x"], letter["y"])
                        )
                        if btn_rect.collidepoint(pos) and not letter["pressed"]:
                            letter["pressed"] = True
                            guessed_letter = letter["letter"].lower()

                            if guessed_letter in letter_occurrences:
                                letter_occurrences[guessed_letter] = True
                                user_points += 10
                            else:
                                player_life -= 1

                    game_result = check_game_state(letter_occurrences, player_life)

                elif current_frame == "game" and game_result in ("win", "lose"):
                    current_frame = "main_menu"

        if current_frame == "main_menu":
            draw_main_menu(menu_buttons)
        elif current_frame == "game":
            if game_result == "playing":
                draw_game_screen(letters)
                draw_user_input(chosen_word, letter_occurrences)
                draw_user_info(player_life, user_points)
            else:
                draw_end_screen(game_result, chosen_word)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
