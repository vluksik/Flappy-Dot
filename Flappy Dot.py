import pygame # pip install pygame
import random
import sys

pygame.init() # Initialize Pygame

SCREEN_WIDTH = 600  
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (173, 216, 230)  
START_SCREEN_COLOR = (35, 199, 229)  
DOT_COLOR = (0, 0, 0) 
PIPE_COLOR = (0, 128, 0) 
PIPE_WIDTH = 50
GAP_HEIGHT = 150
GRAVITY = 0.5
JUMP_SPEED = -8
FONT_PATH = "OptimusPrinceps.ttf" # Loads the font for the game
GAME_FONT = pygame.font.Font(FONT_PATH, 36)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Dot")

clock = pygame.time.Clock()


class Dot:      # The dot that the player controls
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.falling = False
    
    def jump(self): # Makes the dot jump
        self.velocity = JUMP_SPEED
        self.falling = True
    
    def update(self): # Updates the position of the dot
        if self.falling:
            self.velocity += GRAVITY
            self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, DOT_COLOR, (self.x, int(self.y)), 10)


class Pipe:   # The pipes that the dot must avoid
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - GAP_HEIGHT - 50)
    
    def move(self): # Moves the pipes to the left
        self.x -= 5
    
    def off_screen(self):   # Checks if the pipe has gone off the screen
        return self.x < -PIPE_WIDTH
    
    def draw(self): # Draws the pipes
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.height + GAP_HEIGHT, PIPE_WIDTH, SCREEN_HEIGHT))


dot = Dot()
pipes = []
score = 0


def create_pipe():  # Creates a new pipe and adds it to the list of pipes
    pipe = Pipe(SCREEN_WIDTH)
    pipes.append(pipe)


def handle_events():  # Handles the events of the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dot.jump()


def draw_background(): # Draws the background of the game
    screen.fill(BACKGROUND_COLOR)


def draw_objects(): # Draws the dot and the pipes
    dot.draw()
    for pipe in pipes:
        pipe.draw()


def update_objects(): # Updates the dot and the pipes
    dot.update()
    for pipe in pipes:
        pipe.move()
    
    if pipes and pipes[0].x < -PIPE_WIDTH:
        pipes.pop(0)


def check_collisions(): # Checks if the dot has collided with the pipes
    for pipe in pipes:
        if (dot.x + 10 > pipe.x and dot.x - 10 < pipe.x + PIPE_WIDTH and
            (dot.y - 10 < pipe.height or dot.y + 10 > pipe.height + GAP_HEIGHT)):
            return True
    return False


def show_game_over():  # Displays the game over screen
    screen.fill((0, 0, 0))
    text_surface = GAME_FONT.render("YOU DIED", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


def show_score(): # Display thew score of the player
    score_surface = GAME_FONT.render("Score: " + str(score * 100), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))


def show_start_screen(): # Displays the start screen of the game
    """
    Displays the start screen of the game.
    """
    screen.fill((208, 216, 218)) 
    title_surface = GAME_FONT.render("FLAPPY DOT", True, (255, 0, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_surface, title_rect)
    start_surface = GAME_FONT.render("Click your mouse to start", True, (255, 0, 0))
    start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_surface, start_rect)



show_start_screen()
pygame.display.flip()


game_started = False  # A flag to check if the game has started
while not game_started:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_started = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



create_pipe_timer = 0 # A timer to create new pipes
game_over = False
while not game_over:
    handle_events()
    draw_background()
    
    if create_pipe_timer == 100:
        create_pipe()
        create_pipe_timer = 0
        score += 1
    else:
        create_pipe_timer += 1
    
    update_objects()
    draw_objects()
    show_score()
    
    if check_collisions() or dot.y < 0 or dot.y > SCREEN_HEIGHT: # If the dot has collided with the pipes or has gone out of the screen
        game_over = True
        
    
    pygame.display.flip()
    clock.tick(60)


show_game_over() # Display the game over screen
pygame.display.flip()

pygame.time.wait(2000)

pygame.quit()
sys.exit()
