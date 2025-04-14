import random
import chess
from utils.helpers import load_puzzles

# Load puzzles from file
puzzles = load_puzzles()

print("\n🎯 Welcome to the Mate-in-One Trainer!")

while True:
    # Pick a random puzzle
    puzzle = random.choice(puzzles)
    board = chess.Board(puzzle["fen"])
    correct_move = puzzle["move"]

    # Show the board
    print("\nHere's your puzzle:\n")
    print(board)

    # Ask for move
    user_input = input("\nEnter your move (e.g., f1c4): ").strip().lower()

    # Check answer
    if user_input == correct_move:
        print("\n✅ Correct!")
    else:
        print(f"\n❌ Incorrect. The correct move was: {correct_move}")

    # Ask if they want another puzzle
    again = input("\nWant to try another? (y/n): ").strip().lower()
    if again != "y":
        print("\n👋 Thanks for training. Goodbye!")
        break

