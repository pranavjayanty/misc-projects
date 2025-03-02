# human_player.py
from player import Player

class HumanPlayer(Player):
    def make_move(self, opponent):
        valid_attacks = {f"{h}{o}" for h, o in [('t', 't'), ('t', 'b'), ('b', 't'), ('b', 'b')] 
                         if (h == 't' and self.top > 0 or h == 'b' and self.bottom > 0) and 
                            (o == 't' and opponent.top > 0 or o == 'b' and opponent.bottom > 0)}
        
        while True:
            action = input("Move (a for attack, s for split): ").lower().strip()
            
            if action == 'a':
                attack = input(f"Attack ({', '.join(valid_attacks)}): ").lower().strip()
                if attack in valid_attacks:
                    my_hand, opp_hand = attack[0], attack[1]
                    my_value = self.top if my_hand == 't' else self.bottom
                    opp_value = opponent.top if opp_hand == 't' else opponent.bottom
                    new_value = my_value + opp_value
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    # Map 't' to 'top' and 'b' to 'bottom'
                    opp_hand_attr = 'top' if opp_hand == 't' else 'bottom'
                    setattr(opponent, opp_hand_attr, new_value)
                    print(f"{self.name} attacks.")
                    return
                print(f"Invalid attack. Valid options: {', '.join(valid_attacks)}")
                continue
            
            elif action == 's':
                total = self.total_fingers()
                possible_splits = [(m['top'], m['bottom']) for m in self.get_possible_moves(opponent) if m['type'] == 'split']
                if not possible_splits:
                    print("No valid splits possible.")
                    continue
                top_str = input("Top hand chopsticks (0-4, q to quit): ").lower().strip()
                if top_str == 'q':
                    continue
                try:
                    top = int(top_str)
                    bottom = total - top
                    if (top, bottom) in possible_splits:
                        self.set_hands(top, bottom)
                        print(f"{self.name} splits.")
                        return
                    print("Invalid split.")
                except ValueError:
                    print("Enter a number (0-4) or 'q'.")
            else:
                print("Invalid move. Use 'a' or 's'.")
