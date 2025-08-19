# ❄️ Ice Maze AI Game – Blind Search

## 📌 Project Overview
This project is developed as part of an **Artificial Intelligence course** to demonstrate **Blind Search algorithms** (BFS & DFS) in a game environment.

The game uses an ice-maze mechanic: the agent slides in a chosen direction until hitting a wall, which creates interesting state transitions for search.

---

## 🧠 AI Concepts
The project focuses on **uninformed (blind) search**:
- **Breadth-First Search (BFS)** — explores level by level; finds the shortest path in number of moves.
- **Depth-First Search (DFS)** — explores deep paths first; not guaranteed to find the shortest path.
- Visualizes **explored nodes** and the **final solution path**, enabling algorithm comparison.

---

## 🎮 Gameplay
- Start at a fixed position and reach the **goal**.
- Sliding movement (ice): you keep moving until blocked.
- Two modes: **Manual** and **AI**.

### Controls
**Manual Mode**
- `Arrow Keys` / `WASD` — move (slide) the player

**AI Mode**
- `B` — Run BFS
- `D` — Run DFS
- `M` — Toggle Manual/AI
- `R` — Reset maze

---

## ✨ Features
- Grid-based sliding puzzle
- Manual + AI demo modes
- BFS/DFS visualization (explored/solution path)
- Simple sci-fi UI theme
- Supports custom assets (player, goal, etc.)

---

## 📂 File Structure
├── main.py # Game loop & rendering
├── maze.py # Maze generation & sliding movement
├── search.py # BFS & DFS implementations
├── assets/ # Images (player, portal, etc.)
├── pic1.png # (Optional) screenshot for README
├── pic2.png # (Optional) screenshot for README
