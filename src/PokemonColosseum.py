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
    # print("Welcome to Pokemon Colosseum!")
    print(" _______ _______ ___   _ _______ __   __ _______ __    _   _______ _______ ___     _______ _______ _______ _______ __   __ __   __ ")
    print("|       |       |   | | |       |  |_|  |       |  |  | | |       |       |   |   |       |       |       |       |  | |  |  |_|  |")
    print("|    _  |   _   |   |_| |    ___|       |   _   |   |_| | |       |   _   |   |   |   _   |  _____|  _____|    ___|  | |  |       |")
    print("|   |_| |  | |  |      _|   |___|       |  | |  |       | |       |  | |  |   |   |  | |  | |_____| |_____|   |___|  |_|  |       |")
    print("|    ___|  |_|  |     |_|    ___|       |  |_|  |  _    | |      _|  |_|  |   |___|  |_|  |_____  |_____  |    ___|       |       |")
    print("|   |   |       |    _  |   |___| ||_|| |       | | |   | |     |_|       |       |       |_____| |_____| |   |___|       | ||_|| |")
    print("|___|   |_______|___| |_|_______|_|   |_|_______|_|  |__| |_______|_______|_______|_______|_______|_______|_______|_______|_|   |_|")
    name = input("Enter Player Name: ")
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
        moves = ast.literal_eval(line[7]) if line[7] else [] # convert moves to a list from a string
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
        rand = random.randint(0,(len(pokemon_list)-1))
        new_player.pokemon.append(pokemon_list[rand])
        pokemon_list.pop(rand)
    return new_player

def matchStart (playerA, playerB, moves_list) :
    healthy_fighters = True
    cointoss = random.randint(0,1)
    turn = 0
    print("====> Team Rocket enters with " + playerB.pokemon[0].name + ", " + playerB.pokemon[1].name + " and " + playerB.pokemon[2].name + " <====")
    print("====> Team", playerA.name, "enters with " + playerA.pokemon[0].name + ", " + playerA.pokemon[1].name + " and " + playerA.pokemon[2].name + " <====")
    print("A coin toss will determine who starts first.")
    if cointoss == 0:
        print("The coin lands on heads! Team", playerA.name, "will start first!")
        turn = 0
    else: 
        print("The coin lands on tails! Team", playerB.name, "will start first!")
        turn = 1
    print("----------------")
    print("Let the battle begin!")
    while(healthy_fighters):
        # each loop starts a new turn
        # i need to know what pokemon are on the field at the given time
        playerAPokemon = playerA.pokemon[0]
        playerBPokemon = playerB.pokemon[0]
        turn = doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon, moves_list)
        updateGameState(playerA, playerB)
        healthy_fighters = checkGameState(playerA, playerB)

def doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon, moves_list):
    if turn == 0:
        move_choice = doPlayerTurn(playerAPokemon)
        doCombat(move_choice, playerA, playerB, playerAPokemon, playerBPokemon, moves_list)
        return 1
    else:
        move_choice = random.randint(1,len(playerBPokemon.move_queue))
        doCombat(move_choice, playerB, playerA, playerBPokemon, playerAPokemon, moves_list)
        return 0

def doPlayerTurn (current_pokemon) :
    i = 1
    print("==================================")
    print("Choose a move for " + current_pokemon.name)
    print("==================================")
    for moves in current_pokemon.move_queue:
        print("| " + str(i) + ". " + current_pokemon.move_queue[i-1] )
        i += 1
    print("==================================")
    while True:
        try:
            move_choice = int(input("Choose a move: "))
            if move_choice in {1, 2, 3, 4, 5}:  
                break 
            else:
                print("Invalid input. Please try again.") 
        except ValueError:
            print("Invalid input. Please enter a number.") 
    
    return move_choice

def doCombat (move_choice, attacker, defender, attackerPokemon, defenderPokemon, moves_list) :
    print(">>> " + attackerPokemon.name + " uses " + attackerPokemon.move_queue[move_choice - 1] + " on " + defenderPokemon.name + ":")
    doDamage(move_choice, attackerPokemon, defenderPokemon, moves_list)
    attackerPokemon.move_queue.pop(move_choice - 1)
    checkMoveQueue(attackerPokemon)
    if defenderPokemon.hp < 1 :
        print(defenderPokemon.name + " has been knocked out, and returns to it's Pokeball!")
        updateGameState(attacker, defender)
        checkGameState(attacker, defender)
        print("Team " + defender.name + "'s " + defender.pokemon[0].name + " enters the battle!")
    else :
        print(defenderPokemon.name + " now has", defenderPokemon.hp, "hp points")
    print("~~~~~~")

def doDamage (move_choice, attackerPokemon, defenderPokemon, moves_list) :
    move = attackerPokemon.move_queue[move_choice - 1]
    move_info = getMoveInfo(move, moves_list)
    stab = getSTAB(attackerPokemon, move_info)
    type_efficiency = getTypeEfficiency(move_info, defenderPokemon)
    damage = int(int(move_info.power) * (attackerPokemon.attack / defenderPokemon.defense) * stab * type_efficiency * random.uniform(0.5, 1))
    defenderPokemon.hp -= damage
    if type_efficiency == 2 :
        print("It's super effective!")
    if type_efficiency == .5 :
        print("It's not very effective...")
    print(defenderPokemon.name + " takes " + str(damage) + " damage!")

def getMoveInfo (move, moves_list) :
    for e in moves_list:
        if e.name == move:
            return e

def getSTAB(attackerPokemon, move_info) :
    if attackerPokemon.power_type == move_info.move_type:
        return 1.5
    return 1

def getTypeEfficiency (move_info, defenderPokemon) :
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
        case _ :
            return 1

def updateGameState(playerA, playerB):
    if (playerA.pokemon[0].hp < 1):
        playerA.pokemon.pop(0)
    if (playerB.pokemon[0].hp < 1):
        playerB.pokemon.pop(0)

def checkMoveQueue(pokemon) :
    if len(pokemon.move_queue) == 0 :
        pokemon.move_queue = copy.deepcopy(pokemon.moves)

def checkGameState (playerA, playerB):
    if len(playerA.pokemon) == 0:
        print("Team " + playerA.name + " has no more useable Pokemon. Team " + playerB.name + " wins!")
        sys.exit(0)
        return False
    if len(playerB.pokemon) == 0:
        print("Team " + playerB.name + " has no more useable Pokemon. Team " + playerA.name + " wins!")
        sys.exit(0)
        return False
    return True

main()