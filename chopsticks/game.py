# game.py
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.opponent = player2

    def display_state(self):
        p1, p2 = self.player1, self.player2
        max_height = max(p1.top, p1.bottom, p2.top, p2.bottom)
        nw_lines = ['___' if i < p1.top else '   ' for i in range(max_height)][::-1]
        ne_lines = ['___' if i < p2.top else '   ' for i in range(max_height)][::-1]
        sw_lines = ['___' if i < p1.bottom else '   ' for i in range(max_height)][::-1]
        se_lines = ['___' if i < p2.bottom else '   ' for i in range(max_height)][::-1]
        boundary_width = 22
        print(f"{p1.name}          {p2.name}")
        print("-" * boundary_width)
        for i in range(max_height):
            print(f"{nw_lines[i]}          {ne_lines[i]}")
        print('')
        print("-" * boundary_width)
        for i in range(max_height):
            print(f"{sw_lines[i]}          {se_lines[i]}")
        print("-" * boundary_width)

    def play(self):
        while not self.player1.is_defeated() and not self.player2.is_defeated():
            self.display_state()
            print(f"\n{self.current_player.name}'s turn")
            self.current_player.make_move(self.opponent)
            self.current_player, self.opponent = self.opponent, self.current_player
        self.display_state()
        print(f"{self.player2.name if self.player1.is_defeated() else self.player1.name} wins!")
