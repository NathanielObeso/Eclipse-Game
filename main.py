#type: ignore

import gameplay
import pygame
import random

from character_select import display_characters, IMAGE_FILES, load_images
from helpers import *

charCount = 0 # Variable to store number of characters selected
choice1 = [] # Player 1 grid
choice2 = [] # Player 2 grid
chargrid = [[None, None, None], [None, None, None], [None, None, None]] # The entire grid

pygame.init()
pygame.mixer.init()

begin = pygame.mixer.Sound("game_begin.wav")
select = pygame.mixer.Sound("character_selection.wav")

game_name_font = pygame.font.SysFont(DEFAULT_FONT, FONT_SIZE)

# Class for making the buttons
class GameButton():

  def __init__(self, text, width, height, pos, color="#475F77", text_color="#FFFFFF", text_font="Arial"):
    self.pressed = False
    self.top_rect = pygame.Rect(pos, (width, height))
    self.top_color = color
    
    #text vars
    self.text_surf = game_name_font.render(text, True, text_color)
    self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

  def draw(self):
    pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
    screen.blit(self.text_surf, self.text_rect)
    self.click_check()

  def click_check(self):
    mouse_pos = pygame.mouse.get_pos()
    if self.top_rect.collidepoint(mouse_pos):
      self.top_color = "#D66768"
      if pygame.mouse.get_pressed()[0]:
        self.pressed = True
      #else:
      #if self.pressed == True:
      #print('click')
      #self.pressed = False
    else:
      self.top_color = "#475F77"


# Display sprites of characters in the overworld
class Character(pygame.sprite.Sprite):

  def __init__(self, x, y, name, owner):
    self.x = x
    self.y = y
    self.name = name
    self.owner = owner
    self.moved = False

  def movedBorder(self):
    if self.moved == False:
      drawBorder(self.x, self.y, (0,255,0))
    else:
      drawBorder(self.x, self.y, (0,0,0))

  def resetMoved(self, x, y):
    self.moved = False
    self.x = x
    self.y = y
    self.movedBorder()

  def setMoved(self):
    self.moved = True
    self.movedBorder()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True

def drawBorder(x, y, color):
  pygame.draw.line(screen, color, (x, y), (x+90, y))
  pygame.draw.line(screen, color, (x+90, y), (x+90, y+90))
  pygame.draw.line(screen, color, (x+90, y+90), (x, y+90))
  pygame.draw.line(screen, color, (x, y+90), (x, y))

def draw_text(text, font, text_col=(0, 0, 0), x=0, y=0):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))
  pygame.display.update()


def draw_image(img_path, pos=(0, 0), scale=(0, 0)):
  img = pygame.image.load(img_path)
  size = pygame.transform.scale(img, scale)
  screen.blit(size, pos)
  pygame.display.update()

def charTaken(character):
  return character in choice1 or character in choice2

def placeCharacter(character, x, y):
  pygame.draw.rect(screen, (255, 255, 255), (x, y, 90, 90))
  image = None

  low = character.lower()
  charName = low.replace(" ", "_")
  image = IMAGE_FILES[charName]

  draw_image(image, pos=(x, y), scale=(90, 90))
  drawBorder(x, y, (0, 0, 0))


def containsChar(x, y):
  if x > 2 or y > 2 or x < 0 or y < 0:
    return False
  if chargrid[x][y] != None:
    return True
  else:
    return False


def charSpace(space):
  col_1 = space[0] >= 142.5 and space[0] < 232.5
  col_2 = space[0] >= 232.5 and space[0] < 322.5
  col_3 = space[0] >= 322.5 and space[0] < 412.5
  row_1 = space[1] >= 142.5 and space[1] < 232.5
  row_2 = space[1] >= 232.5 and space[1] < 322.5
  row_3 = space[1] >= 322.5 and space[1] < 412.5

  if col_1 and row_1:
    return (0, 0)
  elif col_1 and row_2:
    return (1, 0)
  elif col_1 and row_3:
    return (2, 0)
  elif col_2 and row_1:
    return (0, 1)
  elif col_2 and row_2:
    return (1, 1)
  elif col_2 and row_3:
    return (2, 1)
  elif col_3 and row_1:
    return (0, 2)
  elif col_3 and row_2:
    return (1, 2)
  elif col_3 and row_3:
    return (2, 2)
  else:
    return None


def canMove(start, end):
  if containsChar(start[0], start[1]):
    x = end[0] - start[0]
    y = end[1] - start[1]

    if abs(x) == abs(y):
      return True
    elif x == 0 or y == 0:
      return True
    else:
      return False
  else:
    return False

def resetGrid():
  draw_image("Resources/grid.png", pos=(142.5, 142.5), scale=(270, 270))

  listNo = 0

  for list in chargrid:
    for item in range(0, 3):
      if list[item] != None:
        placeCharacter(list[item].name, 142.5 + item * 90, 142.5 + listNo * 90)

    listNo += 1


play_button = GameButton("Play", 100, 50,
                         (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 25))

main_menu = True

while run:
  #fill screen with black first
  screen.fill((255, 255, 255))

  #Fill background and scale to fit the screen
  draw_image("Resources/background.png",
             (0,0),
             scale=(SCREEN_WIDTH, SCREEN_HEIGHT))

  draw_text(GAME_NAME, game_name_font, (0, 0, 0),
            SCREEN_WIDTH / 2 - len(GAME_NAME) - FONT_SIZE,
            SCREEN_HEIGHT / 2 - FONT_SIZE)

  # Main menu loop
  while main_menu is True:

    play_button.draw()
    # main menu
    # manu menu code rendering
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      #elif event.type == pygame.MOUSEBUTTONDOWN:
      #draw_text(f"x: {event.pos[0]}, y: {event.pos[1]}", game_name_font, (0,0,0), event.pos[0], event.pos[1])

    # Code for hovered title.
    # elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 350 and pygame.mouse.get_pos()[1] >= 150 and pygame.mouse.get_pos()[1] <= 350:
    # draw_image("Resources/play button hovered.png", 250, 250, scale = (100,100))

    pygame.display.update()

    if play_button.pressed is True:
      main_menu = False

  screen.fill((255, 255, 255))
  draw_image("Resources/background.png",
             (0, 0),
             scale=(SCREEN_WIDTH, SCREEN_HEIGHT))

  character_selection = True

  # character select
  # character select code rendering

  character_select_text = 'Choose Your Characters'
  draw_text(character_select_text, game_name_font, (0, 0, 0),
            SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT * 1 / 10 - 50)
  grid = load_images()
  display_characters(screen, grid)
  charName = pygame.Rect((125, 75), (125, 25))
  play = pygame.Rect((400, 75), (75, 30))
  taken = pygame.Rect(125, 25, 260, 20)
  
  while character_selection is True:

    col_1 = pygame.mouse.get_pos()[0] >= 125 and pygame.mouse.get_pos(
    )[0] < 221
    col_2 = pygame.mouse.get_pos()[0] >= 221 and pygame.mouse.get_pos(
    )[0] < 317
    col_3 = pygame.mouse.get_pos()[0] >= 317 and pygame.mouse.get_pos(
    )[0] < 413
    row_1 = pygame.mouse.get_pos()[1] >= 125 and pygame.mouse.get_pos(
    )[1] < 221
    row_2 = pygame.mouse.get_pos()[1] >= 221 and pygame.mouse.get_pos(
    )[1] < 317
    row_3 = pygame.mouse.get_pos()[1] >= 317 and pygame.mouse.get_pos(
    )[1] < 413

    if charCount < 3:
      pygame.draw.rect(screen, (0, 0, 255), play)
      draw_text("Player 1", game_name_font, (0, 0, 0), 400, 75)
    else:
      pygame.draw.rect(screen, (0, 0, 255), play)
      draw_text("Player 2", game_name_font, (0, 0, 0), 400, 75)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEMOTION:
        if col_1 and row_1:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Kimono Rogue", game_name_font, x=125, y=75)

        elif col_2 and row_1:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Kimono Knight", game_name_font, x=125, y=75)

        elif col_3 and row_1:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Kimono Monk", game_name_font, x=125, y=75)

        elif col_1 and row_2:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Authority Rogue", game_name_font, x=125, y=75)

        elif col_2 and row_2:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Authority Knight", game_name_font, x=125, y=75)

        elif col_3 and row_2:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Authority Monk", game_name_font, x=125, y=75)

        elif col_1 and row_3:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Maniac Rogue", game_name_font, x=125, y=75)

        elif col_2 and row_3:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Maniac Knight", game_name_font, x=125, y=75)

        elif col_3 and row_3:
          pygame.draw.rect(screen, (0, 0, 255), charName)
          draw_text("Maniac Monk", game_name_font, x=125, y=75)

      if event.type == pygame.MOUSEBUTTONDOWN:
        if row_1 and col_1:
          if charTaken("Kimono Rogue") == False:
            if charCount < 3:
              choice1.append("Kimono Rogue")
            else:
              choice2.append("Kimono Rogue")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (125, 125), (221, 221))
            pygame.draw.line(screen, (0, 0, 0), (221, 125), (125, 221))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_2 and col_1:
          if charTaken("Authority Rogue") == False:
            if charCount < 3:
              choice1.append("Authority Rogue")
            else:
              choice2.append("Authority Rogue")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (125, 221), (221, 317))
            pygame.draw.line(screen, (0, 0, 0), (221, 221), (125, 317))
            
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_3 and col_1:
          if charTaken("Maniac Rogue") == False:
            if charCount < 3:
              choice1.append("Maniac Rogue")
            else:
              choice2.append("Maniac Rogue")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (125, 317), (221, 413))
            pygame.draw.line(screen, (0, 0, 0), (221, 317), (125, 413))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_1 and col_2:
          if charTaken("Kimono Knight") == False:
            if charCount < 3:
              choice1.append("Kimono Knight")
            else:
              choice2.append("Kimono Knight")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (221, 125), (317, 221))
            pygame.draw.line(screen, (0, 0, 0), (317, 125), (221, 221))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_1 and col_3:
          if charTaken("Kimono Monk") == False:
            if charCount < 3:
              choice1.append("Kimono Monk")
            else:
              choice2.append("Kimono Monk")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (317, 125), (413, 221))
            pygame.draw.line(screen, (0, 0, 0), (413, 125), (317, 221))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_2 and col_2:
          if charTaken("Authority Knight") == False:
            if charCount < 3:
              choice1.append("Authority Knight")
            else:
              choice2.append("Authority Knight")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (221, 221), (317, 317))
            pygame.draw.line(screen, (0, 0, 0), (317, 221), (221, 317))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_2 and col_3:
          if charTaken("Authority Monk") == False:
            if charCount < 3:
              choice1.append("Authority Monk")
            else:
              choice2.append("Authority Monk")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (317, 221), (413, 317))
            pygame.draw.line(screen, (0, 0, 0), (413, 221), (317, 317))
            
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_3 and col_2:
          if charTaken("Maniac Knight") == False:
            if charCount < 3:
              choice1.append("Maniac Knight")
            else:
              choice2.append("Maniac Knight")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (221, 317), (317, 413))
            pygame.draw.line(screen, (0, 0, 0), (317, 317), (221, 413))
            
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

        if row_3 and col_3:
          if charTaken("Maniac Monk") == False:
            if charCount < 3:
              choice1.append("Maniac Monk")
            else:
              choice2.append("Maniac Monk")
            select.play()
            charCount += 1
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character successfully selected",
                      game_name_font,
                      x=125,
                      y=25)

            pygame.draw.line(screen, (0, 0, 0), (317, 317), (413, 413))
            pygame.draw.line(screen, (0, 0, 0), (413, 317), (317, 413))
          
          else:
            pygame.draw.rect(screen, (0, 0, 255), taken)
            draw_text("Character has already been taken",
                      game_name_font,
                      x=125,
                      y=25)

    if charCount >= 6:
      character_selection = False

    pygame.display.update()

  # character_select_text = 'Choose Your Characters'
  #textRect = text.get_rect()
  #draw_text(character_select_text, game_name_font,(0,0,0), SCREEN_WIDTH /2-75, SCREEN_HEIGHT * 1 / 3)
  # Game
  # Game code rendering

  screen.fill((255, 255, 255))
  draw_image("Resources/background.png",
             (0,0),
             scale=(SCREEN_WIDTH, SCREEN_HEIGHT))

  # Character placement screen looped inside the gameplay
  character_placement = True

  while character_placement is True:
    x = 0
    character_specify = pygame.Rect(130, 0, 350, 20)
    pygame.draw.rect(screen, (0, 0, 255), character_specify)
    draw_image("Resources/grid.png", pos=(142.5, 142.5), scale=(270, 270))
    y = 0
    choice = choice1
    while x <= 2:
      if choice == choice1:
        owner = "Player 1"
      else:
        owner = "Player 2"
        
      place = owner + ", place " + choice[x] + " on grid:"
      draw_text(place, game_name_font, (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                SCREEN_HEIGHT * 1 / 10 - 50)

      col_1 = pygame.mouse.get_pos()[0] >= 142.5 and pygame.mouse.get_pos(
      )[0] < 232.5
      col_2 = pygame.mouse.get_pos()[0] >= 232.5 and pygame.mouse.get_pos(
      )[0] < 322.5
      col_3 = pygame.mouse.get_pos()[0] >= 322.5 and pygame.mouse.get_pos(
      )[0] < 412.5
      row_1 = pygame.mouse.get_pos()[1] >= 142.5 and pygame.mouse.get_pos(
      )[1] < 232.5
      row_2 = pygame.mouse.get_pos()[1] >= 232.5 and pygame.mouse.get_pos(
      )[1] < 322.5
      row_3 = pygame.mouse.get_pos()[1] >= 322.5 and pygame.mouse.get_pos(
      )[1] < 412.5

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          if row_1 and col_1:
            if containsChar(0, 0):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 142.5, 142.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(142.5, 142.5, name, owner)

              chargrid[0][0] = choiceObj

          elif row_1 and col_2:
            if containsChar(0, 1):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 232.5, 142.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(232.5, 142.5, name, owner)

              chargrid[0][1] = choiceObj

          elif row_1 and col_3:
            if containsChar(0, 2):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
              
            else:
              placeCharacter(choice[x], 322.5, 142.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(322.5, 142.5, name, owner)

              chargrid[0][2] = choiceObj

          elif row_2 and col_1:
            if containsChar(1, 0):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 142.5, 232.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(142.5, 232.5, name, owner)

              chargrid[1][0] = choiceObj

          elif row_2 and col_2:
            if containsChar(1, 1):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 232.5, 232.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(232.5, 232.5, name, owner)

              chargrid[1][1] = choiceObj

          elif row_2 and col_3:
            if containsChar(1, 2):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 322.5, 232.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(322.5, 232.5, name, owner)

              chargrid[1][2] = choiceObj

          elif row_3 and col_1:
            if containsChar(2, 0):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 142.5, 322.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(142.5, 322.5, name, owner)

              chargrid[2][0] = choiceObj

          elif row_3 and col_2:
            if containsChar(2, 1):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 232.5, 322.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(232.5, 322.5, name, owner)

              chargrid[2][1] = choiceObj

          elif row_3 and col_3:
            if containsChar(2, 2):
              pygame.draw.rect(screen, (0, 0, 255), character_specify)
              draw_text("Spot already taken. Try again.", game_name_font,
                        (0, 0, 0), SCREEN_WIDTH / 2 - 112.5,
                        SCREEN_HEIGHT * 1 / 10 - 50)
              x -= 1
            else:
              placeCharacter(choice[x], 322.5, 322.5)
              name = choice[x]
              owner = None
              if choice == choice1:
                owner = "Player 1"
              else:
                owner = "Player 2"
              choiceObj = Character(322.5, 322.5, name, owner)

              chargrid[2][2] = choiceObj

          else:
            x -= 1

          pygame.draw.rect(screen, (0, 0, 255), character_specify)
          x += 1
          if x >= 3:
            x = x % 3
            y += 1
            choice = choice2
            if y == 2:
              character_placement = False
              x = 3
              pygame.draw.rect(screen, (0, 0, 255), character_specify)

  draw_image("Resources/background.png",
             (0,0),
             scale=(SCREEN_WIDTH, SCREEN_HEIGHT))

  resetGrid()

  game = True

  player_1 = gameplay.Player("Player 1", 10, 10)
  player_2 = gameplay.Player("Player 2", 340, 10)

  pygame.draw.rect(screen, (0, 0, 255), (10, 440, 300, 30))
  text = ""
  draw_text(text, game_name_font, (0, 0, 0), 10, 440)

  initial_point = None
  turn_count = 1
  player = "Player 1"
  currentList = choice1.copy()

  turn = player + "\'s turn"
  pygame.draw.rect(screen, (0, 0, 255), (142.5, 90, 270, 30))
  draw_text(turn, game_name_font, (0, 0, 0), 230, 100)

  l = 0
  
  for list in chargrid:
    for item in range(0, 3):
      if list[item] != None:
        if list[item].owner == player:
          list[item].resetMoved(142.5 + 90*item, 142.5 + 90*l)

    l += 1

  player_1.basic_health(screen)
  player_2.basic_health(screen)

  begin.play()
  
  while game is True:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEMOTION:
        location = pygame.mouse.get_pos()
        coordinates = charSpace(location)
        if charSpace(location) is not None:
          x = coordinates[0]
          y = coordinates[1]
          if containsChar(x, y):
            pygame.draw.rect(screen, (0, 0, 255), (10, 440, 300, 30))
            text = chargrid[x][y].name + ": " + chargrid[x][y].owner
            draw_text(text, game_name_font, (0, 0, 0), 10, 440)

        if location[0] >= 10 and location[0] <= 160 and location[1] >= 10 and location[1] <= 35:
          pygame.draw.rect(screen, (0, 0, 255), (10, 440, 300, 30))
          text = "Player 1" + ": " + repr(round(player_1.current_health, 2)) + "/" + "200"
          draw_text(text, game_name_font, (0, 0, 0), 10, 440)

        if location[0] >= 340 and location[0] <= 490 and location[1] >= 10 and location[1] <= 35:
          pygame.draw.rect(screen, (0, 0, 255), (10, 440, 300, 30))
          text = "Player 2" + ": " + repr(round(player_2.current_health, 2)) + "/" + "200"
          draw_text(text, game_name_font, (0, 0, 0), 10, 440)

      if event.type == pygame.MOUSEBUTTONDOWN:
        start_point = pygame.mouse.get_pos()
        initial_point = charSpace(start_point)

      if event.type == pygame.MOUSEBUTTONUP: 
        end = charSpace(pygame.mouse.get_pos())
        if initial_point == None or end == None:
          continue
        x1 = initial_point[0]
        y1 = initial_point[1]
        x2 = end[0]
        y2 = end[1]
        if chargrid[x1][y1] == None:
          continue
        if chargrid[x1][y1].owner != player:
          continue
        if initial_point == end:
          continue
          
        if canMove(initial_point, end) and chargrid[x1][y1].name in currentList:
          chargrid[x1][y1].setMoved()

          if containsChar(x2, y2):
            HP_loss = gameplay.damage(chargrid[x1][y1], chargrid[x2][y2])
            if HP_loss[1] > HP_loss[0]:
              if player == "Player 1":
                player_1.update(screen, HP_loss[1])
              else:
                player_2.update(screen, HP_loss[0])
            elif HP_loss[1] == HP_loss[0]:
              num = random.random()
              if num < 0.5:
                player_1.update(screen, HP_loss[1])
              else:
                player_2.update(screen, HP_loss[0])
            elif player == "Player 2":
              player_2.update(screen, HP_loss[0])
            else:
              player_1.update(screen, HP_loss[1])
            
          if abs(x2 - x1) == 2:
            if y2 != y1:
              if y2 > y1 and x2+1 <= 2 and y2+1 <= 2 and containsChar(x2 + 1, y2 + 1):
                HP_loss = gameplay.damage(chargrid[x1][y1],
                                chargrid[x2 + 1][y2 + 1])
                if HP_loss[1] >= HP_loss[0]:
                  if player == "Player 1":
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif HP_loss[1] == HP_loss[0]:
                  num = random.random()
                  if num < 0.5:
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif player == "Player 2":
                  player_2.update(screen, HP_loss[0])
                else:
                  player_1.update(screen, HP_loss[1])
                
              elif containsChar(x2 - 1, y2 - 1) and x2-1 >= 0 and y2-1 >= 0:
                HP_loss = gameplay.damage(chargrid[x1][y1],
                                chargrid[x2 - 1][y2 - 1])
                if HP_loss[1] >= HP_loss[0]:
                  if player == "Player 1":
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif HP_loss[1] == HP_loss[0]:
                  num = random.random()
                  if num < 0.5:
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif player == "Player 2":
                  player_2.update(screen, HP_loss[0])
                else:
                  player_1.update(screen, HP_loss[1])
                
            elif x1 > x2 and containsChar(x1 - 1, y1) and x1-1 >= 0:
              HP_loss = gameplay.damage(chargrid[x1][y1], chargrid[x1 - 1][y1])
              
              if HP_loss[1] >= HP_loss[0]:
                if player == "Player 1":
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif HP_loss[1] == HP_loss[0]:
                num = random.random()
                if num < 0.5:
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif player == "Player 2":
                player_2.update(screen, HP_loss[0])
              else:
                player_1.update(screen, HP_loss[1])
              
            elif containsChar(x1 + 1, y1) and x1+1 <= 2:
              HP_loss = gameplay.damage(chargrid[x1][y1], chargrid[x1 + 1][y1])
              if HP_loss[1] >= HP_loss[0]:
                if player == "Player 1":
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif HP_loss[1] == HP_loss[0]:
                num = random.random()
                if num < 0.5:
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif player == "Player 2":
                player_2.update(screen, HP_loss[0])
              else:
                player_1.update(screen, HP_loss[1])
          
          elif abs(y2 - y1) == 2:
            if x2 != x1:
              if x2 > x1 and containsChar(x2 + 1, y2 + 1) and x2+1 <= 2 and y2+1 <= 2:
                HP_loss = gameplay.damage(chargrid[x1][y1],
                                chargrid[x2 + 1][y2 + 1])
                if HP_loss[1] >= HP_loss[0]:
                  if player == "Player 1":
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif HP_loss[1] == HP_loss[0]:
                  num = random.random()
                  if num < 0.5:
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif player == "Player 2":
                  player_2.update(screen, HP_loss[0])
                else:
                  player_1.update(screen, HP_loss[1])
                
              elif containsChar(x2 - 1, y2 - 1) and x2-1 >= 0 and y2-1 >= 0:
                HP_loss = gameplay.damage(chargrid[x1][y1],
                                chargrid[x2 - 1][y2 - 1])
                if HP_loss[1] >= HP_loss[0]:
                  if player == "Player 1":
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif HP_loss[1] == HP_loss[0]:
                  num = random.random()
                  if num < 0.5:
                    player_1.update(screen, HP_loss[1])
                  else:
                    player_2.update(screen, HP_loss[0])
                elif player == "Player 2":
                  player_2.update(screen, HP_loss[0])
                else:
                  player_1.update(screen, HP_loss[1])
                
            elif y1 > y2 and containsChar(x1, y1 - 1) and y1-1 >= 0:
              HP_loss = gameplay.damage(chargrid[x1][y1], chargrid[x1][y1 - 1])
              if HP_loss[1] >= HP_loss[0]:
                if player == "Player 1":
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif HP_loss[1] == HP_loss[0]:
                num = random.random()
                if num < 0.5:
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif player == "Player 2":
                player_2.update(screen, HP_loss[0])
              else:
                player_1.update(screen, HP_loss[1])
              
            elif containsChar(x1, y1 + 1) and y1+1 <= 2:
              HP_loss = gameplay.damage(chargrid[x1][y1], chargrid[x1][y1 + 1])
              if HP_loss[1] >= HP_loss[0]:
                if player == "Player 1":
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif HP_loss[1] == HP_loss[0]:
                num = random.random()
                if num < 0.5:
                  player_1.update(screen, HP_loss[1])
                else:
                  player_2.update(screen, HP_loss[0])
              elif player == "Player 2":
                player_2.update(screen, HP_loss[0])
              else:
                player_1.update(screen, HP_loss[1])

          currentList.remove(chargrid[x1][y1].name)

        if containsChar(x2, y2) == False:
          chargrid[x2][y2] = chargrid[x1][y1]
          chargrid[x1][y1] = None
          resetGrid()

        pygame.draw.line(screen, (0, 0, 0), (142.5, 142.5), (412.5, 142.5))
        pygame.draw.line(screen, (0, 0, 0), (412.5, 142.5), (412.5, 412.5))
        pygame.draw.line(screen, (0, 0, 0), (412.5, 412.5), (142.5, 412.5))
        pygame.draw.line(screen, (0, 0, 0), (142.5, 142.5), (142.5, 412.5))
        
        for list in chargrid:
          for item in range(0, 3):
            if list[item] != None:
              if list[item].name in currentList:
                drawBorder(list[item].x, list[item].y, (0,255,0))

                pygame.display.update()
        
        if currentList == []:
          turn_count += 1

          if turn_count % 2 == 1:
            player = "Player 1"
          else:
            player = "Player 2"

          if player == "Player 1":
            currentList = choice1.copy()
          else:
            currentList = choice2.copy()

          turn = player + "\'s turn"
          pygame.draw.rect(screen, (0, 0, 255), (142.5, 90, 270, 30))
          draw_text(turn, game_name_font, (0, 0, 0), 230, 100)
          
          w = 0

          for list in chargrid:
            for item in range(0, 3):
              if list[item] != None:
                if list[item].owner == player:
                  list[item].resetMoved(142.5 + 90*item, 142.5 + 90*w)


            w += 1

    pygame.display.update()

    if round(player_1.current_health, 2) <= 0:
      player_1.current_health = 0
      game = False
    if round(player_2.current_health, 2) <= 0:
      player_2.current_health = 0
      game = False

  draw_image("Resources/background.png",
             (0,0),
             scale=(SCREEN_WIDTH, SCREEN_HEIGHT))

  end_game = True

  replay_button = GameButton("Play Again", 100, 50, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 25))

  complete = pygame.mixer.Sound("game_complete.wav")
  complete.play()

  while end_game is True:

    if player_2.current_health >= player_1.current_health:
      draw_text("Player 2 Wins!", game_name_font, (0, 0, 0), 200, 125)
    elif player_1.current_health >= player_2.current_health:
      draw_text("Player 1 Wins!", game_name_font, (0, 0, 0), 200, 125)
    else:
      draw_text("Draw", game_name_font, (0, 0, 0), 200, 125)

    replay_button.draw()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        
    if replay_button.pressed == True:
      end_game = False
      charCount = 0
      choice1 = []
      choice2 = []
      chargrid = [[None, None, None], [None, None, None], [None, None, None]]

    pygame.display.update()
    
pygame.quit()
