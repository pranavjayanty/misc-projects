import random

# Base Player class to manage hand states
class Player:
    def __init__(self, name):
        self.name = name
        self.top = 1  # Top hand starts with 1 finger
        self.bottom = 1  # Bottom hand starts with 1 finger

    def get_hands(self):
        return (self.top, self.bottom)

    def set_hands(self, top, bottom):
        self.top = top if top < 5 else 0
        self.bottom = bottom if bottom < 5 else 0

    def is_defeated(self):
        return self.top == 0 and self.bottom == 0

    def total_fingers(self):
        return self.top + self.bottom

    def get_possible_moves(self, opponent):
        moves = []
        # Attack moves
        for hand in ['top', 'bottom']:
            if getattr(self, hand) > 0:
                for opp_hand in ['top', 'bottom']:
                    if getattr(opponent, opp_hand) > 0:
                        moves.append({'type': 'attack', 'hand': hand, 'opp_hand': opp_hand})
        # Split moves with no inverts
        total = self.total_fingers()
        for a in range(5):
            b = total - a
            if (0 <= b <= 4 and 
                (a, b) != (self.top, self.bottom) and  # Not the same as current
                (a, b) != (self.bottom, self.top)):     # Not an invert
                moves.append({'type': 'split', 'top': a, 'bottom': b})
        return moves

# HumanPlayer class with single-letter commands, infinite scroll, and no inverts
class HumanPlayer(Player):
    def make_move(self, opponent):
        while True:
            action = input("Choose action: ").lower()
            if action == 'a':
                while True:
                    hand = input("Choose your hand: ").lower()
                    if hand in ['t', 'b']:
                        if (hand == 't' and self.top > 0) or (hand == 'b' and self.bottom > 0):
                            break
                        else:
                            print("Your chosen hand must have at least 1 chopstick.")
                    else:
                        print("Invalid choice. Choose 't' or 'b'.")
                while True:
                    opp_hand = input("Choose opponent's hand: ").lower()
                    if opp_hand in ['t', 'b']:
                        if (opp_hand == 't' and opponent.top > 0) or (opp_hand == 'b' and opponent.bottom > 0):
                            break
                        else:
                            print("Opponent's chosen hand must have at least 1 chopstick.")
                    else:
                        print("Invalid choice. Choose 't' or 'b'.")
                attack_value = self.top if hand == 't' else self.bottom
                opp_hand_value = opponent.top if opp_hand == 't' else opponent.bottom
                new_value = attack_value + opp_hand_value
                if new_value == 5:
                    new_value = 0  # Knocked out only if exactly 5
                elif new_value > 5:
                    new_value -= 5  # Infinite scroll: subtract 5 if over
                if opp_hand == 't':
                    opponent.top = new_value
                else:
                    opponent.bottom = new_value
                print(f"{self.name} attacks.")
                break
            elif action == 's':
                total = self.total_fingers()
                while True:
                    try:
                        top_str = input(f"Enter chopsticks for top hand: ")
                        top = int(top_str)
                        bottom = total - top
                        if (0 <= top <= 4 and 0 <= bottom <= 4 and 
                            (top, bottom) != (self.top, self.bottom) and 
                            (top, bottom) != (self.bottom, self.top)):
                            self.top = top
                            self.bottom = bottom
                            print(f"{self.name} splits.")
                            break
                        else:
                            print("Invalid split. Must be 0-4, different from current, and not an invert).")
                    except ValueError:
                        print("Please enter an integer.")
                break
            else:
                print("Invalid action. Choose 'a' or 's'.")

# ComputerPlayer class with infinite scroll and no inverts
class ComputerPlayer(Player):
    def __init__(self, name, difficulty):
        super().__init__(name)
        self.difficulty = difficulty

    def make_move(self, opponent):
        if self.difficulty == 'e':
            self.easy_move(opponent)
        elif self.difficulty == 'm':
            self.medium_move(opponent)
        elif self.difficulty == 'h':
            self.hard_move(opponent)

    def easy_move(self, opponent):
        if random.choice([True, False]):
            possible_hands = [hand for hand in ['top', 'bottom'] if getattr(self, hand) > 0]
            if possible_hands:
                hand = random.choice(possible_hands)
                opp_possible = [opp_hand for opp_hand in ['top', 'bottom'] if getattr(opponent, opp_hand) > 0]
                if opp_possible:
                    opp_hand = random.choice(opp_possible)
                    attack_value = getattr(self, hand)
                    new_value = getattr(opponent, opp_hand) + attack_value
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(opponent, opp_hand, new_value)
                    print(f"{self.name} attacks.")
                    return
        total = self.total_fingers()
        possible_splits = [(a, total - a) for a in range(5) if 
                          0 <= total - a <= 4 and 
                          (a, total - a) != (self.top, self.bottom) and 
                          (a, total - a) != (self.bottom, self.top)]
        if possible_splits:
            top, bottom = random.choice(possible_splits)
            self.set_hands(top, bottom)
            print(f"{self.name} splits.")
        else:
            print(f"{self.name} attacks.")
            self.easy_move(opponent)

    def medium_move(self, opponent):
        for hand in ['top', 'bottom']:
            if getattr(self, hand) > 0:
                for opp_hand in ['top', 'bottom']:
                    if (getattr(opponent, opp_hand) > 0 and 
                        getattr(opponent, opp_hand) + getattr(self, hand) == 5):
                        new_value = 0  # Only knock out if exactly 5
                        setattr(opponent, opp_hand, new_value)
                        print(f"{self.name} attacks.")
                        return
        if self.top == 0 or self.bottom == 0:
            total = self.total_fingers()
            possible_splits = [(a, total - a) for a in range(1, 5) if 
                              0 < total - a < 5 and 
                              (a, total - a) != (self.top, self.bottom) and 
                              (a, total - a) != (self.bottom, self.top)]
            if possible_splits:
                top, bottom = random.choice(possible_splits)
                self.set_hands(top, bottom)
                print(f"{self.name} splits.")
                return
        self.easy_move(opponent)

    def hard_move(self, opponent):
        best_move = None
        best_value = -float('inf')
        for move in self.get_possible_moves(opponent):
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
            elif move['type'] == 'split':
                top, bottom = move['top'], move['bottom']
                original_top, original_bottom = self.top, self.bottom
                self.set_hands(top, bottom)
                value = self.minimax(self, opponent, 3, False)
                self.set_hands(original_top, original_bottom)
            if value > best_value:
                best_value = value
                best_move = move
        if best_move['type'] == 'attack':
            hand, opp_hand = best_move['hand'], best_move['opp_hand']
            attack_value = getattr(self, hand)
            new_value = getattr(opponent, opp_hand) + attack_value
            if new_value == 5:
                new_value = 0
            elif new_value > 5:
                new_value -= 5
            setattr(opponent, opp_hand, new_value)
            print(f"{self.name} attacks.")
        elif best_move['type'] == 'split':
            top, bottom = best_move['top'], best_move['bottom']
            self.set_hands(top, bottom)
            print(f"{self.name} splits.")

    def minimax(self, player, opponent, depth, is_maximizing):
        if depth == 0 or player.is_defeated() or opponent.is_defeated():
            if opponent.is_defeated():
                return 1
            elif player.is_defeated():
                return -1
            return 0
        if is_maximizing:
            best_value = -float('inf')
            for move in self.get_possible_moves(opponent):
                if move['type'] == 'attack':
                    hand, opp_hand = move['hand'], move['opp_hand']
                    original = getattr(opponent, opp_hand)
                    new_value = original + getattr(self, hand)
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(opponent, opp_hand, new_value)
                    value = self.minimax(player, opponent, depth - 1, False)
                    setattr(opponent, opp_hand, original)
                elif move['type'] == 'split':
                    top, bottom = move['top'], move['bottom']
                    original_top, original_bottom = player.top, player.bottom
                    player.set_hands(top, bottom)
                    value = self.minimax(player, opponent, depth - 1, False)
                    player.set_hands(original_top, original_bottom)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in opponent.get_possible_moves(player):
                if move['type'] == 'attack':
                    hand, opp_hand = move['hand'], move['opp_hand']
                    original = getattr(player, opp_hand)
                    new_value = original + getattr(opponent, hand)
                    if new_value == 5:
                        new_value = 0
                    elif new_value > 5:
                        new_value -= 5
                    setattr(player, opp_hand, new_value)
                    value = self.minimax(player, opponent, depth - 1, True)
                    setattr(player, opp_hand, original)
                elif move['type'] == 'split':
                    top, bottom = move['top'], move['bottom']
                    original_top, original_bottom = opponent.top, opponent.bottom
                    opponent.set_hands(top, bottom)
                    value = self.minimax(player, opponent, depth - 1, True)
                    opponent.set_hands(original_top, original_bottom)
                best_value = min(best_value, value)
            return best_value

# Game class to manage turns and display state
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.opponent = player2

    def display_state(self):
        # Assign players
        player1 = self.player1
        player2 = self.player2

        # Assign hands to quadrants
        nw = player1.top    # Player 1's top hand (NW)
        sw = player1.bottom   # Player 1's bottom hand (SW)
        ne = player2.top    # Player 2's top hand (NE)
        se = player2.bottom   # Player 2's bottom hand (SE)

        # Find maximum height across all hands
        max_height = max(nw, sw, ne, se)

        # Build quadrant lines (top-down, so reverse later)
        nw_lines = ['___' if i < nw else '   ' for i in range(max_height)]
        ne_lines = ['___' if i < ne else '   ' for i in range(max_height)]
        sw_lines = ['___' if i < sw else '   ' for i in range(max_height)]
        se_lines = ['___' if i < se else '   ' for i in range(max_height)]

        # Reverse to display from top to bottom
        nw_lines.reverse()
        ne_lines.reverse()
        sw_lines.reverse()
        se_lines.reverse()

        # Width of the display
        boundary_width = 30

        # Display the state
        print(f"\n{player1.name}              {player2.name}")
        print("-" * boundary_width)
        for i in range(max_height):
            print(f"{nw_lines[i]}           ||           {ne_lines[i]}")
        print("-" * boundary_width)
        for i in range(max_height):
            print(f"{sw_lines[i]}           ||           {se_lines[i]}")
        print("-" * boundary_width)

    def play(self):
        while not self.player1.is_defeated() and not self.player2.is_defeated():
            self.display_state()
            print(f"\n{self.current_player.name}'s turn")
            self.current_player.make_move(self.opponent)
            self.current_player, self.opponent = self.opponent, self.current_player
        self.display_state()
        if self.player1.is_defeated():
            print(f"{self.player2.name} wins!")
        else:
            print(f"{self.player1.name} wins!")

# Main function to start the game
def main():
    INIT_MESSAGE = f"""\nWelcome to Chopsticks!\nCommands:
    - attack: 'a'
    - split:  's'
    - top:    't'
    - bottom: 'b'
    """
    MODE_INPUT_MESSAGE = f"""Choose mode:
    - 2-Player: '2'
    - Computer: 'c'
    """
    DIFFICULTY_INPUT_MESSAGE = f"""Choose difficulty:
    - Easy: 'e'
    - Medium: 'm'
    - Hard: 'h'
    """
    print(INIT_MESSAGE)
    mode = input(MODE_INPUT_MESSAGE)
    if mode == '2':

        player1 = HumanPlayer(input("Enter Player 1 name: "))
        player2 = HumanPlayer(input("Enter Player 2 name: "))
    elif mode == 'c':
        difficulty = input(DIFFICULTY_INPUT_MESSAGE)
        if difficulty not in ['e', 'm', 'h']:
            print("Invalid difficulty.")
            return
        player1 = HumanPlayer("Player")
        player2 = ComputerPlayer("Computer", difficulty)
    else:
        print("Invalid mode.")
        return
    game = Game(player1, player2)
    game.play()

if __name__ == "__main__":
    main()