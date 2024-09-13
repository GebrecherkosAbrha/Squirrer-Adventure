import pygame
import random
import yaml

# Load configuration from YAML file


def load_config(filename='config.yml'):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


# Load game configuration
config = load_config()
SCREEN_WIDTH = config['screen']['width']
SCREEN_HEIGHT = config['screen']['height']
SQUIRREL_SIZE = (config['squirrel']['size']['width'],
                 config['squirrel']['size']['height'])
ACORN_SIZE = (config['acorn']['size']['width'],
              config['acorn']['size']['height'])
OBSTACLE_SIZE = (config['obstacle']['size']['width'],
                 config['obstacle']['size']['height'])
INITIAL_SPEED = config['initial_speed']
LEVEL_UP_THRESHOLD = config['level_up_threshold']

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Squirrer")

# Clock to control frame rate
clock = pygame.time.Clock()

# Classes for game objects


class Squirrel:
    def __init__(self):
        self.image = pygame.Surface(SQUIRREL_SIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = INITIAL_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Acorn:
    def __init__(self):
        self.image = pygame.Surface(ACORN_SIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def fall(self, speed):
        self.rect.y += speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

    def draw(self):
        screen.blit(self.image, self.rect)


class Obstacle:
    def __init__(self):
        self.image = pygame.Surface(OBSTACLE_SIZE)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def fall(self, speed):
        self.rect.y += speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

    def draw(self):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.squirrel = Squirrel()
        self.acorn = Acorn()
        self.obstacle = Obstacle()
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.running = True
        self.game_over = False
        self.level_up_flag = False  # Flag to prevent multiple level-ups at the same score

    def check_collision(self):
        if self.squirrel.rect.colliderect(self.acorn.rect):
            self.score += 1
            self.acorn.rect.y = -self.acorn.rect.height
            self.acorn.rect.x = random.randint(
                0, SCREEN_WIDTH - self.acorn.rect.width)

        if self.squirrel.rect.colliderect(self.obstacle.rect):
            self.game_over = True

    def update_level(self):
        # Level up when the score reaches multiples of LEVEL_UP_THRESHOLD, but only once
        if self.score > 0 and self.score % LEVEL_UP_THRESHOLD == 0 and not self.level_up_flag:
            self.level += 1
            self.speed += 1
            self.level_up_flag = True  # Set flag to prevent multiple increments

        # Reset flag once the score moves away from the current threshold
        if self.score % LEVEL_UP_THRESHOLD != 0:
            self.level_up_flag = False

    def display_text(self, text, font_size, color, x, y):
        font = pygame.font.SysFont(None, font_size)
        rendered_text = font.render(text, True, color)
        screen.blit(rendered_text, (x, y))

    def reset(self):
        self.__init__()

    def game_over_screen(self):
        screen.fill(WHITE)
        self.display_text("GAME OVER", 72, RED,
                          SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
        self.display_text(f"Score: {self.score}", 50,
                          BLACK, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
        self.display_text("Press R to Restart", 36, BLACK,
                          SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5)
        pygame.display.update()

    def run(self):
        while self.running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.reset()

            keys = pygame.key.get_pressed()
            if not self.game_over:
                self.squirrel.move(keys)
                self.acorn.fall(self.speed)
                self.obstacle.fall(self.speed)
                self.check_collision()
                self.update_level()

                self.squirrel.draw()
                self.acorn.draw()
                self.obstacle.draw()

                # Display score and level
                self.display_text(f"Score: {self.score}", 36, BLACK, 10, 10)
                self.display_text(f"Level: {self.level}", 36, BLACK, 10, 50)
            else:
                self.game_over_screen()

            pygame.display.update()
            clock.tick(30)


# Start the game
game = Game()
game.run()

pygame.quit()
