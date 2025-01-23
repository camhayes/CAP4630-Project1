class Pokemon:
    def __init__ (self, name, power_type, hp, attack, defense, height, weight, moves) : 
        self.name = name
        self.power_type = power_type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.height = height
        self.weight = weight
        self.moves = moves
        self.move_queue = moves
