import random
from player import Player

class ComputerPlayer(Player):
    def __init__(self, name, difficulty):
        super().__init__(name)
        self.difficulty = difficulty

    def make_move(self, opponent):
        moves = self.get_possible_moves(opponent)
        if self.difficulty == 'e':
            move = random.choice(moves)
        elif self.difficulty == 'm':
            knockouts = [m for m in moves if m['type'] == 'attack' and 
                         getattr(self, m['hand']) + getattr(opponent, m['opp_hand']) == 5]
            revive_splits = [m for m in moves if m['type'] == 'split' and 
                            (self.top == 0 or self.bottom == 0) and m['top'] > 0 and m['bottom'] > 0]
            move = random.choice(knockouts or revive_splits or moves)
        else:  # Hard
            best_move, best_value = None, -float('inf')
            for move in moves:
                if move['type'] == 'attack':
                    hand, opp_hand = move['hand'], move['opp_hand']
                    original = getattr(opponent, opp_hand)
                    new_value = original + getattr(self, hand)
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(opponent, opp_hand, new_value)
                    value = self.minimax(self, opponent, 3, False)
                    setattr(opponent, opp_hand, original)
                else:
                    original_top, original_bottom = self.top, self.bottom
                    self.set_hands(move['top'], move['bottom'])
                    value = self.minimax(self, opponent, 3, False)
                    self.set_hands(original_top, original_bottom)
                if value > best_value:
                    best_value = value
                    best_move = move
            move = best_move
        
        if move['type'] == 'attack':
            attack_value = getattr(self, move['hand'])
            new_value = getattr(opponent, move['opp_hand']) + attack_value
            if new_value == 5:
                new_value = 0
            elif new_value > 5:
                new_value -= 5
            setattr(opponent, move['opp_hand'], new_value)
            print(f"{self.name} attacks.")
        else:
            self.set_hands(move['top'], move['bottom'])
            print(f"{self.name} splits.")

    def minimax(self, player, opponent, depth, is_maximizing):
        if depth == 0 or player.is_defeated() or opponent.is_defeated():
            return 1 if opponent.is_defeated() else -1 if player.is_defeated() else 0
        moves = player.get_possible_moves(opponent)
        if is_maximizing:
            best_value = -float('inf')
            for move in moves:
                if move['type'] == 'attack':
                    original = getattr(opponent, move['opp_hand'])
                    new_value = original + getattr(player, move['hand'])
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(opponent, move['opp_hand'], new_value)
                    value = self.minimax(player, opponent, depth - 1, False)
                    setattr(opponent, move['opp_hand'], original)
                else:
                    original_top, original_bottom = player.top, player.bottom
                    player.set_hands(move['top'], move['bottom'])
                    value = self.minimax(player, opponent, depth - 1, False)
                    player.set_hands(original_top, original_bottom)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in opponent.get_possible_moves(player):
                if move['type'] == 'attack':
                    original = getattr(player, move['opp_hand'])
                    new_value = original + getattr(opponent, move['hand'])
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(player, move['opp_hand'], new_value)
                    value = self.minimax(player, opponent, depth - 1, True)
                    setattr(player, move['opp_hand'], original)
                else:
                    original_top, original_bottom = opponent.top, opponent.bottom
                    opponent.set_hands(move['top'], move['bottom'])
                    value = self.minimax(player, opponent, depth - 1, True)
                    opponent.set_hands(original_top, original_bottom)
                best_value = min(best_value, value)
            return best_value
    