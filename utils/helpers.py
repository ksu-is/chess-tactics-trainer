# This line imports the built-in json module, which will let us read JSON files.
import json

# We define a function called load_puzzles.
# A function is like a mini-program inside your code that does one specific task.
def load_puzzles(path="puzzles/puzzles.json"):
    """
    Loads puzzles from the JSON file and returns them as a list.
    
    Parameters:
      path (str): The relative path to the puzzles JSON file.
                   By default, it is "puzzles/puzzles.json".
      
    Returns:
      list: A list of puzzles loaded from the JSON file.
    """
    # Open the file located at the given 'path' in read mode ("r").
    # The 'with' statement is used to open the file and automatically close it afterward.
    with open(path, "r") as file:
        # json.load(file) reads the file and converts JSON data into a Python list or dictionary.
        puzzles = json.load(file)
    # The function returns the puzzles that were loaded.
    return puzzles

