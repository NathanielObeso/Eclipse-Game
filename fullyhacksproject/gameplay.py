#type: ignore

import pygame

import calculation


def damage(char_1, char_2):
  char1_damage = calculation.attack(char_1.name, char_2.name)[0]
  char2_damage = calculation.attack(char_1.name, char_2.name)[1]

  return (char1_damage, char2_damage)

class Player():
  
  def __init__(self, player, x, y):
    self.name = player
    self.current_health = 200
    self.max_health = 200
    self.health_bar_length = 150
    self.health_ratio = self.max_health / self.health_bar_length
    self.position = (x, y)

  def update(self, screen, HP):
    self.current_health -= HP
    self.basic_health(screen)

  def basic_health(self, screen):
    HP = self.current_health/self.health_ratio
    health = pygame.Rect(self.position[0], self.position[1], HP, 25)
    pygame.draw.rect(screen, (255,255,255), (self.position[0], self.position[1], self.health_bar_length, 25))
    pygame.draw.rect(screen, (255,0,0), health)
