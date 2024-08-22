#type: ignore

import os

import pygame

from helpers import SCREEN_HEIGHT, SCREEN_WIDTH

CELL_SIZE = 96 # size in pixels of each cell in the grid where characters are displayed
MENU_WIDTH = CELL_SIZE * 3 # width of the menu where characters are displayed
MENU_HEIGHT = CELL_SIZE * 3 # height of the menu where characters are displayed

# Define the paths to your image resources
IMAGE_DIR = "Resources"  # Adjust to match your directory structure
IMAGE_FILES = {
    'kimono_rogue': os.path.join(IMAGE_DIR, "kimono.png"),
    'kimono_knight': os.path.join(IMAGE_DIR, "kimono knight.png"),
    'kimono_monk': os.path.join(IMAGE_DIR, "kimono monk.png"),
    'authority_rogue': os.path.join(IMAGE_DIR, "authority_logo.png"),
    'authority_knight': os.path.join(IMAGE_DIR, "authority knight.png"),
    'authority_monk': os.path.join(IMAGE_DIR, "authority monk.png"),
    'maniac_rogue': os.path.join(IMAGE_DIR, "maniac.png"),
    'maniac_knight': os.path.join(IMAGE_DIR, "maniac knight.png"),
    'maniac_monk': os.path.join(IMAGE_DIR, "maniac monk.jpeg")
}

character_spreadsheet = {
    # Kimono Row
    'kimono_rogue': [0,0],
    'kimono_knight': [32,0],
    'kimono_monk': [64,0],

    # Authority Row
    'authority_rogue': [0,32],
    'authority_knight': [32,32],
    'authority_monk': [64,32],

    # Maniac Row
    'maniac_rogue': [0,64],
    'maniac_knight': [32,64],
    'maniac_monk': [64,64]
  }

# Function to load images
def load_images():
    images = {}
    for character, file_path in IMAGE_FILES.items():
        images[character] = pygame.image.load(file_path).convert_alpha()
    return images

# Function to display characters
def display_characters(screen, images):
    menu_x = (SCREEN_WIDTH - 250) // 2
    menu_y = (SCREEN_HEIGHT - 250) // 2
    for row in range(3):
        for col in range(3):
            character_key = list(character_spreadsheet.keys())[row * 3 + col]
            #character_spreadsheet[character_key]
            x = menu_x + col * CELL_SIZE
            y = menu_y + row * CELL_SIZE

            # Draw white box
            pygame.draw.rect(screen, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE))

            # Draw character/image
            image = images.get(character_key)
            draw_image(image, x, y, screen)

# Function to draw image
def draw_image(img, x=0, y=0, screen=None, pos=(0, 0), scale=(0, 0)):
    size = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))  # Scale to fit the cell size
    screen.blit(size, (x, y))
    pygame.display.update()