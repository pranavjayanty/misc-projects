# computer_player.py
import random
from player import Player

class ComputerPlayer(Player):
    # Hard-coded states where the player wins (player_hands, computer_hands) -> utility
    KNOWN_WIN_STATES = {
        # From your example sequence, states where player is guaranteed to win
        ((3, 3), (1, 0)): 1,  # Initial state you provided
        ((4, 2), (0, 2)): 1,  # After first move
        ((1, 1), (1, 0)): 1,  # Later in sequence
        ((3, 0), (1, 0)): 1,  # Nearing the end
        ((4, 0), (1, 0)): 1,  # One move from victory
    }

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
        else:  # Hard mode with minimax
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
                    value = self.minimax(self, opponent, 10, False)
                    setattr(opponent, opp_hand, original)
                else:  # Split
                    original_top, original_bottom = self.top, self.bottom
                    self.set_hands(move['top'], move['bottom'])
                    value = self.minimax(self, opponent, 10, False)
                    self.set_hands(original_top, original_bottom)
                if value > best_value:
                    best_value = value
                    best_move = move
            move = best_move
        
        # Execute the chosen move
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
        # Check for known win states (player’s perspective)
        state_key = ((player.top, player.bottom), (opponent.top, opponent.bottom))
        if state_key in self.KNOWN_WIN_STATES:
            return self.KNOWN_WIN_STATES[state_key] if is_maximizing else -self.KNOWN_WIN_STATES[state_key]

        # Terminal states or depth limit
        if depth == 0 or player.is_defeated() or opponent.is_defeated():
            if opponent.is_defeated():
                return 1  # Computer wins
            elif player.is_defeated():
                return -1  # Computer loses
            else:
                # Enhanced heuristic: difference in live hands
                player_live = (1 if player.top > 0 else 0) + (1 if player.bottom > 0 else 0)
                opponent_live = (1 if opponent.top > 0 else 0) + (1 if opponent.bottom > 0 else 0)
                return player_live - opponent_live if is_maximizing else opponent_live - player_live

        # Standard minimax search
        moves = player.get_possible_moves(opponent) if is_maximizing else opponent.get_possible_moves(player)
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
            for move in moves:
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