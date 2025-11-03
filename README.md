# Hangman in Python

A little project combining a Hangman-style game built with pygame and a Hangman solver implemented in Python.  
Originally, I just wanted to write the solver but then I thought, “Why not make a full game too?”.

## Hangman Game (`main.py`)

This is a lighthearted version of the classic Hangman game, except no one gets hanged here.
Instead, a sakura flower loses its petals one by one as you make incorrect guesses.

### Features:
- Choose between 6 different categories of words.  
- You get 6 attempts before the sakura flower is completely bare.  

### Demo
[![Video Title](demo/thumbnail.jpg)](https://youtu.be/KHl7L5Ul6uo)

## Hangman Solver (`hangman_solver.ipynb`)

A fully automated word-guessing algorithm that can:
- Run a single simulation and show you each guess step-by-step, or  
- Run hundreds of simulations to measure the algorithm’s success rate

The solver uses:
- Positional letter frequency - guessing letters based on where they most often appear in similar words.  
- Smart candidate filtering - narrowing down possible words as it learns more.  

You can run it directly inside the Jupyter Notebook, visualize its accuracy with a graph, and change parameters like number of trials or allowed mistakes.

## Credits

* **Background:** https://free-game-assets.itch.io/free-sky-with-clouds-background-pixel-art-set
* **Buttons:** https://mandinhart.itch.io/garden-cozy-kit-uigui-buttons-and-icons
* **Flower:** drawn by me!