from objects import Habit
import pygame
pygame.init()
pygame.key.set_repeat(400, 30)

#screen dimensions
S_HEIGHT = 700
S_WIDTH = 900

#habit tracker system
habit_box = pygame.Rect(S_WIDTH - 510, 30, 500, S_HEIGHT - 60)
check_list_box = pygame.Rect(habit_box.x + 50, habit_box.y + 120, 400, habit_box.height - 150)

#font
font=pygame.font.Font("assets/font/Grand9K Pixel.ttf", 20)
heading_font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 30)
small_font = pygame.font.Font("assets/font/Grand9K Pixel.ttf", 10)
input_box = "Enter text here"
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
LIGHTER_COOLGREEN = (194, 252, 194)
DEEPGREEN = (6,64,43)
GRAYGREEN = (143 ,151, 121)

running = True

def main(running):
    global input_box
    global input_active
    global scroll_offset

    #loading assets
    bg_image = pygame.image.load("assets/bg.png")
    bg_image = pygame.transform.scale(bg_image, (S_WIDTH, S_HEIGHT))


    while running:

        fps = clock.tick(60)/1000

        for event in pygame.event.get(): #checling for an event
            if event.type == pygame.QUIT: #quitng the loop if user quits
                running = False
            
            #checking if the user scrolled
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 40  # Adjust scroll speed
                max_scroll = max(len(Habit.all_habits) * (10 + check_list_box.height * 0.2) - check_list_box.height + 10 , 0)
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            if event.type == pygame.MOUSEBUTTONDOWN:
                #checking if the user has input box selected
                if input_rect.collidepoint(event.pos):
                    input_active = True
                    if input_box == "Enter text here":
                        input_box = ""
                else:
                    input_active = False

                # Check if a checkbox is clicked
                for habit in Habit.all_habits:
                    if habit.checkbox_rect and habit.checkbox_rect.collidepoint(event.pos):
                        habit.completed_today = not habit.completed_today  # Toggle status
                        break 

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_box = input_box[:-1]
                    else:
                        input_box += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        entered_text = input_box[:-1]
                        if entered_text != "":
                            Habit(entered_text)

                        input_box = ""

        screen.blit(bg_image, (0,0))
        
        habit_section()
        
        pygame.display.update()

    pygame.quit()

def habit_section():

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
    show_checklist(scroll_offset)

    habit_input()

def show_checklist(offset):
    y_offset = check_list_box.y + 10 - offset  # start a little inside the box
    line_spacing = 10  # space between habits

    screen.set_clip(pygame.Rect(check_list_box.x, check_list_box.y + 2, check_list_box.width, check_list_box.height - 4))  # Prevent drawing outside the checklist box
    for habit in Habit.all_habits:      
        y_offset = checklist_element(habit, y_offset)
        y_offset += line_spacing

    screen.set_clip(None)
    draw_fade_edges()

def checklist_element(habit, y_offset):
    start_date = small_font.render("start: " + str(habit.start_date), True, GRAYGREEN)
    last_completed =  small_font.render("last done: " + str(habit.last_completed), True, GRAYGREEN)
    days_completed =  small_font.render("Days Completed: " + str(habit.days_completed), True, GRAYGREEN)

    container_rect = pygame.Rect(check_list_box.x + 10,
                                 y_offset,
                                 check_list_box.width - 20,
                                 check_list_box.height * 0.2)

    checkbox_size = 35

    if habit.completed_today:
        text_color = (115,134,120)
    else:
        text_color = DEEPGREEN

    #making the checkbox for each habit
    habit.checkbox_rect = pygame.Rect(
        container_rect.x + container_rect.width - checkbox_size - 20,
        container_rect.y - checkbox_size//2 + container_rect.height//2,
        checkbox_size,
        checkbox_size,
    )

    checklist_item = font.render(habit.name, True, text_color)

    pygame.draw.rect(screen, (227, 252, 227), container_rect, border_radius= 10)
    screen.blit(checklist_item, (container_rect.x + 20, container_rect.y + 8))
    screen.blit(days_completed, (container_rect.x + 20, container_rect.y + checklist_item.get_height() + 5))
    screen.blit(start_date, (container_rect.x + 20, container_rect.y + + checklist_item.get_height() + days_completed.get_height() + 5))
    screen.blit(last_completed, (container_rect.x + container_rect.width - last_completed.get_width() - 10, container_rect.y + container_rect.height - last_completed.get_height() - 10))

    pygame.draw.rect(screen, LIGHT_COOLGREEN , habit.checkbox_rect, width=2 , border_radius= 3)

    return y_offset + container_rect.height


def habit_input():
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

def draw_fade_edges():
    fade_height = 30
    width = check_list_box.width
    border_radius = 14

    # Create a surface with per-pixel alpha
    top_fade = pygame.Surface((width, fade_height), pygame.SRCALPHA)
    bottom_fade = pygame.Surface((width, fade_height), pygame.SRCALPHA)

    # Fill each row with decreasing alpha
    for i in range(fade_height):
        alpha = int(255 * (1 - i / fade_height))
        color = (*LIGHTER_COOLGREEN, alpha)
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
    max_scroll = max(len(Habit.all_habits) * (10 + check_list_box.height * 0.2) - check_list_box.height + 10, 0)
    if scroll_offset < max_scroll:
        screen.blit(pygame.transform.flip(bottom_fade, False, True),
                    (check_list_box.x, check_list_box.y + check_list_box.height - fade_height))

main(running)