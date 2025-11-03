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

bg_image = pygame.image.load("assets/background.png")
bg2_image = pygame.image.load("assets/background2.png")
button_image = pygame.image.load("assets/button2.png")
button_pressed_image = pygame.image.load("assets/button_pressed.png")
category_button = pygame.image.load("assets/category_button.png")
category_button_pressed = pygame.image.load("assets/category_button_pressed.png")
play_button_image = pygame.image.load("assets/base.png")
petal_image = pygame.image.load("assets/petal.png")
life_image = pygame.image.load("assets/life.png")
hint_button_image = pygame.image.load("assets/button.png")
hint_button_image = pygame.transform.scale(hint_button_image, (120, 48))
font = pygame.font.Font("assets/Gluten-light.ttf", 32)

clock = pygame.time.Clock()
current_frame = "main_menu"

player_life = 6
user_points = 0


# ---------------------------------- #
# -------- Helper functions -------- #
# ---------------------------------- #
def create_letter_buttons():
    letters = []
    rows_counts = [9, 9, 8]
    button_w = constants.DIAMETER * 2
    button_h = button_w
    spacing = constants.GAP
    starty = 378
    A = 65
    idx = 0
    for r, count in enumerate(rows_counts):
        total_width = count * button_w + (count - 1) * spacing
        startx = round((constants.WINDOW_WIDTH - total_width) / 2)
        y = starty + r * (button_h + spacing)
        for c in range(count):
            if idx >= 26:
                break
            x = startx + c * (button_w + spacing)
            letters.append({"x": x, "y": y, "pressed": False, "letter": chr(A + idx)})
            idx += 1
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
    starty = (constants.WINDOW_HEIGHT - total_height) // 2 + 20

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
images = []
for i in range(1, 7):
    image = pygame.image.load("assets/flower" + str(i) + ".png")
    images.append(image)

flower_status = 0


def draw_main_menu(buttons):
    window.blit(bg_image, (0, 0))
    window.blit(play_button_image, (play_buttonx, play_buttony))
    text = font.render("Play", True, constants.BLACK)
    btn_rect = play_button_image.get_rect(topleft=(play_buttonx, play_buttony))
    text_rect = text.get_rect(center=btn_rect.center)
    window.blit(text, text_rect)
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
    life_x = 40
    window.blit(life_image, (life_x, 50))
    window.blit(life, (life_x + life_image.get_width() + 8, 50))
    petal_w = petal_image.get_width()
    petal_x = 115
    window.blit(petal_image, (petal_x, 50))
    window.blit(points, (petal_x + petal_w + 8, 50))


def draw_game_screen(letters):
    window.blit(bg2_image, (0, 0))
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

    if images:
        img = images[flower_status]
        img_rect = img.get_rect(center=(constants.WINDOW_WIDTH // 2, 150))
        window.blit(img, img_rect)

    hint_w, hint_h = hint_button_image.get_size()
    hint_x = constants.WINDOW_WIDTH - hint_w - 20
    hint_y = 20
    hint_rect = hint_button_image.get_rect(topleft=(hint_x, hint_y))
    window.blit(hint_button_image, (hint_x, hint_y))
    hint_text = font.render("Hint", True, constants.BLACK)
    hint_text_rect = hint_text.get_rect(center=hint_rect.center)
    window.blit(hint_text, hint_text_rect)


def draw_user_input(chosen_word, letter_occurrences):
    spacing = 50
    slots = len(chosen_word)
    total_width = slots * spacing
    x_start = (constants.WINDOW_WIDTH - total_width) // 2
    y_underscore = constants.WINDOW_HEIGHT // 2 + 20
    y_letter = y_underscore - 10

    for i, letter in enumerate(chosen_word):
        x = x_start + i * spacing
        if letter.isalpha():
            underscore = font.render("_", True, (0, 0, 0))
            underscore_rect = underscore.get_rect(
                center=(x + spacing // 2, y_underscore)
            )
            window.blit(underscore, underscore_rect)

            if (
                letter.lower() in letter_occurrences
                and letter_occurrences[letter.lower()]
            ):
                text = font.render(letter.upper(), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + spacing // 2, y_letter))
                window.blit(text, text_rect)
        else:
            space = font.render(" ", True, (0, 0, 0))
            space_rect = space.get_rect(center=(x + spacing // 2, y_underscore))
            window.blit(space, space_rect)


def draw_end_screen(result, chosen_word):
    window.blit(bg_image, (0, 0))

    if result == "lose":
        text = font.render(f"You Lose! Word: {chosen_word.upper()}", True, (200, 0, 0))

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
    global current_frame, player_life, user_points, flower_status
    letters = create_letter_buttons()
    menu_buttons = create_category_buttons()
    run = True
    chosen_word = ""
    letter_occurrences = {}
    game_result = "playing"
    categories = []

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
                        player_life = 6
                        user_points = 0
                        flower_status = 0
                        game_result = "playing"

                    for btn in menu_buttons:
                        btn_rect = category_button.get_rect(
                            topleft=(btn["x"], btn["y"])
                        )
                        if btn_rect.collidepoint(pos):
                            btn["pressed"] = not btn["pressed"]

                elif current_frame == "game" and game_result == "playing":
                    hint_w, hint_h = hint_button_image.get_size()
                    hint_rect = hint_button_image.get_rect(
                        topleft=(constants.WINDOW_WIDTH - hint_w - 20, 20)
                    )
                    if hint_rect.collidepoint(pos):
                        if user_points >= 20 and letter_occurrences:
                            unguessed = [
                                l for l, v in letter_occurrences.items() if not v
                            ]
                            if unguessed:
                                chosen_letter = random.choice(unguessed)
                                letter_occurrences[chosen_letter] = True
                                user_points -= 20
                                for btn in letters:
                                    if btn["letter"].lower() == chosen_letter:
                                        btn["pressed"] = True
                                        break
                                game_result = check_game_state(
                                    letter_occurrences, player_life
                                )
                                if game_result == "win":
                                    user_points += player_life * 10
                                    chosen_word, letter_occurrences = game_logic(
                                        categories
                                    )
                                    letters = create_letter_buttons()
                                    player_life = 6
                                    flower_status = 0
                                    game_result = "playing"
                        continue

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
                                flower_status = min(flower_status + 1, len(images) - 1)

                    game_result = check_game_state(letter_occurrences, player_life)
                    if game_result == "win":
                        user_points += player_life * 10
                        chosen_word, letter_occurrences = game_logic(categories)
                        letters = create_letter_buttons()
                        player_life = 6
                        flower_status = 0
                        game_result = "playing"

                elif current_frame == "game" and game_result in ("win", "lose"):
                    if game_result == "win":
                        chosen_word, letter_occurrences = game_logic(categories)
                        letters = create_letter_buttons()
                        player_life = 6
                        flower_status = 0
                        game_result = "playing"
                    else:
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
