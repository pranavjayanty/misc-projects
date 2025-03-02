# main.py
from human import HumanPlayer
from computer import ComputerPlayer
from game import Game

def main():
    print("\nWelcome to Chopsticks!\nCommands:\n  a then tt/tb/bt/bb: attack\n  s then 0-4 or q: split")
    print("Modes:\n  cc: Computer vs. Computer\n  pp: Player vs. Player\n  cp: Computer vs. Player (Computer first)\n  pc: Player vs. Computer (Player first)")
    mode = input("Choose mode: ").lower().strip()
    
    if mode == 'cc':  # Computer vs. Computer
        difficulty1 = input("Difficulty for Computer 1 (e: Easy, m: Medium, h: Hard): ").lower().strip()
        if difficulty1 not in ['e', 'm', 'h']:
            print("Invalid difficulty for Computer 1.")
            return
        difficulty2 = input("Difficulty for Computer 2 (e: Easy, m: Medium, h: Hard): ").lower().strip()
        if difficulty2 not in ['e', 'm', 'h']:
            print("Invalid difficulty for Computer 2.")
            return
        player1 = ComputerPlayer("Computer 1", difficulty1)
        player2 = ComputerPlayer("Computer 2", difficulty2)
    
    elif mode == 'pp':  # Player vs. Player
        player1 = HumanPlayer(input("Player 1 name: "))
        player2 = HumanPlayer(input("Player 2 name: "))
    
    elif mode == 'cp':  # Computer vs. Player (Computer first)
        difficulty = input("Difficulty for Computer (e: Easy, m: Medium, h: Hard): ").lower().strip()
        if difficulty not in ['e', 'm', 'h']:
            print("Invalid difficulty.")
            return
        player1 = ComputerPlayer("Computer", difficulty)
        player2 = HumanPlayer("Player")
    
    elif mode == 'pc':  # Player vs. Computer (Player first)
        difficulty = input("Difficulty for Computer (e: Easy, m: Medium, h: Hard): ").lower().strip()
        if difficulty not in ['e', 'm', 'h']:
            print("Invalid difficulty.")
            return
        player1 = HumanPlayer("Player")
        player2 = ComputerPlayer("Computer", difficulty)
    
    else:
        print("Invalid mode. Use 'cc', 'pp', 'cp', or 'pc'.")
        return
    
    game = Game(player1, player2)
    game.play()

if __name__ == "__main__":
    main()
