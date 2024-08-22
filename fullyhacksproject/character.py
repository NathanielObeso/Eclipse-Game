

# Kimono Characters
characters = {"kimono_rogue": {
    'kimono': True, 
    'paper': 5, 
    'rock': 1, 
    'scissors': 1
  },
                
"kimono_knight": {
    'kimono': True, 
    'paper': 3, 
    'rock': 2, 
    'scissors': 2
  },
                
"kimono_monk": {
    'kimono': True, 
    'paper': 2.3, 
    'rock': 2.3, 
    'scissors': 2.3
  },

# Authority Characters
"authority_rogue": {
    'authority': True, 
    'rock': 5, 
    'paper': 1, 
    'scissors': 1
  },
                
"authority_knight": {
    'authority': True, 
    'rock': 3, 
    'paper': 2, 
    'scissors': 2
  },
                
"authority_monk": {
    'authority': True,
    'rock': 2.3,
    'paper': 2.3,
    'scissors': 2.3
  },

# Maniacs Characters
"maniac_rogue": {
    'maniac': True,
      'scissors': 5,
      'paper': 1,
      'rock': 1
  },
                
"maniac_knight": {
      'maniac': True,
      'scissors': 3,
      'paper': 2,
      'rock': 2
  },
                
"maniac_monk": {
      'maniac': True,
      'scissors': 2.3,
      'paper': 2.3,
      'rock': 2.3
  }}

def convertCharToStats(character):
  low = character.lower()
  charName = low.replace(" ", "_")
  stats = characters[charName]
  return stats