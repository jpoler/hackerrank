import sys
from heapq import heappush, heappop

class Path:
    def __init__(self, v, dist, dest, route):
        self.node = v
        self.dist = dist
        self.route = route[:] + [v]
        self.dest = dest

    def __lt__(self, other):
        if self.dist == other.dist:
            return abs(self.node - self.dest) < abs(other.node - other.dest)
        return self.dist < other.dist
    
    def __le__(self, other):
        if self.dist == other.dist:
            return abs(self.node - self.dest) < abs(other.node - other.dest)
        return self.dist <= other.dist

    def __repr__(self):
        return "<Path (node: {}, dist: {}, route: {}".format(
            self.node,
            self.dist,
            self.route
        )

class Node:
    def __init__(self, key, dest, *edges):
        self.key = key
        self.discovered = False
        self.processed = False
        self.parent = None
        self.edges = set(edges)
        self.min_path = Path(key, float("inf"), dest, [])
        
    def __repr__(self):
        return "<Node (Parent: {}, Edges: {}, Discovered: {}, Processed: {})>".format(
            self.parent,
            self.edges,
            self.discovered,
            self.processed,
        )

    def is_ladder(self):
        for i in self.edges:
            if self.key <= i:
                return True
        return False

    def is_snake(self):
        for i in self.edges:
            if self.key >= i:
                return True
        return False

class Graph:
    def __init__(self, n):
        self.G = {i: Node(i, n, *[j for j in range(i+1, i+7 if i+7 <= n+1 else n+1)]) for i in range(n)}
        self.G[n] = Node(n, n)
        self.h = []
        
    def add_edges(self, edges):
        for source, dest in edges:
            self.G[source].edges.add(dest)

    def djikstra(self, source, dest):
        self.h.append(Path(source, 0, dest, []))
        start_node = self.G[source]
        last = source
        while last != dest:
            min_path = heappop(self.h)
            u_node = self.G[min_path.node]
            for v in u_node.edges:
                v_node = self.G[v]
                new_path = Path(v, min_path.dist + 1, dest, min_path.route)
                if new_path < v_node.min_path:
                    v_node.min_path = new_path
                    heappush(self.h, new_path)
            last = u_node.key
        return self.G[dest].min_path


        
def parse_line(line):
    clean = line.strip().split(' ')
    return [list(map(int, elem.split(','))) for elem in clean]
            
def parse_test_case():
    board = Graph(100)
    ladders, snakes = parse_line(sys.stdin.readline())[0]
    ladder_edges = parse_line(sys.stdin.readline())
    snake_edges = parse_line(sys.stdin.readline())
    assert len(ladder_edges) == ladders
    assert len(snake_edges) == snakes
    
    board.add_edges(ladder_edges)
    board.add_edges(snake_edges)
    
    return board

def emit_answer(answer):
    print(answer)

def count_rolls(route):
    rolls = 0
    valid_rolls = range(1, 7)
    for i in range(1, len(route)):
        if (route[i] - route[i-1]) in valid_rolls:
            rolls += 1
    return rolls
    
def solve_test_case():
    board = parse_test_case()
    result = board.djikstra(1, 100)
    answer = count_rolls(result.route)
    emit_answer(answer)
    
testcases = int(sys.stdin.readline().strip())

for _ in range(testcases):
    solve_test_case()


