import random
import chess
from utils.helpers import load_puzzles

# load all puzzles written in SAN format
puzzles = load_puzzles()

print("\n🎯 Welcome to the Mate-in-One Trainer")

while True:
    # pick a new random puzzle every round
    puzzle = random.choice(puzzles)
    board = chess.Board(puzzle["fen"])
    correct_move_san = puzzle["move"]

    # Show the puzzle
    print("\nHere's your puzzle:\n")
    print(board.unicode(borders=True))

    # Ask for user's move in SAN (algebraic) format
    user_input = input("\nEnter your move (e.g., Qf6, g3, Re8): ").strip()

    try:
        # Convert SAN input to a move object
        move = board.parse_san(user_input)
        board.push(move)

        # Show updated board after move
        print("\n📥 You played:\n")
        print(board.unicode(borders=True))

        # Compare move to correct solution
        if user_input == correct_move_san:
            print("\n✅ Correct move!")
        else:
            print(f"\n❌ Incorrect. The correct move was: {correct_move_san}")
    except:
        print("\n⚠️ Invalid move. Please try a format like 'Qf6', 'g3', or 'O-O'.")

    # Ask if user wants to continue
    again = input("\nTry another puzzle? (y/n): ").strip().lower()
    if again != "y":
        print("\n👋 Thanks for training. Goodbye!")
        break