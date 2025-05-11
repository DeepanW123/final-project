from objects import Habit, Player
import datetime
import pygame
from pygame import mixer
pygame.init()
pygame.key.set_repeat(400, 30)

#screen dimensions
S_HEIGHT = 700
S_WIDTH = 900

#habit tracker system
habit_box = pygame.Rect(S_WIDTH - 510, 30, 500, S_HEIGHT - 60)
check_list_box = pygame.Rect(habit_box.x + 50, habit_box.y + 120, 400, habit_box.height - 150)
garden_box = pygame.Rect(10, 50, S_WIDTH - 530, S_HEIGHT - 110)

#font
font=pygame.font.Font("assets/font/Grand9K Pixel.ttf", 20)
heading_font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 30)
small_font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 10)
input_box = "Enter text here"

#box to enter input
input_rect = pygame.Rect(habit_box.x + 50, habit_box.y + 70, habit_box.w - 100, 35)
input_active = False

#scroll
scroll_offset = 0

#initializing the creen and the clock
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
COOLGREEN_T = (152,251,152, 180)
COOLGREEN = (152,251,152)
LIGHT_COOLGREEN = (194, 252, 194)
DEEPGREEN = (6,64,43)
GRAYGREEN = (143 ,151, 121)

running = True

#for background music
mixer.init()
mixer.music.load("assets/sound/bg_music.mp3")
mixer.music.set_volume(0.1) 
mixer.music.play(-1, fade_ms=3000)

def garden(player, running): #takes a player object as a parameter
    global input_box
    global input_active
    global scroll_offset
    test_day_count = 1

    #loads all necessary sprites, currently not that useful
    load_sprites()

    #loading assets
    bg_image = pygame.image.load("assets/bg.png")
    bg_image = pygame.transform.scale(bg_image, (S_WIDTH, S_HEIGHT))

    #updates the current day
    update_date(player)
    player.last_played = datetime.date.today()

    #main loop
    while running:

        fps = clock.tick(60)/1000 #currently not in use

        for event in pygame.event.get(): #checling for an event
            if event.type == pygame.QUIT: #quitng the loop if user quits
                running = False
            
            #checking if the user scrolled
            if event.type == pygame.MOUSEWHEEL:
                #Scroll functionality
                scroll_offset -= event.y * 40  # Scroll speed
                max_scroll = max(len(player.habits) * (10 + check_list_box.height * 0.2) - check_list_box.height + 10 , 0)
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            if event.type == pygame.MOUSEBUTTONDOWN:
                #checking if the user has input box selected
                if input_rect.collidepoint(event.pos):
                    #checks if the user has the text box selected
                    input_active = True
                    if input_box == "Enter text here":
                        input_box = ""
                else:
                    input_active = False

                # Check if a checkbox is clicked
                for habit in player.habits:
                    if habit.checkbox_rect.collidepoint(event.pos) and not habit.is_completed_today():
                        confirm = confirm_popup(habit.name) #prompting a popup
                        if confirm: 
                            if player.username == "test": #the functionality is handeled differently for a test file
                                score = habit.complete_today(datetime.timedelta(days=test_day_count))
                                player.add_score(score, habit)
                            else: #normal functionality
                                score = habit.complete_today()
                                player.add_score(score, habit)
                        break
                
                if player.username == "test" and next_day_button.collidepoint(event.pos): #there is a next day button for test file since waiting a single day for the habit to reset is not possible for demo
                    test_day_count += 1
                    for habit in player.habits:
                        habit.completed_today = False

            if event.type == pygame.KEYDOWN:
                # handles the actual input into the text box of habit section
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_box = input_box[:-1]
                    else:
                        input_box += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        entered_text = input_box[:-1]
                        if entered_text != "":
                            player.add_habit(Habit(entered_text)) #adding the habit to the player object when the user presses enter

                        input_box = ""

        screen.blit(bg_image, (0,0)) #bg image
        
        if player.username == "test": #next day button if the user is a tester
            next_day()

        garden_section(player) #runs the garden section of the code (wip)

        habit_section(player) #runs the habit section of the code
        
        pygame.display.update()

    pygame.quit()

    return player

def habit_section(player):

    # Create a transparent surface with per-pixel alpha
    transparent_surface = pygame.Surface((habit_box.width, habit_box.height), pygame.SRCALPHA)

    # Draw the filled rounded rectangle with alpha
    pygame.draw.rect(
        transparent_surface,
        COOLGREEN_T, 
        pygame.Rect(0, 0, habit_box.width, habit_box.height),
        border_radius=15
    )

    # Blit the rounded rect surface onto the main screen
    screen.blit(transparent_surface, habit_box.topleft)

    #black border around the green box
    pygame.draw.rect(screen, BLACK, habit_box, width=1, border_radius=15)

    heading = heading_font.render("Your Habits", True, WHITE)

    # Center heading inside the habit box
    heading_x = habit_box.x + (habit_box.width - heading.get_width()) // 2
    screen.blit(heading, (heading_x, habit_box.y + 10))

    #checklist box
    pygame.draw.rect(screen, LIGHT_COOLGREEN, check_list_box, border_radius= 15)
    show_checklist(scroll_offset, player)

    habit_input()

def show_checklist(offset, player):
    """Displays the entire checklist of habits the user has entered in it's proper position,
    has scroll functionality when all the habits cant be displayed at the same time"""
    y_offset = check_list_box.y + 10 - offset  # start a little inside the box
    line_spacing = 10  # space between habits

    screen.set_clip(pygame.Rect(check_list_box.x, check_list_box.y + 2, check_list_box.width, check_list_box.height - 4))  # Prevent drawing outside the checklist box
    for habit in player.habits:      
        y_offset = checklist_element(habit, y_offset)
        y_offset += line_spacing

    screen.set_clip(None)
    draw_fade_edges(player)

def checklist_element(habit, y_offset):
    """Draws the individual box for a habit with all it's constituent elements"""
    start_date = small_font.render("start: " + str(habit.start_date), True, GRAYGREEN)
    last_completed =  small_font.render("last done: " + str(habit.last_completed), True, GRAYGREEN)
    days_completed =  small_font.render("Days Completed: " + str(habit.days_completed), True, GRAYGREEN)

    container_rect = pygame.Rect(check_list_box.x + 10,
                                 y_offset,
                                 check_list_box.width - 20,
                                 check_list_box.height * 0.2)

    checkbox_size = 35

    #making the checkbox for each habit
    habit.checkbox_rect = pygame.Rect(
        container_rect.x + container_rect.width - checkbox_size - 20,
        container_rect.y - checkbox_size//2 + container_rect.height//2,
        checkbox_size,
        checkbox_size,
    )

    vert_rect = pygame.Rect(
        container_rect.x + container_rect.width//2 - checkbox_size//2,
        container_rect.y,
        checkbox_size,
        container_rect.height,
    )

    
    if habit.completed_today:
        text_color = (115,134,120)        
    else:
        text_color = DEEPGREEN

    checklist_item = font.render(habit.name, True, text_color)

    pygame.draw.rect(screen, (227, 252, 227), container_rect, border_radius= 10)
    screen.blit(checklist_item, (container_rect.x + 20, container_rect.y + 8))
    screen.blit(days_completed, (container_rect.x + 20, container_rect.y + checklist_item.get_height() + 5))
    screen.blit(start_date, (container_rect.x + 20, container_rect.y + + checklist_item.get_height() + days_completed.get_height() + 5))
    screen.blit(last_completed, (container_rect.x + container_rect.width - last_completed.get_width() - 10, container_rect.y + container_rect.height - last_completed.get_height() - 10))

    if not habit.completed_today: #a checkbox is drawn if the habit is not completed today
        pygame.draw.rect(screen, LIGHT_COOLGREEN , habit.checkbox_rect, width=2 , border_radius= 3)
    else: # the habit is marked done if it is completed
        pygame.draw.rect(screen, LIGHT_COOLGREEN, vert_rect)
        done_text = font.render("DONE", True, WHITE)
        rotated_surface = pygame.transform.rotate(done_text, 270)  #270 degrees
        screen.blit(rotated_surface, (vert_rect.x + rotated_surface.get_width()//2 - 12, vert_rect.y + rotated_surface.get_height()//2 - 10))


    return y_offset + container_rect.height


def habit_input():
    """handles the display of user input inside the input text box"""
    global input_active
    global input_box

    if input_active:
        color = (227, 252, 227)
        text_color = DEEPGREEN
    else:
        color = LIGHT_COOLGREEN
        text_color = (143, 201, 143)
        if input_box == "":
            input_box = "Enter text here"


    # Calculate max width allowed
    max_width = input_rect.width - 20  # padding on both sides

    # Clip text if it overflows
    display_text = input_box
    while font.size(display_text)[0] > max_width and len(display_text) > 0:
        display_text = display_text[1:]  # remove characters from the start

    # Render clipped text
    text_surface = font.render(display_text, True, text_color)
    
    pygame.draw.rect(screen, color, input_rect,border_radius=10)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y))

def draw_fade_edges(player):
    """Draws a gradient ontop and bottom of the checklist for semless scrolling, almost entirely made by chat gpt"""
    fade_height = 30
    width = check_list_box.width
    border_radius = 14

    # Create a surface with per-pixel alpha
    top_fade = pygame.Surface((width, fade_height), pygame.SRCALPHA)
    bottom_fade = pygame.Surface((width, fade_height), pygame.SRCALPHA)

    # Fill each row with decreasing alpha
    for i in range(fade_height):
        alpha = int(255 * (1 - i / fade_height))
        color = (*LIGHT_COOLGREEN, alpha)
        pygame.draw.rect(top_fade, color, pygame.Rect(0, i, width, 1))
        pygame.draw.rect(bottom_fade, color, pygame.Rect(0, i, width, 1))

    # Create masks with rounded corners for top and bottom
    mask = pygame.Surface((width, fade_height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)

    top_fade.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    bottom_fade.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Only show top fade if scrolled
    if scroll_offset > 0:
        screen.blit(top_fade, (check_list_box.x, check_list_box.y))

    # Bottom fade: only if not fully scrolled
    max_scroll = max(len(player.habits) * (10 + check_list_box.height * 0.2) - check_list_box.height + 10, 0)
    if scroll_offset < max_scroll:
        screen.blit(pygame.transform.flip(bottom_fade, False, True),
                    (check_list_box.x, check_list_box.y + check_list_box.height - fade_height))

def confirm_popup(habit_name):
    """Handles the pop-up when a user clicks the checklist for a habit"""
    popup_width = 400
    popup_height = 200
    popup_rect = pygame.Rect(
        (S_WIDTH - popup_width) // 2,
        (S_HEIGHT - popup_height) // 2,
        popup_width,
        popup_height
    )

    yes_button = pygame.Rect(popup_rect.x + 50, popup_rect.y + 130, 100, 40)
    no_button = pygame.Rect(popup_rect.x + 250, popup_rect.y + 130, 100, 40)

    # Create dim background
    dim_surface = pygame.Surface((S_WIDTH, S_HEIGHT), pygame.SRCALPHA)
    dim_surface.fill((GRAYGREEN + (15,)))  # Semi-transparent black

    while True:
        screen.blit(dim_surface, (0, 0))

        # Draw popup window
        pygame.draw.rect(screen, (245, 255, 245), popup_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, popup_rect, 2, border_radius=12)

        # Render text
        message = font.render("Are you sure you did your task?", True, DEEPGREEN)
        task_name = small_font.render(f"\"{habit_name}\"", True, GRAYGREEN)

        screen.blit(message, (popup_rect.centerx - message.get_width() // 2, popup_rect.y + 30))
        screen.blit(task_name, (popup_rect.centerx - task_name.get_width() // 2, popup_rect.y + 60))

        # Render buttons
        pygame.draw.rect(screen, (100, 200, 100), yes_button, border_radius=8)
        pygame.draw.rect(screen, (200, 100, 100), no_button, border_radius=8)

        yes_text = font.render("Yes", True, BLACK)
        no_text = font.render("No", True, BLACK)

        screen.blit(yes_text, (yes_button.centerx - yes_text.get_width() // 2, yes_button.y + 4))
        screen.blit(no_text, (no_button.centerx - no_text.get_width() // 2, no_button.y + 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #checking whether the user presses yes or no
                if yes_button.collidepoint(event.pos):
                    return True
                elif no_button.collidepoint(event.pos):
                    return False

def next_day():
    """The next day button and it's functionality for test user"""
    button_text = font.render("Next Day", True, WHITE)
    global next_day_button
    next_day_button = pygame.Rect(10,S_HEIGHT - button_text.get_height() - 20, button_text.get_width() + 10, button_text.get_height() + 10 )
    pygame.draw.rect(screen, COOLGREEN, next_day_button, border_radius= 3)
    screen.blit(button_text, (next_day_button.x + 5, next_day_button.y + 5))

def update_date(player):
    """Resets all habits if a new day has come"""
    today = datetime.date.today()
    if today != player.last_played:
        player.reset_habit()

def garden_section(player):
    """Draws the garden section, currently all commented out since I realized I didnt have time to properly implement it"""
    global garden_box

    score = player.score
    gardener = player.username

    gardener_surface = font.render(gardener, True, DEEPGREEN)
    score_surface = small_font.render("Garden points: "+ str(score), True, DEEPGREEN)

    screen.blit(gardener_surface, (10, 10))
    screen.blit(score_surface, (gardener_surface.get_width() + 15, 10 + gardener_surface.get_height() - score_surface.get_height()))

    # # Draw platforms
    # num_platforms = 9
    # vertical_spacing = garden_box.height // (num_platforms + 1)
    
    # for i in range(num_platforms):
    #     platform_y = garden_box.y + vertical_spacing * (i + 1)
    #     platform_rect = pygame.Rect(garden_box.x -4, platform_y, garden_box.width + 8, 10)
        
    #     # Scale the sprite to match this rect
    #     scaled_sprite = pygame.transform.scale(platform_sprite, (platform_rect.width, platform_rect.height))

    #     # Blit the scaled sprite at the rect's position
    #     screen.blit(scaled_sprite, platform_rect.topleft)

    #     #draw a border around the sprite area
    #     pygame.draw.rect(screen, DEEPGREEN, platform_rect, width=1, border_radius=3)

def load_sprites():
    """Loads all the sprites, currently not useful"""
    global garden_box
    global platform_sprite
    platform_image = pygame.image.load("assets/sprite/platform.png").convert_alpha()
    platform_sprite = pygame.transform.scale(platform_image, (garden_box.width, 10))

