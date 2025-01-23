import csv
import ast
import random
from Pokemon import *
from Player import *
from Move import *


def main () :
    pokemon_data = '../data/pokemon-data.csv'
    moves_data = '../data/moves-data.csv'
    pokemon_list = loadPokemon(pokemon_data)
    moves_list = loadMoves(moves_data)
    print("Welcome to Pokemon Colosseum!")
    name = input("Enter Player Name: ")
    player = constructPlayer(name, pokemon_list)
    badGuy = constructPlayer("Team Rocket", pokemon_list)
    matchStart(player, badGuy)

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

def matchStart (playerA, playerB) :
    healthy_fighters = True
    cointoss = random.randint(0,1)
    turn = 0
    print("Team Rocket enters with " + playerB.pokemon[0].name + ", " + playerB.pokemon[1].name + " and " + playerB.pokemon[2].name)
    print("Team", playerA.name, "enters with " + playerA.pokemon[0].name + ", " + playerA.pokemon[1].name + " and " + playerA.pokemon[2].name)
    if cointoss == 0:
        print("Team", playerA.name, "will start first!")
        turn = 0
    else: 
        print(playerB.name, "will start first!")
        turn = 1
    print("Let the battle begin!")
    while(healthy_fighters):
        # each loop starts a new turn
        # i need to know what pokemon are on the field at the given time
        playerAPokemon = playerA.pokemon[0]
        playerBPokemon = playerB.pokemon[0]
        turn = doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon)
        updateGameState(playerA, playerB)
        healthy_fighters = checkGameState(playerA, playerB)

def doTurn(turn, playerA, playerB, playerAPokemon, playerBPokemon):
    if turn == 0:
        move_choice = doPlayerTurn(playerAPokemon)
        doCombat(move_choice, playerA, playerB, playerAPokemon, playerBPokemon)
        return 1
    else:
        move_choice = random.randint(1,4)
        doCombat(move_choice, playerA, playerB, playerBPokemon, playerAPokemon)
        return 0

def doPlayerTurn (current_pokemon) :
    print("Choose a move for " + current_pokemon.name)
    print("1. ", current_pokemon.moves[0])
    print("2. ", current_pokemon.moves[1])
    print("3. ", current_pokemon.moves[2])
    print("4. ", current_pokemon.moves[3])
    while True:
        try:
            move_choice = int(input("Choose a move: "))
            if move_choice in {1, 2, 3, 4}:  
                break 
            else:
                print("Invalid input. Please choose a number between 1 and 4.") 
        except ValueError:
            print("Invalid input. Please enter a number.") 
    
    return move_choice

def doCombat (move_choice, attacker, defender, attackerPokemon, defenderPokemon) :
    print(attackerPokemon.name + " uses " + attackerPokemon.moves[move_choice - 1] + " on " + defenderPokemon.name)
    # temp stuff here...
    # need to reference actual move dictionary here and make all of the appropriate algorithmic calculations.
    defenderPokemon.hp = defenderPokemon.hp - 25
    
    print("Damage done to " + defenderPokemon.name)
    print(defenderPokemon.name + " now has", defenderPokemon.hp, "hp points")

def updateGameState(playerA, playerB):
    if (playerA.pokemon[0].hp < 1):
        playerA.pokemon.pop(0)
    if (playerB.pokemon[0].hp < 1):
        playerB.pokemon.pop(0)    

def checkGameState (playerA, playerB):
    if len(playerA.pokemon) == 0:
        print("Player A loses")
        return False
    if len(playerB.pokemon) == 0:
        print("Player B loses")
        return False
    return True

main()