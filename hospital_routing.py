import tkinter as tk
from collections import deque
import heapq
import random

GRID = [
    ["S", ".", ".", "C", "C", ".", "G"],
    [".", "#", ".", "C", "#", ".", "."],
    [".", "#", ".", ".", ".", "#", "."],
    [".", ".", "C", "C", ".", ".", "."],
    [".", "#", "#", ".", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", "."],
]

COST = {"S": 1, "G": 1, ".": 1, "C": 5}
COLORS = {
    "S": "#2E7D32",
    "G": "#C62828",
    "#": "#263238",
    ".": "#ECEFF1",
    "C": "#FFB300",
    "visited": "#BBDEFB",
    "path": "#00BFA5",
}
SIZE = 70


def find_cell(grid, target):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == target:
                return (r, c)


def neighbors(grid, pos):
    r, c = pos
    res = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            res.append((nr, nc))
    return res


def calc_cost(grid, path):
    return sum(COST.get(grid[r][c], 1) for r, c in path) if path else None


def bfs(grid, start, goal):
    q = deque([[start]])
    seen = {start}
    visited = []
    while q:
        path = q.popleft()
        curr = path[-1]
        visited.append(curr)
        if curr == goal:
            return path, visited
        for nxt in neighbors(grid, curr):
            if nxt not in seen:
                seen.add(nxt)
                q.append(path + [nxt])
    return None, visited


def dfs(grid, start, goal):
    stack = [[start]]
    seen = {start}
    visited = []
    while stack:
        path = stack.pop()
        curr = path[-1]
        visited.append(curr)
        if curr == goal:
            return path, visited
        for nxt in reversed(neighbors(grid, curr)):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(path + [nxt])
    return None, visited


def ids(grid, start, goal):
    total_visited = []
    max_depth = len(grid) * len(grid[0])

    def dls(curr, path, depth, limit, path_set):
        total_visited.append(curr)
        if curr == goal:
            return path
        if depth >= limit:
            return None
        for nxt in neighbors(grid, curr):
            if nxt not in path_set:
                path_set.add(nxt)
                res = dls(nxt, path + [nxt], depth + 1, limit, path_set)
                path_set.remove(nxt)
                if res:
                    return res
        return None

    for limit in range(max_depth + 1):
        res = dls(start, [start], 0, limit, {start})
        if res:
            return res, total_visited
    return None, total_visited


def greedy(grid, start, goal):
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    pq = [(h(start), start, [start])]
    seen = {start}
    visited = []
    while pq:
        _, curr, path = heapq.heappop(pq)
        visited.append(curr)
        if curr == goal:
            return path, visited
        for nxt in neighbors(grid, curr):
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(pq, (h(nxt), nxt, path + [nxt]))
    return None, visited


def astar(grid, start, goal):
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    pq = [(h(start), 0, start, [start])]
    best = {start: 0}
    visited = []
    while pq:
        _, g, curr, path = heapq.heappop(pq)
        visited.append(curr)
        if curr == goal:
            return path, visited
        for nxt in neighbors(grid, curr):
            ng = g + COST.get(grid[nxt[0]][nxt[1]], 1)
            if nxt not in best or ng < best[nxt]:
                best[nxt] = ng
                heapq.heappush(pq, (ng + h(nxt), ng, nxt, path + [nxt]))
    return None, visited


ALGOS = [("BFS", bfs), ("DFS", dfs), ("IDS", ids), ("Greedy", greedy), ("A*", astar)]


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Hospital Routing")
        self.grid = [row[:] for row in GRID]
        self.path = []
        self.visited = []
        self.mode = "G"

        self.canvas = tk.Canvas(root, width=len(GRID[0]) * SIZE, height=len(GRID) * SIZE)
        self.canvas.pack(side="left", padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        panel = tk.Frame(root)
        panel.pack(side="right", fill="y", padx=8, pady=8)

        for name, fn in ALGOS:
            tk.Button(panel, text=name, width=14, command=lambda n=name, f=fn: self.run_one(n, f)).pack(pady=2)

        tk.Button(panel, text="Compare All", width=14, command=self.compare).pack(pady=2)
        tk.Button(panel, text="Random Crowding", width=14, command=self.random_crowd).pack(pady=2)
        tk.Button(panel, text="Reset", width=14, command=self.reset).pack(pady=2)

        self.box = tk.Text(panel, width=32, height=14)
        self.box.pack(pady=8)
        self.compare()

    def draw(self):
        self.canvas.delete("all")
        p_set = set(self.path)
        v_set = set(self.visited)
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                x1, y1 = c * SIZE, r * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                pos = (r, c)
                fill = COLORS[val] if val in ("S", "G") else COLORS["path"] if pos in p_set else COLORS["visited"] if pos in v_set else COLORS[val]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#78909C")
                text = "*" if pos in p_set and val not in ("S", "G") else val
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=("Arial", 11, "bold"))

    def left_click(self, e):
        r, c = e.y // SIZE, e.x // SIZE
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and self.grid[r][c] not in ("S", "G"):
            self.grid[r][c] = {".": "C", "C": "#", "#": "."}[self.grid[r][c]]
            self.path, self.visited = [], []
            self.draw()

    def right_click(self, e):
        r, c = e.y // SIZE, e.x // SIZE
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and self.grid[r][c] not in ("S", "G"):
            old = find_cell(self.grid, self.mode)
            if old:
                self.grid[old[0]][old[1]] = "."
            self.grid[r][c] = self.mode
            self.mode = "S" if self.mode == "G" else "G"
            self.path, self.visited = [], []
            self.draw()

    def run_one(self, name, fn):
        s, g = find_cell(self.grid, "S"), find_cell(self.grid, "G")
        self.path, self.visited = fn(self.grid, s, g)
        self.path = self.path or []
        self.draw()
        steps = len(self.path) - 1 if self.path else "No Path"
        cost = calc_cost(self.grid, self.path)
        self.box.delete("1.0", tk.END)
        self.box.insert(tk.END, f"{name}\nSteps: {steps}\nCost: {cost}\nVisited: {len(self.visited)}")

    def compare(self):
        s, g = find_cell(self.grid, "S"), find_cell(self.grid, "G")
        lines = ["Algo   | Steps | Cost | Visited"]
        for name, fn in ALGOS:
            p, v = fn(self.grid, s, g)
            st = len(p) - 1 if p else "None"
            lines.append(f"{name:6s} | {str(st):5s} | {str(calc_cost(self.grid, p)):4s} | {len(v)}")
            if name == "A*":
                self.path, self.visited = p or [], v
        self.draw()
        self.box.delete("1.0", tk.END)
        self.box.insert(tk.END, "\n".join(lines))

    def random_crowd(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] in (".", "C"):
                    self.grid[r][c] = random.choices([".", "C"], [0.65, 0.35])[0]
        self.compare()

    def reset(self):
        self.grid = [row[:] for row in GRID]
        self.mode = "G"
        self.compare()


root = tk.Tk()
App(root)
root.mainloop()