import random
import chess
from utils.helpers import load_puzzles

# Load all puzzles once at the start
puzzles = load_puzzles()

print("\n🎯 Welcome to the Mate-in-One Trainer!")

while True:
    # ✅ Randomly select a new puzzle every time through the loop
    puzzle = random.choice(puzzles)
    board = chess.Board(puzzle["fen"])
    correct_move = puzzle["move"]

    # Display the puzzle board
    print("\nHere's your puzzle:\n")
    print(board.unicode(borders=True))

    # Get the user's move
    user_input = input("\nEnter your move (e.g., f1c4): ").strip().lower()

    try:
        # Convert input to a move object
        move = chess.Move.from_uci(user_input)

        if move in board.legal_moves:
            # Apply the move
            board.push(move)

            # Show the updated board
            print("\n📥 You played:\n")
            print(board.unicode(borders=True))

            # Check if it's correct
            if user_input == correct_move:
                print("\n✅ Correct move!")
            else:
                print(f"\n❌ Incorrect. The correct move was: {correct_move}")
        else:
            print("\n⚠️ That move is not legal in this position.")
    except:
        print("\n⚠️ Invalid move format. Please enter something like 'f1c4'")

    # Ask if the user wants another puzzle
    again = input("\nWant to try another? (y/n): ").strip().lower()
    if again != "y":
        print("\n👋 Thanks for training. Goodbye!")
        break
