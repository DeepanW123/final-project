import os
import pygame
import pickle
from objects import Player
from gardens import garden

def main():
    player = select_player() #gets the player object if it exists
    new_player = garden(player, True) #runs the garden function with that player and recieves the player object with all the new things the user has done
    save_user(new_player) #saves the new player object

def select_player():
    """Prompts the user to input their username and password then handles the logic accordingly,
      returns the player object if everything is well"""
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHTER_COOLGREEN = (194, 252, 194)
    DEEPGREEN = (6, 64, 43)
    BUTTON_COLOR = (100, 200, 100)
    GRAYGREEN = (143 ,151, 121)

    pygame.init()
    pygame.key.set_repeat(400, 30)

    # Screen dimensions
    S_HEIGHT = 700
    S_WIDTH = 900

    # Fonts
    font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 20)
    heading_font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 30)

    # Input fields
    username = ""
    password = ""
    active_box = None
    error_message = ""

    user_box = pygame.Rect(S_WIDTH//2 - 200, S_HEIGHT//2 - 30, 400, 40)
    password_box = pygame.Rect(S_WIDTH//2 - 200, S_HEIGHT//2 + 30, 400, 40)

    login_button = pygame.Rect(S_WIDTH//2 - 200, S_HEIGHT//2 + 100, 180, 40)
    create_button = pygame.Rect(S_WIDTH//2 + 20, S_HEIGHT//2 + 100, 180, 40)

    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    clock = pygame.time.Clock()

    not_selected = True

    while not_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if user_box.collidepoint(event.pos):
                    active_box = "username"
                elif password_box.collidepoint(event.pos):
                    active_box = "password"
                elif login_button.collidepoint(event.pos):
                    player, code = user_check(username, password)
                    if player:
                        return player
                    else:
                        error_message = code
                        username = ""
                        password = ""
                        active_box = None
                elif create_button.collidepoint(event.pos):
                    if username and password:
                        _, msg = create_new_user(username, password)
                        error_message = msg
                        username = ""
                        password = ""
                        active_box = None
                    else:
                        error_message = "Please enter both a username and password to create a new user."

            elif event.type == pygame.KEYDOWN:
                if active_box == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_box = "password"
                    else:
                        username += event.unicode
                elif active_box == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        player, code = user_check(username, password)
                        if player:
                            return player
                        else:
                            error_message = code
                            username = ""
                            password = ""
                            active_box = None
                    else:
                        password += event.unicode

        screen.fill(LIGHTER_COOLGREEN)

        # Error message at top
        if error_message:
            error_surface = font.render(error_message, True, GRAYGREEN)
            screen.blit(error_surface, (S_WIDTH // 2 - error_surface.get_width() // 2, 30))

        # Heading
        heading_surface = heading_font.render("Enter your garden", True, DEEPGREEN)
        screen.blit(heading_surface, (
            S_WIDTH // 2 - heading_surface.get_width() // 2,
            S_HEIGHT // 2 - 100
        ))

        # Draw input boxes
        pygame.draw.rect(screen, WHITE, user_box, border_radius=10)
        pygame.draw.rect(screen, WHITE, password_box, border_radius=10)

        # Username text
        if username or active_box == "username":
            username_surface = font.render(username, True, DEEPGREEN)
        else:
            username_surface = font.render("Username", True, (150, 180, 150))

        # Password text
        password_mask = "*" * len(password)
        if password or active_box == "password":
            password_surface = font.render(password_mask, True, DEEPGREEN)
        else:
            password_surface = font.render("Password", True, (150, 180, 150))

        screen.blit(username_surface, (user_box.x + 10, user_box.y + 5))
        screen.blit(password_surface, (password_box.x + 10, password_box.y + 5))

        # Draw buttons
        pygame.draw.rect(screen, BUTTON_COLOR, login_button, border_radius=8)
        pygame.draw.rect(screen, BUTTON_COLOR, create_button, border_radius=8)

        login_text = font.render("Enter", True, BLACK)
        create_text = font.render("Create", True, BLACK)

        screen.blit(login_text, (
            login_button.x + login_button.width // 2 - login_text.get_width() // 2,
            login_button.y + 5
        ))
        screen.blit(create_text, (
            create_button.x + create_button.width // 2 - create_text.get_width() // 2,
            create_button.y + 5
        ))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def user_check(username, password):
    """checks if the user exists, returns the player object if the user exists and the password is correct
     returns Flase and an error message otherwise """
    
    filename = username + ".pkl"
    check = os.path.exists("users/" + filename)
    if check:
        with open("users/" + filename, "rb") as file:
            player = pickle.load(file)
            if player.password == password:
                return player, "Logging in!"
            else:
                return False, "Incorrect Password. Please try again!"
    else:
        return False, "User doesn't exist. Please try again or create a new one."
    
def create_new_user(username, password):
    """Creates a new user"""
    filename = username + ".pkl"
    filepath = "users/" + filename

    # Check if user already exists
    if os.path.exists(filepath):
        return False, "User already exists. Please choose a different username."

    # Create new player and save to file
    player = Player(username, password)
    with open(filepath, "wb") as file:
        pickle.dump(player, file)

    return True, "New user created! Please login now."

def save_user(player):
    """Saves all the progress of a user"""
    filename = f"users/{player.username}.pkl"
    with open(filename, "wb") as file:
        pickle.dump(player, file)

main()