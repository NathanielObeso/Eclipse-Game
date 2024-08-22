import character


def attack(char_1, char_2):
  damage_multipler = (2, 0.5)
  character_1 = character.convertCharToStats(char_1)
  character_2 = character.convertCharToStats(char_2)
  damage_total_1 = 0
  damage_total_2 = 0
  types = [x for x in character_1 if x != 'kimono' and x != 'authority' and x != 'maniac']
  types2 = [x for x in character_2 if x != 'kimono' and x != 'authority' and x != 'maniac']
  
  if types == types2:
    damage_total_1 += character_1[types[0]] + character_1[types[1]] * 2
    damage_total_2 += character_2[types[0]] + character_2[types[1]] * 2
  elif ('kimono' in character_1 and 'authority' in character_2
        or 'authority' in character_1 and 'maniac' in character_2
        or 'maniac' in character_1 and 'kimono' in character_2):
    damage_total_1 += character_1[types[0]] * damage_multipler[0]
    damage_total_1 += character_1[types[1]] * 2
    damage_total_2 += character_2[types2[0]] * damage_multipler[1]
    damage_total_2 += character_2[types2[1]] * 2
  elif ('authority' in character_1 and 'kimono' in character_2
        or 'maniac' in character_1 and 'authority' in character_2
        or 'kimono' in character_1 and 'maniac' in character_2):
    damage_total_1 += character_1[types[0]] * damage_multipler[1]
    damage_total_1 += character_1[types[1]] * 2
    damage_total_2 += character_2[types2[0]] * damage_multipler[0]
    damage_total_2 += character_2[types2[1]] * 2

  return (damage_total_1, damage_total_2)