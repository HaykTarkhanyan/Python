# unfinished, messy, perhaps will never fix

import random
from collections import Counter

#decide play with code or friend
def choose_game_mode():
  choice = input("If you want play with friend write F:  \n if with my code write AI:  \n if you want to play with computer write C:  ")

  if choice.upper()=="FRIEND" or choice.upper()=="F":
    #game_with_human()
    pass
    #code for playing with Friend
  elif choice.upper()=="AI":
    #game_with_AI()
    pass
    #code for playing with AI
  elif choice.upper()=="C" or choice.upper=="COMPUTER":
    game_with_computer()
  else:
    print ("Sorry, yout input is invalid")
    choose_game_mode()
#messeages that should show in the begining

#first_number = int(input("Input your number: "))
#number_of_digits = len(str#(first_number))
  
#select first number for computer
def generate_random_number(number_of_digits):
  all_values = [x for x in range(10**(number_of_digits-1),10**number_of_digits)]
  ai_first_number = random.choice(all_values)
  if check_if_number_is_valid(ai_first_number,number_of_digits)!=False:
    return ai_first_number
  else:
    return generate_random_number(number_of_digits)
#generator works properly


def check_if_number_is_valid(number,number_of_digits): #checing if number dont contain same digits"
    number = str(number)
    checker = Counter(number)
    if len(checker) < len(number):
      return False
     # check if new number isn't same length as first one
    if len(number)!=number_of_digits:
      return False

def count_similarity(x,y):
  if  check_if_number_is_valid(x,len(y))==False:
    pass
  else:  
    cows = 0
    bulls = 0
    number_of_digits = len(str(x))
    for i in range(number_of_digits):
      if str(x)[i] in str(y): #find how many digits of one number are in the other one
        cows += 1
      if str(x)[i]==str(y)[i]: # find how many numbers match
        bulls += 1
    return cows, bulls

def check_if_player_won(x,y):
  if count_similarity(x,y) == (len(str(x)),len(str(x))):
    return True
  else:
    return False

def check_if_player_lose(n):
  if n>=10:
    return True

def game_with_computer():
  checker = 0
  fix_wrong_number_counter = 0
  #start_game()
  y = input("Input your number: ")
  number_of_digits = len(str(y))
  x = generate_random_number(len(str(y)))
  #print (x)
  if check_if_player_won(x,y)==True:
    checker = 1
    print  ("CONGRATULATIONS you won from first try")
    
  if check_if_number_is_valid(y,number_of_digits) == False:
      print ("Your number doesn't satisfy to game rules")
      #fix_wrong_number_counter+=1
      checker = 1
  if checker == 0:
    print(count_similarity(x,y))
  
  for counter in range(100):

    if check_if_player_won(x,y)==True:
      print  ("CONGRATULATIONS you won from " + str(counter+1-fix_wrong_number_counter) + " tries")
      break
    elif check_if_player_lose(counter) == True:
      print ("Right number was " + str(x))
      break
  
    else:
      y = input("Input your number: ")
      #print (check_if_number_is_valid(y,number_of_digits))
      if check_if_number_is_valid(y,number_of_digits) == False:
        print ("Your number doesn't satisfy to game rules")
        fix_wrong_number_counter+=1
        continue
      else:
        print (count_similarity(x,y))
        #print (counter+1)
       # print (34)
  


#print (check_if_number_is_valid(123,4))

#game_with_computer()
choose_game_mode()
















#overall picture
#"""choose_game_mode()
