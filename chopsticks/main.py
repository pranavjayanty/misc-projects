from human import HumanPlayer
from computer import ComputerPlayer
from game import Game

def main():
    print("\nWelcome to Chopsticks!\nCommands:\n  a then tt/tb/bt/bb: attack\n  s then 0-4 or q: split")
    mode = input("Mode (2 for 2-Player, c for Computer): ").lower()
    if mode == '2':
        player1 = HumanPlayer(input("Player 1 name: "))
        player2 = HumanPlayer(input("Player 2 name: "))
    elif mode == 'c':
        difficulty = input("Difficulty (e: Easy, m: Medium, h: Hard): ").lower()
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
