import csv
import ast
import random
import sys
import copy
from Pokemon import *
from Player import *
from Move import *


def main () :
    pokemon_data = '../data/pokemon-data.csv'
    moves_data = '../data/moves-data.csv'
    pokemon_list = loadPokemon(pokemon_data)
    moves_list = loadMoves(moves_data)
    print("\n")
    print("█▀█ █▀█ █▄▀ █▀▀ █▀▄▀█ █▀█ █▄░█   █▀▀ █▀█ █░░ █▀█ █▀ █▀ █▀▀ █░█ █▀▄▀█")
    print("█▀▀ █▄█ █░█ ██▄ █░▀░█ █▄█ █░▀█   █▄▄ █▄█ █▄▄ █▄█ ▄█ ▄█ ██▄ █▄█ █░▀░█")
    print("\n")
    print("> Hello, and welcome to the Pokemon Colosseum! My name is Professor Cam, and you must be... erm.. what was your name again?")
    name = input(">> Enter Player Name: ")
    print("> Ah, right! Of course, you're " + name + "!")
    print("> In just a moment, you'll enter the colosseum with a team of three Pokemon to battle against a strong foe. A coin toss will determine who starts first.")
    # instantiate players
    player = constructPlayer(name, pokemon_list)
    badGuy = constructPlayer("Rocket", pokemon_list)
    matchStart(player, badGuy, moves_list)

def loadPokemon (csv_file) :
    pokemon = []
    try:
        f = open (csv_file, 'r')
    except IOError:
        print ('Cannot open file')
    lines = csv.reader(f)
    next(f)
    for line in lines:
        moves = ast.literal_eval(line[7]) if line[7] else [] # convert moves to a list from a string so data can be used
        new_pokemon = Pokemon(line[0], line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), moves)
        pokemon.append(new_pokemon) 
    f.close()
    return pokemon

def loadMoves (csv_file) :
    moves = []
    try:
        f = open (csv_file, 'r')
    except IOError:
        print ('Cannot open file')
    lines = csv.reader(f)
    next(f)
    for line in lines:
        new_move = Move(*line) 
        moves.append(new_move) 
    f.close()
    return moves

def constructPlayer (name, pokemon_list) :
    new_player = Player(name, [])
    for i in range(1,4):
        rand = random.randint(0,(len(pokemon_list)-1)) # get a random number in a range of total number of pokemon
        new_player.pokemon.append(pokemon_list[rand]) # add the random pokemon to the queue for this player
        pokemon_list.pop(rand) # removes the added pokemon from the total list to prevent duplicates
    return new_player

def matchStart (playerA, playerB, moves_list) :
    healthy_fighters = True
    cointoss = random.randint(0,1)
    turn = 0
    
    if cointoss == 0:
        print("The coin lands on heads, so Team", playerA.name, "will start first!")
        turn = 0
    else: 
        print("The coin lands on tails, so Team", playerB.name, "will start first!")
        turn = 1
    print("\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ Let the battle begin! ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n")
    print("====> Team Rocket enters with " + playerB.pokemon[0].name + ", " + playerB.pokemon[1].name + " and " + playerB.pokemon[2].name + " <====")
    print("====> Team", playerA.name, "enters with " + playerA.pokemon[0].name + ", " + playerA.pokemon[1].name + " and " + playerA.pokemon[2].name + " <====")
    print("\n")
    while(healthy_fighters):
        # Each loop starts a new turn
        playerAPokemon = playerA.pokemon[0]
        playerBPokemon = playerB.pokemon[0]
        turn = doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon, moves_list)
        updateGameState(playerA, playerB) # make sure all available pokemon are healthy
        healthy_fighters = checkGameState(playerA, playerB) # Keep the loop running until game state finishes

def doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon, moves_list):
    if turn == 0: # Players turn
        move_choice = doPlayerTurn(playerAPokemon, playerBPokemon) # get a user input
        doCombat(move_choice, playerA, playerB, playerAPokemon, playerBPokemon, moves_list)
        return 1
    else: # NPC turn
        move_choice = random.randint(1,len(playerBPokemon.move_queue))
        doCombat(move_choice, playerB, playerA, playerBPokemon, playerAPokemon, moves_list)
        return 0

def doPlayerTurn (current_pokemon, opponent_pokemon) :
    i = 1
    print("==================================")
    print("Choose a move for " + current_pokemon.name + " to use against " + opponent_pokemon.name + " (" + str(opponent_pokemon.hp) + "hp)")
    print("==================================")
    for moves in current_pokemon.move_queue:
        print("║ " + str(i) + ". " + current_pokemon.move_queue[i-1] )
        i += 1
    print("==================================")
    while True: # validate input
        try:
            move_choice = input("Choose a move: ")
            if "run" in move_choice.lower(): # for fun...
                print("You can't run from a Pokemon battle!")
            elif int(move_choice) in {1, 2, 3, 4, 5}:  
                break 
            else:
                print("Invalid input. Please try again.") 
        except ValueError:
            print("Invalid input. Please enter a number.") 
    print("\n")
    return int(move_choice)

def doCombat (move_choice, attacker, defender, attackerPokemon, defenderPokemon, moves_list) :
    print(">>> " + attackerPokemon.name + " uses " + attackerPokemon.move_queue[move_choice - 1] + " on " + defenderPokemon.name + ":")
    doDamage(move_choice, attackerPokemon, defenderPokemon, moves_list)
    # Uses move queue here so we can remove used moves throughout the battle
    attackerPokemon.move_queue.pop(move_choice - 1)
    # Do a clean up effort for the move queue in case it's empty
    checkMoveQueue(attackerPokemon)
    # If a pokemon has fainted... 
    if defenderPokemon.hp < 1 :
        print(defenderPokemon.name + " has been knocked out, and returns to it's Pokeball!")
        updateGameState(attacker, defender)
        checkGameState(attacker, defender)
        print("Team " + defender.name + "'s " + defender.pokemon[0].name + " enters the battle!")
    else :
        print(defenderPokemon.name + " now has", defenderPokemon.hp, "hp points")
    print("\n")

def doDamage (move_choice, attackerPokemon, defenderPokemon, moves_list) :
    # The main damage dealing method. Get some data and move properties first
    move = attackerPokemon.move_queue[move_choice - 1]
    move_info = getMoveInfo(move, moves_list)
    stab = getSTAB(attackerPokemon, move_info)
    type_efficiency = getTypeEfficiency(move_info, defenderPokemon)
    # Use the damage algorithm to calculate how much HP to subtract from defender
    damage = int(int(move_info.power) * (attackerPokemon.attack / defenderPokemon.defense) * stab * type_efficiency * random.uniform(0.5, 1))
    defenderPokemon.hp -= damage
    if type_efficiency == 2 :
        print("It's super effective!")
    if type_efficiency == .5 :
        print("It's not very effective...")
    print(defenderPokemon.name + " takes " + str(damage) + " damage!")

def getMoveInfo (move, moves_list) :
    # Returns full move info node for the provided move name
    for e in moves_list:
        if e.name == move:
            return e

def getSTAB(attackerPokemon, move_info) :
    # Get the STAB property if applicable
    if attackerPokemon.power_type == move_info.move_type:
        return 1.5
    return 1

def getTypeEfficiency (move_info, defenderPokemon) :
    # Get the efficiency stat modifier. Nothing too special here, just some comparative stuff
    match move_info.move_type :
        case "Fire" :
            if defenderPokemon.power_type == "Fire" or defenderPokemon.power_type == "Water":
                return .5
            if defenderPokemon.power_type == "Grass" :
                return 2
            return 1
        case "Water" :
            if defenderPokemon.power_type == "Water" or defenderPokemon.power_type == "Grass" :
                return .5
            if defenderPokemon.power_type == "Fire" :
                return 2
            return 1
        case "Electric" :
            if defenderPokemon.power_type == "Electric" or defenderPokemon.power_type == "Grass" :
                return .5
            if defenderPokemon.power_type == "Water" :
                return 2
            return 1
        case "Grass" :
            if defenderPokemon.power_type == "Fire" or defenderPokemon.power_type == "Grass" :
                return .5
            if defenderPokemon.power_type == "Water" :
                return 2
            return 1
        case _ : # everything else (including Normal) has no modifier
            return 1

def updateGameState(playerA, playerB):
    # This is a cleanup service. Check to make sure that the pokemon at the front of the queue for each player has HP remaining, and remove it if not
    if (playerA.pokemon[0].hp < 1):
        playerA.pokemon.pop(0)
    if (playerB.pokemon[0].hp < 1):
        playerB.pokemon.pop(0)

def checkMoveQueue(pokemon) :
    # If the move queue is empty, refill it from the total list of moves
    if len(pokemon.move_queue) == 0 :
        pokemon.move_queue = copy.deepcopy(pokemon.moves)

def checkGameState (playerA, playerB):
    # Checks to see if either player has no remaining pokemon and ends the game if so
    if len(playerA.pokemon) == 0:
        print("> Team " + playerA.name + " has no more useable Pokemon. Team " + playerB.name + " wins!")
        sys.exit(0)
        return False
    if len(playerB.pokemon) == 0:
        print("> Team " + playerB.name + " has no more useable Pokemon. Team " + playerA.name + " wins!")
        sys.exit(0)
        return False
    return True

main()