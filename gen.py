nouns = """
Clothing
Message
Sound
Paper
Market
Government
"Tea or Coffee"
Keys
Dragons
Dungeons
Babies
Names
Education
Graphs
Inventory
Time
Memes
Taxes
Clippy
Globe
Phones
Security
Dates
Weather
Turtles
Numbers
Hats
Muppets
Debts
"File system"
Sharks
Consoles
Conversations
Handicap""".strip().split("\n")

Adjectives = """
Gooey
Quirkly
Modest
Cloudy
Overdone
Xkcd
"Motion Graphics-y"
Zen
Background
Villainous
"Old School"
Imaginative""".strip().split("\n")

import random

def generate():
    word1 = random.choice(nouns)
    word2 = word1

    while word1 == word2:
        word2 = random.choice(nouns)

    adjective = random.choice(Adjectives)

    return "%s %s %s" % (adjective, word1, word2)

choice = "Y"
number = 0
while choice.upper() != "N":
    number += 1
    print ("\n%s\n" % generate())
    choice = raw_input("Type N to stop: ")

    if number == 2:
       print ("Teenage Ninja Turtles") # just for the presentation
       choice = raw_input("Type N to stop: ")