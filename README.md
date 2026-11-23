[README-aa0b576c.md](https://github.com/user-attachments/files/35299695/README-aa0b576c.md)
# Smart Hospital Routing

An AI search-based pathfinding application that finds the best route from an emergency entrance to a destination inside a hospital, while avoiding crowded corridors.

Built with Python and Tkinter. Implements and compares five classic search algorithms: **BFS, DFS, IDS, Greedy, and A\***.

## The Problem

When someone arrives at a hospital emergency entrance, they need to reach their destination (a ward, a lab, a reception desk) as fast as possible. The shortest path in terms of distance is not always the best path: some corridors are crowded, and walking through them costs extra time and effort. A visitor or patient needs a route that balances distance against crowding.

## The Solution

The hospital floor is modeled as a 2D grid:

| Cell | Meaning | Movement cost |
|------|---------|---------------|
| `S`  | Start (entrance) | 1 |
| `G`  | Goal (destination) | 1 |
| `.`  | Free corridor | 1 |
| `C`  | Crowded corridor | 5 |
| `#`  | Wall (blocked) | cannot pass |

Search algorithms explore this grid and return a path from `S` to `G`. The application visualizes the explored cells and the final path, and compares all algorithms side by side.

## Where is the AI?

This project is **Search-Based AI** (classical AI), not a trained Machine Learning model.

- **Uninformed (blind) search**: BFS, DFS, and Iterative Deepening Search (IDS) explore the map with no knowledge of where the goal is.
- **Informed (heuristic) search**: Greedy and A* use the **Manhattan distance** to the goal as a heuristic `h(n)` to guide the search.
- **A\*** combines the actual cost so far `g(n)` with the heuristic `h(n)` (`f(n) = g(n) + h(n)`), so it finds the **minimum-cost** route, where the cost of a cell reflects crowding. That means A* may choose a slightly longer path in steps if it avoids crowded corridors and costs less overall.

## Results on the Default Map

Computed directly from the source code (6x7 default grid):

| Algorithm | Steps | Cost | Visited cells |
|-----------|-------|------|---------------|
| BFS       | 6     | 15   | 22            |
| DFS       | 16    | 33   | 26            |
| IDS       | 6     | 15   | 95            |
| Greedy    | 6     | 15   | 7             |
| A*        | **12** | **13** | 19         |

- BFS, IDS, and Greedy find the fewest **steps** (6), but their cost is higher because they pass through crowded cells.
- A* takes more steps (12) but achieves the lowest **cost** (13) by avoiding crowded corridors.
- Greedy visits the fewest cells (7), but it is not guaranteed to be optimal.
- IDS re-explores cells at every depth limit, so its visited count (95) is the highest.

> Note: `Cost` includes the starting cell. `Visited` counts every cell the algorithm logs during the search (IDS counts repeated visits across iterations).

## Screenshot

![Smart Hospital Routing app](screenshot.png)

The comparison table on the right shows Steps, Cost, and Visited for each algorithm. The teal cells (`*`) are the chosen path, blue cells were explored during the search, and amber cells (`C`) are crowded corridors.

## Features

- Interactive grid visualization with Tkinter
- Run any single algorithm or compare all five at once
- **Random Crowding** button generates a new crowding layout (65% free / 35% crowded)
- **Reset** restores the default map
- Click to edit the map yourself:
  - **Left click** a cell to cycle it: free -> crowded -> wall -> free
  - **Right click** to move the Start or Goal point

## Requirements

- Python 3.x
- `tkinter` (included with standard Python on Windows; on Linux install it with `sudo apt install python3-tk`)

No external libraries are needed. Only the Python standard library is used (`tkinter`, `collections`, `heapq`, `random`).

## How to Run

```bash
python hospital_routing.py
```

The app window opens and immediately shows the full algorithm comparison on the default map.

## Project Structure

```
hospital_routing.py   # the whole application: grid, algorithms, and GUI
```

Inside the file:

- `GRID`, `COST`, `COLORS` - the map, movement costs, and cell colors
- `bfs`, `dfs`, `ids`, `greedy`, `astar` - the five search algorithms
- `neighbors`, `calc_cost`, `find_cell` - helper functions
- `App` - the Tkinter GUI (canvas, buttons, and results panel)

## Customization

- Edit `GRID` to change the map layout or size.
- Edit `COST` to change how expensive crowded cells are.
- The heuristic in `greedy` and `astar` is Manhattan distance; it can be swapped for another heuristic.

## Limitations

- Costs are abstract weights, not measured walking times.
- The grid is a simplified hospital map, not a real floor plan.
- This is classical search-based AI; no machine learning model is trained.

## Future Work

- Load real hospital floor plans as the grid
- Dynamic crowding that changes over time and re-routes the path
- More informed heuristics and weighted A*
- Pathfinding for multiple destinations or multiple people at once

## Team

- Mohamed Gamal
- Nadia fathi
- Sandy Draz
- Moaaz Elsaka
- Yossif radwan
- Abdullah Ashraf
- Rewan Mohamed

## References

- [UC Berkeley CS188 - Informed Search](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html)
- [UC Berkeley CS188 - Uninformed Search](https://inst.eecs.berkeley.edu/~cs188/textbook/search/uninformed.html)
- [Python tkinter documentation](https://docs.python.org/3/library/tkinter.html)
