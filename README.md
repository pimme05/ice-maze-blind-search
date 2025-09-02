# Star Wars: Hoth Ice Maze

A Star Wars-themed puzzle game featuring AI pathfinding algorithms and sliding ice mechanics. Navigate through 5 challenging levels as a Rebel pilot trying to reach Echo Base while avoiding Imperial patrols.

## 🎮 Game Overview

Unlike traditional maze games, this ice maze requires you to keep sliding in your chosen direction until you hit an obstacle - just like moving on slippery ice! Set on the ice planet Hoth from the Star Wars universe, you must collect a golden key before reaching Echo Base to complete each level.

### Key Features

- **Unique Ice Physics**: Slide until you hit something - no stopping mid-move
- **Dual Game Modes**: Play as human or watch AI algorithms solve the maze
- **AI Pathfinding**: Implements BFS and DFS with key collection logic
- **Progressive Difficulty**: 5 levels with increasing complexity and enemy patrols
- **Star Wars Theme**: Complete with Hoth atmosphere and Rebel vs Empire elements

## 🎯 Objective

- Control a Rebel walker to reach Echo Base
- Collect the golden key first (door won't open without it)
- Avoid Imperial patrols (game over if caught)
- Complete all 5 levels to win

## 🕹️ Controls

### Human Mode
- **WASD** or **Arrow Keys**: Move pilot (slides until hitting obstacle)
- **R**: Reset current level
- **M**: Toggle between Human/AI mode
- **ESC**: Return to main menu

### AI Mode
- **B**: Run BFS (Breadth-First Search) algorithm
- **D**: Run DFS (Depth-First Search) algorithm
- **A**: Autopilot (execute AI solution after pathfinding)
- **R**: Reset current level
- **M**: Toggle between Human/AI mode
- **ESC**: Return to main menu

## 🧠 AI Algorithms

The game demonstrates two fundamental search algorithms:

### BFS (Breadth-First Search) - "Rebel Scanner"
- Explores all positions at distance N before exploring distance N+1
- **Guarantees** shortest path solution
- Uses queue data structure (FIFO - First In, First Out)
- Colored in **blue** during visualization

### DFS (Depth-First Search) - "Empire Probe"
- Explores as far as possible along each branch before backtracking
- May find longer paths but uses less memory
- Uses stack data structure (LIFO - Last In, First Out)
- Colored in **red** during visualization

### Key Collection Logic
Both algorithms implement sophisticated state tracking:
- **Compound States**: Each position is tracked with key status (has_key: true/false)
- **Goal Dependencies**: Cannot reach Echo Base without collecting the key first
- **Path Reconstruction**: Maintains complete solution path for execution

## 🎮 Game Modes

### 1. Human Mode
- Direct player control with keyboard input
- Real-time collision detection with enemy patrols
- Manual puzzle solving with ice sliding mechanics

### 2. AI Demonstration Mode
- Watch algorithms explore the maze step-by-step
- Visual representation of how BFS and DFS work
- Solution path highlighted in green
- Optional autopilot to execute the AI's solution

## 📊 Level Progression

| Level | Name | Grid Size | Enemies | Complexity |
|-------|------|-----------|---------|------------|
| 1 | Hoth Landing Site | 12×9 | 0 | Tutorial level |
| 2 | Ice Caverns | 12×9 | 2 | Basic patrols |
| 3 | Echo Base Approach | 12×9 | 3 | Complex layout |
| 4 | Frozen Wastes | 16×10 | 3 | Larger maze |
| 5 | Shield Generator Run | 16×10 | 4 | Maximum difficulty |

### Search Performance
- **Early Levels**: 15-25 nodes expanded
- **Later Levels**: 45-120 nodes expanded
- **Algorithm Comparison**: BFS vs DFS exploration patterns clearly visible

## 🤖 Enemy System

**Imperial Patrols** move automatically with simple AI:
- **Predictable Movement**: Each patrol follows a direction vector (dx, dy)
- **Bounce Behavior**: Reverses direction when hitting walls
- **Frame-Rate Independent**: Moves every 0.35 seconds regardless of game speed
- **Mode-Specific Threat**: Only dangerous to human players, not during AI demonstrations

## 🛠️ Technical Implementation

### Core Components

1. **Maze Class**: Handles level data, ice physics, and game rules
2. **SearchAlgorithm Class**: Implements BFS/DFS with key collection logic
3. **StarWarsIceMazeGame Class**: Manages game state, rendering, and user interaction

### Ice Physics Engine
```python
def slide_move(self, start_x, start_y, direction):
    # Slides until hitting a wall or boundary
    # Returns new position or None if no movement possible
```

### Search Algorithm Integration
- **State Representation**: (position, has_key, path_history)
- **Duplicate Detection**: Prevents infinite loops in graph traversal
- **Solution Validation**: Ensures both position and key requirements are met

### Visual Effects
- **Real-time Animation**: Step-by-step algorithm visualization
- **Holographic UI**: Star Wars-inspired interface elements
- **Particle Effects**: Starfield background and scanning effects
- **Color Coding**: Different colors for BFS (blue) vs DFS (red) exploration

## 🚀 Installation & Usage

### Requirements
- Python 3.7+
- Pygame library

### Installation
```bash
pip install pygame
```

### Running the Game
```bash
python main.py
```

### Optional Assets
The game supports custom images but works with built-in graphics:
- `pic1.png` - Player character sprite
- `pic2.png` - Echo Base sprite  
- `key.png` - Key sprite

## 🎓 Educational Value

This project demonstrates several computer science concepts:

### Pathfinding Algorithms
- **Graph Traversal**: BFS vs DFS comparison with visual feedback
- **State Space Search**: Complex state representation with dependencies
- **Optimization**: Shortest path guarantees vs memory efficiency trade-offs

### Game Development
- **Physics Simulation**: Ice sliding mechanics
- **State Management**: Multiple game modes and level progression
- **Animation Systems**: Real-time visualization of algorithm execution

### Software Engineering
- **Design Patterns**: State, Strategy, Observer, and Command patterns
- **Modular Architecture**: Clean separation between game logic and AI systems
- **Error Handling**: Robust collision detection and boundary checking

## 🌟 Unique Features

- **Educational Gaming**: Learn algorithms while having fun
- **Dual Experience**: Human puzzle-solving and AI demonstration in one game
- **Progressive Complexity**: Carefully designed difficulty curve
- **Star Wars Immersion**: Themed graphics, colors, and terminology
- **Real-time Visualization**: See exactly how search algorithms think

## 🎯 Target Audience

- Computer science students learning search algorithms
- Game developers interested in pathfinding implementation
- Star Wars fans who enjoy puzzle games
- Anyone curious about how AI solves problems

## 🔧 Customization

The modular design allows easy customization:
- Add new levels by modifying the `Maze.load_level()` method
- Implement additional search algorithms in the `SearchAlgorithm` class
- Adjust difficulty by changing enemy patrol patterns
- Modify ice physics parameters for different sliding behaviors

---

*May the Force be with you as you navigate the frozen wastes of Hoth!*
