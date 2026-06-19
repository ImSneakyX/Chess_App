# Chess Project

This is my second attempt at building a chess application.

The long-term goal is to create both an opening database and my own chess engine. The project is also intended as a learning journey: I want to understand and implement the underlying concepts myself rather than simply assembling existing solutions.

The first version uses an object-oriented representation of the board and pieces. I am currently exploring how to transition this design towards a more data-oriented representation in order to improve performance and scalability.

The repository documents this process, including experiments, refactorings, and performance optimizations.

## Current Status

* Object-oriented board representation implemented
* Legal move generation
* Minimax search with alpha-beta pruning
* GUI implementation

## Notes

At the moment, the application starts through `ui/main_window.py`. A dedicated entry point (`main.py`) will be added later as the project structure evolves.
