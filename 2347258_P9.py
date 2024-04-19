import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Jet Plane Bombing Animation")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load images
jet_image = pygame.image.load('jet.jpg')
bomb_image = pygame.image.load('explosion.jpg')
house_image = pygame.image.load('house.jpg')
explosion_image = pygame.image.load('bomb.jpg')

# Load sound
bomb_sound = pygame.mixer.Sound('bomb_sound.wav')

# Define a custom event for the explosion timer
EXPLOSION_TIMER_EVENT = pygame.USEREVENT + 1

class JetPlane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jet_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, house):
        super().__init__()
        self.image = bomb_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.house = house

    def update(self):
        self.rect.y += self.speed
        if self.rect.colliderect(self.house.rect):
            self.kill()
            bomb_sound.play()
            self.house.hit_by_bomb()

class House(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = house_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.exploding = False

    def hit_by_bomb(self):
        if not self.exploding:
            self.exploding = True
            self.image = explosion_image
            # Set up the explosion timer
            pygame.time.set_timer(EXPLOSION_TIMER_EVENT, 1000) # 1000 milliseconds = 1 second

all_sprites = pygame.sprite.Group()
jets = pygame.sprite.Group()
house = House()
all_sprites.add(house)

jet = JetPlane()
all_sprites.add(jet)
jets.add(jet)

# Set up the explosion timer
pygame.time.set_timer(EXPLOSION_TIMER_EVENT, 1000) # 1000 milliseconds = 1 second

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == EXPLOSION_TIMER_EVENT:
            if house.exploding:
                house.exploding = False
                house.image = house_image # Revert to the original house image

    # Update all sprites
    all_sprites.update()

    # Randomly spawn bombs
    if random.randrange(100) < 2: # Adjust the probability as needed
        x = random.randrange(SCREEN_WIDTH)
        y = 0
        bomb = Bomb(x, y, house)
        all_sprites.add(bomb)

    # Draw everything
    screen.fill((0, 0, 0)) # Clear the screen
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
