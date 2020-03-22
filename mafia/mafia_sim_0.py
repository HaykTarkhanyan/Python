"""
Written by Hayk Tarkhanyan (start date 16.03.2020)

It's simulation of the game Mafia(Warewolf), purpose of which is
to make some conclusion for real life game based on many many iterations in
the simulation.

I make following assumtions here.

1. Mafia decides who to kill randomly, and can't change planes unless Don has
found the Sherif(when Don does, they kill the sherif very next night)
2. No one is leaving game in the morning, unless sherif found mafia.

All this makes the game very unrealistic, but it's a good starting point
"""

import random

# def setup():
#     size(600,200)
#     global all_pl, kills, killed
#     all_pl = split_roles()
#     kills = random.sample(range(10), 3)
#     print (kills)
#     killed = []

# def draw():
#     background(200)
#     # all_pl = split_roles()
#     frameRate(1)
#     print (killed)
#     draw_rects_for_players(all_pl, 50, killed)
#     print (frameCount)

#     if frameCount % 15 == 0:
#         killed.append(kills[0])
#     elif frameCount % 10 == 0:
#         killed.append(kills[1])
#     elif frameCount % 5 == 0:
#         killed.append(kills[2])


class Mafia:
    def __init__(self):
        # first initialize the roles
        self.don = self.split_roles()["Don"]
        self.sherif = self.split_roles()["Sherif"]
        self.black_team = self.split_roles()["Black_team"]
        self.red_team = self.split_roles()["Red_team"]

        # now initialize who will be killed eack night
        self.rasklad = self.choose_rasklad(self.red_team)

    @staticmethod
    def split_roles():
        """
        Functions randomly assignes roles, and returns a dictionary containing
        indexes of every type of player.
        7 Red players(citizens)(1 of which is Sherif), 3 Black players(one Don)

        Output example : {'Sherif': 2, 'Don': 6,
                          'Black_team': [6, 1, 3], 'Red_team': [0, 4, 5, 7, 8, 9]}
        """

        all_rand_indexes = random.sample(range(10), 4)

        sherif_ind = all_rand_indexes[0]
        don_ind = all_rand_indexes[1]
        black_team_indexes = all_rand_indexes[1:4]
        red_team_indexes = [i for i in range(
            10) if i not in black_team_indexes]

        all_players = {"Sherif": sherif_ind,
                       "Don": don_ind,
                       "Black_team": black_team_indexes,
                       "Red_team": red_team_indexes
                       }

        return all_players

    @staticmethod
    def choose_rasklad(red_team):
        """
        Randomly chooses 3 players which are going to be killed
        returns a list

        example output: [2,5,3]
        """
        return random.sample(red_team, 3)


a = Mafia()

# print(len(a.red_team))


def sherifi_stugum(sherif, black_team):
    """
    Sherif has a chance to search for a black player every night

    returns a boolean
    """
    possibilities = list(range(10))
    possibilities.remove(sherif)

    stugum = random.choice(possibilities)

    if stugum in black_team:
        return True
    return False


def doni_stugum(red_team, sherif):
    """
    Don has a chance to search for the sherif every night

    returns a boolean
    """
    stugum = random.choice(red_team)

    if stugum == sherif:
        return True
    return False


# def draw_rects_for_players(all_players, rect_size, removed_player):

#     for i in range(len(all_players)):
#         if i in removed_player:
#             print ("banana")
#             stroke(200)
#             fill(200)

#         elif all_players[i] == "S":
#             fill(0)
#         elif all_players[i] == "K":
#             fill(255,0,0)
#         elif all_players[i] == "Sh":
#             fill(255,255,0)
#         elif all_players[i] == "D":
#             fill(100)

#         rect(50 + rect_size * i, 100, rect_size, rect_size)
