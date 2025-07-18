# AI_CAR

AI_CAR is a self-driving car simulation using a neural network and genetic algorithm, built with Python and Pygame. Cars learn to navigate a track by evolving their neural networks over generations.

## Features
- Neural network-based car control (see `brain.py`)
- Genetic algorithm for evolving car behavior
- Visual simulation with Pygame
- Fitness-based evolution and lap tracking
- Customizable car and track images

## Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have `car.png` and `map.png` in the project directory.

## Usage
Run the simulation with:
```bash
python main.py
```

- The simulation window will open, showing cars learning to drive around the track.
- Each car is controlled by a neural network whose weights evolve over generations.
- Specs for each car (speed, distance, fitness) are displayed above the car in red.

## Files
- `main.py`: Main simulation and genetic algorithm logic
- `brain.py`: Neural network implementation
- `car.png`: Car image
- `map.png`: Track image
- `requirements.txt`: Python dependencies
- `todo.txt`: Planned features and improvements

## Planned Features (see `todo.txt`)
```
1. Add multiple levels/tracks with increasing difficulty
2. Add background music and sound effects
3. Add control panels (UI) to adjust car specs (speed, acceleration, etc.)
4. Implement car customization (color, model, upgrades)
5. Add obstacles or moving hazards on the track
6. Add a leaderboard/high score system
7. Implement power-ups (speed boost, shield, etc.)
8. Add a replay or ghost car feature
9. Add weather effects (rain, fog, etc.)
10. Add multiplayer or AI vs AI race mode
11. Add achievements and unlockables
12. Add a tutorial or help screen
13. Add camera options (zoom, follow, overview)
14. Add lap time tracking and best lap display
```

---

Feel free to contribute or suggest more features to make the simulation even more fun!
