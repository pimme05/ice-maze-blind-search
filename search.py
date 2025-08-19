from collections import deque

class SearchAlgorithm:
    """
    Rebel Navigation AI - Implements blind search algorithms to find paths
    through the Hoth ice maze. No heuristics used - pure exploration!
    
    This class demonstrates how AI agents can navigate unknown terrain
    using systematic search strategies.
    """
    
    def __init__(self, maze):
        """
        Initialize the search system
        
        Args:
            maze: Maze object containing the terrain layout
        """
        self.maze = maze
        self.explored = set()          # Positions we've already scanned
        self.path = []                 # Final solution path
        self.search_order = []         # Order in which positions were explored
        self.algorithm_used = None     # Track which algorithm was used
        self.nodes_expanded = 0        # Performance metric
    
    def reset(self):
        """Reset all search data for a new search operation"""
        self.explored.clear()
        self.path.clear()
        self.search_order.clear()
        self.algorithm_used = None
        self.nodes_expanded = 0
    
    def get_neighbors(self, pos):
        """
        Get all reachable positions from current position using ice sliding
        
        Args:
            pos: Current position tuple (x, y)
            
        Returns:
            list: All positions reachable in one slide move
        """
        x, y = pos
        neighbors = []
        directions = ['up', 'down', 'left', 'right']
        
        for direction in directions:
            new_pos = self.maze.slide_move(x, y, direction)
            if new_pos and new_pos not in self.explored:
                neighbors.append(new_pos)
        
        return neighbors
    
    def bfs(self, start, goal):
        """
        Breadth-First Search - Rebel Scanner Algorithm
        
        Explores the maze level by level, guaranteeing the shortest path.
        Like how Rebel scouts would systematically map territory.
        
        Args:
            start: Starting position tuple
            goal: Target position tuple
            
        Returns:
            bool: True if path found, False if no solution exists
        """
        self.reset()
        self.algorithm_used = "BFS (Breadth-First Search)"
        
        # Initialize the frontier with starting position
        queue = deque([(start, [start])])
        self.explored.add(start)
        
        while queue:
            current_pos, path = queue.popleft()
            self.search_order.append(current_pos)
            self.nodes_expanded += 1
            
            # Check if we've reached Echo Base
            if current_pos == goal:
                self.path = path
                return True
            
            # Explore all neighboring positions
            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in self.explored:
                    self.explored.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        # No path found to Echo Base
        return False
    
    def dfs(self, start, goal):
        """
        Depth-First Search - Empire Probe Algorithm
        
        Explores deeply into the maze before backtracking.
        Like how Imperial probe droids would aggressively pursue leads.
        May not find the optimal path, but can be faster in some cases.
        
        Args:
            start: Starting position tuple
            goal: Target position tuple
            
        Returns:
            bool: True if path found, False if no solution exists
        """
        self.reset()
        self.algorithm_used = "DFS (Depth-First Search)"
        
        # Use a stack for DFS (LIFO - Last In, First Out)
        stack = [(start, [start])]
        
        while stack:
            current_pos, path = stack.pop()
            
            # Skip if already explored (avoid cycles)
            if current_pos in self.explored:
                continue
            
            # Mark as explored and add to search order
            self.explored.add(current_pos)
            self.search_order.append(current_pos)
            self.nodes_expanded += 1
            
            # Check if we've found the target
            if current_pos == goal:
                self.path = path
                return True
            
            # Add neighbors to the stack (they'll be explored next)
            neighbors = self.get_neighbors(current_pos)
            for neighbor in reversed(neighbors):  # Reverse for consistent ordering
                if neighbor not in self.explored:
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
        
        # No path found
        return False
    
    def dfs_recursive(self, start, goal, max_depth=50):
        """
        Recursive Depth-First Search - Alternative implementation
        
        Args:
            start: Starting position
            goal: Target position  
            max_depth: Maximum search depth to prevent infinite recursion
            
        Returns:
            bool: True if path found
        """
        self.reset()
        self.algorithm_used = "DFS-Recursive"
        
        def dfs_helper(current, path, depth):
            if depth > max_depth:
                return False
            
            if current in self.explored:
                return False
            
            self.explored.add(current)
            self.search_order.append(current)
            self.nodes_expanded += 1
            
            if current == goal:
                self.path = path
                return True
            
            for neighbor in self.get_neighbors(current):
                if dfs_helper(neighbor, path + [neighbor], depth + 1):
                    return True
            
            return False
        
        return dfs_helper(start, [start], 0)
    
    def get_search_stats(self):
        """
        Get statistics about the last search operation
        
        Returns:
            dict: Search performance metrics
        """
        return {
            'algorithm': self.algorithm_used,
            'nodes_expanded': self.nodes_expanded,
            'path_length': len(self.path) if self.path else 0,
            'total_explored': len(self.explored),
            'solution_found': bool(self.path),
            'optimal_guaranteed': 'BFS' in str(self.algorithm_used)
        }
    
    def print_search_results(self):
        """Debug function to print search results"""
        stats = self.get_search_stats()
        
        print(f"\n=== REBEL NAVIGATION REPORT ===")
        print(f"Algorithm Used: {stats['algorithm']}")
        print(f"Mission Status: {'SUCCESS' if stats['solution_found'] else 'FAILED'}")
        print(f"Sectors Scanned: {stats['nodes_expanded']}")
        print(f"Total Area Explored: {stats['total_explored']}")
        
        if stats['solution_found']:
            print(f"Route Length: {stats['path_length']} jumps")
            print(f"Optimal Path: {'GUARANTEED' if stats['optimal_guaranteed'] else 'NOT GUARANTEED'}")
            print(f"Navigation Route: {' -> '.join([f'({x},{y})' for x, y in self.path])}")
        else:
            print("ALERT: No viable route to Echo Base found!")
        
        print("=" * 35)
    
    def compare_algorithms(self, start, goal):
        """
        Run both BFS and DFS to compare their performance
        
        Args:
            start: Starting position
            goal: Target position
            
        Returns:
            dict: Comparison results
        """
        # Test BFS
        bfs_found = self.bfs(start, goal)
        bfs_stats = self.get_search_stats()
        
        # Test DFS  
        dfs_found = self.dfs(start, goal)
        dfs_stats = self.get_search_stats()
        
        comparison = {
            'bfs': {
                'found_solution': bfs_found,
                'nodes_expanded': bfs_stats['nodes_expanded'],
                'path_length': bfs_stats['path_length'],
                'total_explored': bfs_stats['total_explored']
            },
            'dfs': {
                'found_solution': dfs_found,
                'nodes_expanded': dfs_stats['nodes_expanded'], 
                'path_length': dfs_stats['path_length'],
                'total_explored': dfs_stats['total_explored']
            }
        }
        
        return comparison
    
    def visualize_search_space(self):
        """
        Create a visual representation of the search process
        For debugging and educational purposes
        """
        if not self.search_order:
            print("No search data available. Run a search first.")
            return
        
        print(f"\n=== SEARCH VISUALIZATION ({self.algorithm_used}) ===")
        print("Legend: S=Start, G=Goal, â–ˆ=Wall, Â·=Free, #=Explored, *=Path")
        
        # Create a copy of the maze for visualization
        viz_grid = []
        for row in self.maze.grid:
            viz_grid.append(row.copy())
        
        # Mark explored positions
        for pos in self.explored:
            x, y = pos
            if viz_grid[y][x] == 0:  # Only mark free spaces
                viz_grid[y][x] = 'E'  # Explored
        
        # Mark the solution path
        for pos in self.path:
            x, y = pos
            if pos != self.maze.start_pos and pos != self.maze.goal_pos:
                viz_grid[y][x] = 'P'  # Path
        
        # Print the visualization
        for y, row in enumerate(viz_grid):
            line = ""
            for x, cell in enumerate(row):
                if (x, y) == self.maze.start_pos:
                    line += "S "
                elif (x, y) == self.maze.goal_pos:
                    line += "G "
                elif cell == 1:
                    line += "â–ˆ "  # Wall
                elif cell == 'E':
                    line += "# "  # Explored
                elif cell == 'P':
                    line += "* "  # Solution path
                else:
                    line += "Â· "  # Free space
            print(line)
        print()


class AdvancedSearch(SearchAlgorithm):
    """
    Advanced search algorithms - for future expansion
    Could include A*, Dijkstra's, or other informed search methods
    """
    
    def __init__(self, maze):
        super().__init__(maze)
        self.heuristics_enabled = False
    
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def euclidean_distance(self, pos1, pos2):
        """Calculate Euclidean distance between two positions"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def greedy_search(self, start, goal):
        """
        Greedy Best-First Search - Future implementation
        Uses heuristics to guide search toward goal
        """
        # This would be implemented for informed search demonstration
        pass
    
    def a_star_search(self, start, goal):
        """
        A* Search - Future implementation  
        Combines actual cost + heuristic for optimal pathfinding
        """
        # This would be implemented for optimal informed search
        pass