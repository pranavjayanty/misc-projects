from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.top = 1
        self.bottom = 1

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
        for hand in ['top', 'bottom']:
            if getattr(self, hand) > 0:
                for opp_hand in ['top', 'bottom']:
                    if getattr(opponent, opp_hand) > 0:
                        moves.append({'type': 'attack', 'hand': hand, 'opp_hand': opp_hand})
        total = self.total_fingers()
        for a in range(5):
            b = total - a
            if (0 <= b <= 4 and (a, b) != (self.top, self.bottom) and (a, b) != (self.bottom, self.top)):
                moves.append({'type': 'split', 'top': a, 'bottom': b})
        return moves

    @abstractmethod
    def make_move(self, opponent):
        pass
