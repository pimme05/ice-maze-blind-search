from collections import deque
import pygame
import sys
import time
import os
import math
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 12
GRID_HEIGHT = 9
CELL_SIZE = 60
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 350  # Extra space for UI
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 100
FPS = 60

# Star Wars Color Scheme
SPACE_BLACK = (10, 10, 20)
ICE_BLUE = (173, 216, 255)
WALL_GRAY = (60, 70, 85)
DARK_GRAY = (30, 35, 45)
REBEL_ORANGE = (255, 165, 0)
EMPIRE_RED = (220, 20, 60)
JEDI_GREEN = (50, 205, 50)
SABER_BLUE = (64, 164, 255)
FORCE_PURPLE = (138, 43, 226)
HOTH_WHITE = (245, 245, 255)
CONSOLE_GREEN = (0, 255, 127)
HOLOGRAM_CYAN = (0, 255, 255)
KEY_GOLD = (255, 215, 0)

class Maze:
    """Enhanced Maze class with multiple levels and collectibles"""
    
    def __init__(self, level=1):
        self.level = level
        self.key_collected = False
        self.key_pos = None
        self.load_level(level)
        
    def load_level(self, level):
        """Load different maze layouts based on level"""
        self.level = level
        self.key_collected = False
        
        if level == 1:
            # Level 1: Basic Hoth Landing Site
            self.grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            self.start_pos = (1, 1)
            self.goal_pos = (10, 7)
            self.key_pos = (5, 3)  # Key in the middle area
            
        elif level == 2:
            # Level 2: Ice Caverns - More complex
            self.grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            self.start_pos = (1, 1)
            self.goal_pos = (10, 7)
            self.key_pos = (2, 5)  # Key in lower left
            
        elif level == 3:
            # Level 3: Echo Base Approach - Most complex
            self.grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            self.start_pos = (1, 7)  # Start at bottom left
            self.goal_pos = (10, 1)  # Goal at top right
            self.key_pos = (6, 5)   # Key in center maze
            
        self.terrain_type = "ice"
    
    def is_wall(self, x, y):
        """Check if position contains an ice wall or obstacle"""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x] == 1
        return True
    
    def is_valid_pos(self, x, y):
        """Check if position is valid for movement"""
        return (0 <= y < len(self.grid) and 
                0 <= x < len(self.grid[0]) and 
                not self.is_wall(x, y))
    
    def slide_move(self, start_x, start_y, direction):
        """Simulate sliding movement on ice"""
        x, y = start_x, start_y
        dx, dy = 0, 0
        
        direction_map = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        if direction in direction_map:
            dx, dy = direction_map[direction]
        else:
            return None
        
        moves_made = 0
        while True:
            next_x, next_y = x + dx, y + dy
            
            if self.is_wall(next_x, next_y):
                break
                
            x, y = next_x, next_y
            moves_made += 1
            
            if moves_made > 20:
                break
        
        return (x, y) if (x, y) != (start_x, start_y) else None
    
    def collect_key(self, player_pos):
        """Check if player collected the key"""
        if not self.key_collected and player_pos == self.key_pos:
            self.key_collected = True
            return True
        return False
    
    def can_exit(self, player_pos):
        """Check if player can exit (must have key and be at goal)"""
        return self.key_collected and player_pos == self.goal_pos
    
    def get_level_name(self):
        """Get descriptive name for current level"""
        names = {
            1: "Hoth Landing Site",
            2: "Ice Caverns", 
            3: "Echo Base Approach"
        }
        return names.get(self.level, f"Level {self.level}")

class SearchAlgorithm:
    """Enhanced search algorithms that consider key collection"""
    
    def __init__(self, maze):
        self.maze = maze
        self.explored = set()
        self.path = []
        self.search_order = []
        self.algorithm_used = None
        self.nodes_expanded = 0
    
    def reset(self):
        """Reset all search data for a new search operation"""
        self.explored.clear()
        self.path.clear()
        self.search_order.clear()
        self.algorithm_used = None
        self.nodes_expanded = 0
    
    def get_neighbors(self, pos, has_key=False):
        """Get all reachable positions from current position"""
        x, y = pos
        neighbors = []
        directions = ['up', 'down', 'left', 'right']
        
        for direction in directions:
            new_pos = self.maze.slide_move(x, y, direction)
            if new_pos and new_pos not in self.explored:
                neighbors.append(new_pos)
        
        return neighbors
    
    def bfs_with_key(self, start, goal, key_pos):
        """BFS that must collect key before reaching goal"""
        from collections import deque
        
        self.reset()
        self.algorithm_used = "BFS with Key Collection"
        
        # State: (position, has_key, path)
        queue = deque([(start, False, [start])])
        # Explored: set of (position, has_key) tuples
        explored_states = set()
        explored_states.add((start, False))
        
        while queue:
            current_pos, has_key, path = queue.popleft()
            self.search_order.append(current_pos)
            self.nodes_expanded += 1
            
            # Collect key if we're at key position
            if current_pos == key_pos:
                has_key = True
            
            # Check if we've reached goal with key
            if current_pos == goal and has_key:
                self.path = path
                return True
            
            # Explore neighbors
            for neighbor in self.get_neighbors(current_pos):
                state = (neighbor, has_key)
                if state not in explored_states:
                    explored_states.add(state)
                    new_path = path + [neighbor]
                    queue.append((neighbor, has_key, new_path))
        
        return False
    
    def dfs_with_key(self, start, goal, key_pos):
        """DFS that must collect key before reaching goal"""
        self.reset()
        self.algorithm_used = "DFS with Key Collection"
        
        # State: (position, has_key, path)
        stack = [(start, False, [start])]
        explored_states = set()
        
        while stack:
            current_pos, has_key, path = stack.pop()
            
            state = (current_pos, has_key)
            if state in explored_states:
                continue
            
            explored_states.add(state)
            self.search_order.append(current_pos)
            self.nodes_expanded += 1
            
            # Collect key if we're at key position
            if current_pos == key_pos:
                has_key = True
            
            # Check if we've reached goal with key
            if current_pos == goal and has_key:
                self.path = path
                return True
            
            # Add neighbors to stack
            neighbors = self.get_neighbors(current_pos)
            for neighbor in reversed(neighbors):
                new_state = (neighbor, has_key)
                if new_state not in explored_states:
                    new_path = path + [neighbor]
                    stack.append((neighbor, has_key, new_path))
        
        return False

class StarWarsIceMazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Star Wars: Hoth Ice Maze - Multi-Level Mission")
        self.clock = pygame.time.Clock()
        
        # Fonts
        try:
            self.font = pygame.font.Font(None, 24)
            self.title_font = pygame.font.Font(None, 32)
            self.console_font = pygame.font.Font(None, 20)
        except:
            self.font = pygame.font.Font(None, 24)
            self.title_font = pygame.font.Font(None, 32)
            self.console_font = pygame.font.Font(None, 20)
        
        self.current_level = 1
        self.max_level = 3
        self.maze = Maze(self.current_level)
        self.search = SearchAlgorithm(self.maze)
        
        self.current_algorithm = None
        self.visualization_step = 0
        self.animating = False
        self.animation_speed = 8
        self.last_step_time = 0
        
        self.player_pos = self.maze.start_pos
        self.manual_mode = True
        self.solution_found = False
        
        # Animation effects
        self.glow_effect = 0
        self.scan_lines = 0
        self.key_glow = 0
        
        # Game state
        self.game_completed = False
    
    def load_images(self):
        """Load character and object images with fallback to drawn graphics"""
        images = {}
        image_files = {
            'player': 'pic1.png',           # Player character image
            'base': 'pic2.png',             # Base/goal image
            'key': 'key.png',               # Key image (optional)
            'wall': 'wall.png',             # Wall texture (optional)
            'background': 'background.png'   # Background image (optional)
        }
        
        for name, filename in image_files.items():
            try:
                # Try to load the image file
                import os
                if os.path.exists(filename):
                    original_image = pygame.image.load(filename).convert_alpha()
                    # Scale to fit cell size (with some padding)
                    scaled_image = pygame.transform.scale(original_image, (CELL_SIZE - 10, CELL_SIZE - 10))
                    images[name] = scaled_image
                    print(f"✓ Loaded {filename} for {name}")
                else:
                    images[name] = None
                    print(f"⚠ File {filename} not found, using drawn graphics for {name}")
            except Exception as e:
                # If any error occurs, use drawn graphics as fallback
                images[name] = None
                print(f"⚠ Error loading {filename}: {e}, using drawn graphics for {name}")
        
        return images
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.manual_mode and not self.animating:
                    # Manual player movement
                    new_pos = None
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        new_pos = self.maze.slide_move(*self.player_pos, 'up')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        new_pos = self.maze.slide_move(*self.player_pos, 'down')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        new_pos = self.maze.slide_move(*self.player_pos, 'left')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        new_pos = self.maze.slide_move(*self.player_pos, 'right')
                    
                    if new_pos:
                        self.player_pos = new_pos
                        
                        # Check for key collection
                        if self.maze.collect_key(self.player_pos):
                            print(f"Key collected on Level {self.current_level}!")
                        
                        # Check for level completion
                        if self.maze.can_exit(self.player_pos):
                            self.complete_level()
                
                # Algorithm controls
                if event.key == pygame.K_b and not self.animating:
                    self.start_bfs()
                elif event.key == pygame.K_d and not self.animating:
                    self.start_dfs()
                elif event.key == pygame.K_r:
                    self.reset_level()
                elif event.key == pygame.K_m:
                    self.toggle_mode()
                elif event.key == pygame.K_n and self.current_level < self.max_level:
                    self.next_level()
                elif event.key == pygame.K_p and self.current_level > 1:
                    self.previous_level()
        
        return True
    
    def complete_level(self):
        """Handle level completion"""
        if self.current_level < self.max_level:
            self.current_level += 1
            self.load_new_level()
            print(f"Level {self.current_level-1} completed! Moving to {self.maze.get_level_name()}")
        else:
            self.game_completed = True
            print("All levels completed! You've reached Echo Base!")
    
    def load_new_level(self):
        """Load a new level"""
        self.maze = Maze(self.current_level)
        self.search = SearchAlgorithm(self.maze)
        self.player_pos = self.maze.start_pos
        self.reset_search_state()
    
    def next_level(self):
        """Go to next level manually"""
        if self.current_level < self.max_level:
            self.current_level += 1
            self.load_new_level()
    
    def previous_level(self):
        """Go to previous level manually"""
        if self.current_level > 1:
            self.current_level -= 1
            self.load_new_level()
    
    def reset_level(self):
        """Reset current level"""
        self.maze.key_collected = False
        self.player_pos = self.maze.start_pos
        self.reset_search_state()
        self.game_completed = False
    
    def reset_search_state(self):
        """Reset search visualization state"""
        self.search.reset()
        self.current_algorithm = None
        self.visualization_step = 0
        self.animating = False
        self.manual_mode = True
        self.solution_found = False
    
    def start_bfs(self):
        """Start BFS with key collection"""
        self.current_algorithm = "REBEL SCANNER (BFS)"
        self.solution_found = self.search.bfs_with_key(
            self.maze.start_pos, self.maze.goal_pos, self.maze.key_pos)
        self.visualization_step = 0
        self.animating = True
        self.manual_mode = False
    
    def start_dfs(self):
        """Start DFS with key collection"""
        self.current_algorithm = "EMPIRE PROBE (DFS)"
        self.solution_found = self.search.dfs_with_key(
            self.maze.start_pos, self.maze.goal_pos, self.maze.key_pos)
        self.visualization_step = 0
        self.animating = True
        self.manual_mode = False
    
    def toggle_mode(self):
        self.manual_mode = not self.manual_mode
        if self.manual_mode:
            self.animating = False
    
    def update(self):
        current_time = time.time()
        
        # Update animation effects
        self.glow_effect = (self.glow_effect + 3) % 360
        self.scan_lines = (self.scan_lines + 2) % WINDOW_HEIGHT
        self.key_glow = (self.key_glow + 5) % 360
        
        if self.animating and current_time - self.last_step_time > (1.0 / self.animation_speed):
            if self.visualization_step < len(self.search.search_order):
                self.visualization_step += 1
                self.last_step_time = current_time
            else:
                self.animating = False
    
    def draw_key(self, pos):
        """Draw the collectible key - use image if available, otherwise draw it"""
        if self.maze.key_collected:
            return
            
        x, y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
        center_x, center_y = x + CELL_SIZE // 2, y + CELL_SIZE // 2
        
        # Try to use loaded key image first
        if self.images.get('key') is not None:
            # Animated glow effect around image
            glow_intensity = int(64 + 32 * math.sin(math.radians(self.key_glow)))
            
            # Draw glow background
            for radius in range(25, 15, -2):
                alpha = max(0, glow_intensity - (25 - radius) * 5)
                glow_surf = pygame.Surface((radius * 2, radius * 2))
                glow_surf.set_alpha(alpha)
                glow_surf.fill(KEY_GOLD)
                glow_rect = glow_surf.get_rect(center=(center_x, center_y))
                self.screen.blit(glow_surf, glow_rect)
            
            # Draw the key image
            key_rect = self.images['key'].get_rect(center=(center_x, center_y))
            self.screen.blit(self.images['key'], key_rect)
            
        else:
            # Fallback to drawn key (original code)
            glow_intensity = int(128 + 64 * math.sin(math.radians(self.key_glow)))
            
            # Outer glow
            for radius in range(25, 15, -2):
                alpha = max(0, glow_intensity - (25 - radius) * 10)
                glow_surf = pygame.Surface((radius * 2, radius * 2))
                glow_surf.set_alpha(alpha)
                glow_surf.fill(KEY_GOLD)
                glow_rect = glow_surf.get_rect(center=(center_x, center_y))
                self.screen.blit(glow_surf, glow_rect)
            
            # Key body
            pygame.draw.circle(self.screen, KEY_GOLD, (center_x, center_y), 12)
            pygame.draw.circle(self.screen, (200, 180, 0), (center_x, center_y), 12, 2)
            
            # Key hole
            pygame.draw.circle(self.screen, SPACE_BLACK, (center_x, center_y), 4)
            
            # Key teeth
            pygame.draw.rect(self.screen, KEY_GOLD, (center_x + 8, center_y - 2, 8, 4))
            pygame.draw.rect(self.screen, KEY_GOLD, (center_x + 12, center_y - 1, 4, 2))
            
            # Star Wars symbol on key
            points = []
            for i in range(5):
                angle = math.radians(i * 72 - 90)
                points.append((center_x + 6 * math.cos(angle), center_y + 6 * math.sin(angle)))
            if len(points) >= 3:
                pygame.draw.polygon(self.screen, EMPIRE_RED, points)
    
    def draw_character(self, pos, char_type="rebel"):
        """Draw Star Wars characters - use images if available, otherwise draw them"""
        x, y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
        center_x, center_y = x + CELL_SIZE // 2, y + CELL_SIZE // 2
        
        if char_type == "rebel":
            # Try to use loaded player image first
            if self.images.get('player') is not None:
                # Draw the player image
                player_rect = self.images['player'].get_rect(center=(center_x, center_y))
                self.screen.blit(self.images['player'], player_rect)
                
                # Add key indicator if collected (small overlay)
                if self.maze.key_collected:
                    key_indicator_pos = (center_x + 20, center_y - 20)
                    pygame.draw.circle(self.screen, KEY_GOLD, key_indicator_pos, 8)
                    pygame.draw.circle(self.screen, (200, 180, 0), key_indicator_pos, 8, 2)
                    # Mini key symbol
                    pygame.draw.circle(self.screen, SPACE_BLACK, key_indicator_pos, 3)
                    
            else:
                # Fallback to drawn rebel pilot (original code)
                pygame.draw.circle(self.screen, REBEL_ORANGE, (center_x, center_y - 5), 18)
                pygame.draw.circle(self.screen, DARK_GRAY, (center_x, center_y - 5), 18, 3)
                
                # Visor
                pygame.draw.ellipse(self.screen, SABER_BLUE, 
                                  (center_x - 12, center_y - 12, 24, 10))
                
                # Body
                pygame.draw.ellipse(self.screen, REBEL_ORANGE, 
                                  (center_x - 10, center_y + 5, 20, 15))
                
                # Key indicator if collected
                if self.maze.key_collected:
                    pygame.draw.circle(self.screen, KEY_GOLD, (center_x + 15, center_y - 15), 6)
                    pygame.draw.circle(self.screen, (200, 180, 0), (center_x + 15, center_y - 15), 6, 2)
            
        elif char_type == "base":
            # Try to use loaded base image first
            if self.images.get('base') is not None:
                # Draw the base image
                base_rect = self.images['base'].get_rect(center=(center_x, center_y))
                self.screen.blit(self.images['base'], base_rect)
                
                # Add level indicator overlay
                level_bg = pygame.Surface((20, 20))
                level_bg.fill(DARK_GRAY)
                level_bg.set_alpha(180)
                level_bg_rect = level_bg.get_rect(center=(center_x, center_y + 20))
                self.screen.blit(level_bg, level_bg_rect)
                
                level_surf = self.console_font.render(str(self.current_level), True, HOTH_WHITE)
                level_rect = level_surf.get_rect(center=(center_x, center_y + 20))
                self.screen.blit(level_surf, level_rect)
                
            else:
                # Fallback to drawn base (original code)
                base_color = ICE_BLUE if self.current_level == 1 else JEDI_GREEN if self.current_level == 2 else FORCE_PURPLE
                
                pygame.draw.polygon(self.screen, base_color, [
                    (center_x, center_y - 15),
                    (center_x - 15, center_y + 10),
                    (center_x + 15, center_y + 10)
                ])
                
                # Level indicator
                level_surf = self.console_font.render(str(self.current_level), True, HOTH_WHITE)
                level_rect = level_surf.get_rect(center=(center_x, center_y))
                self.screen.blit(level_surf, level_rect)
    
    def draw_grid(self):
        """Enhanced grid drawing with level-specific styling"""
        # Dynamic background based on level
        bg_colors = [SPACE_BLACK, (20, 20, 40), (40, 20, 40)]
        self.screen.fill(bg_colors[self.current_level - 1])
        
        # Level-specific stars
        random.seed(42 + self.current_level)
        star_count = 30 + self.current_level * 10
        for _ in range(star_count):
            x = random.randint(0, GRID_WIDTH * CELL_SIZE)
            y = random.randint(0, GRID_HEIGHT * CELL_SIZE)
            pygame.draw.circle(self.screen, HOTH_WHITE, (x, y), 1)
        
        # Draw maze with level-specific wall colors
        wall_colors = [WALL_GRAY, (85, 70, 60), (85, 60, 85)]
        wall_color = wall_colors[self.current_level - 1]
        
        for y in range(len(self.maze.grid)):
            for x in range(len(self.maze.grid[0])):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(self.screen, wall_color, rect)
                    pygame.draw.rect(self.screen, ICE_BLUE, rect, 2)
                else:
                    pygame.draw.rect(self.screen, HOTH_WHITE, rect)
                    pygame.draw.rect(self.screen, ICE_BLUE, rect, 1)
        
        # Draw search visualization
        if not self.manual_mode and self.search.search_order:
            for i in range(min(self.visualization_step, len(self.search.search_order))):
                pos = self.search.search_order[i]
                rect = pygame.Rect(pos[0] * CELL_SIZE + 5, pos[1] * CELL_SIZE + 5, 
                                 CELL_SIZE - 10, CELL_SIZE - 10)
                
                color = SABER_BLUE if "BFS" in str(self.current_algorithm) else EMPIRE_RED
                
                glow_surf = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10))
                glow_surf.set_alpha(80)
                glow_surf.fill(color)
                self.screen.blit(glow_surf, (pos[0] * CELL_SIZE + 5, pos[1] * CELL_SIZE + 5))
        
        # Draw solution path
        if not self.manual_mode and not self.animating and self.solution_found:
            for pos in self.search.path:
                if pos == self.maze.start_pos or pos == self.maze.goal_pos:
                    continue
                    
                rect = pygame.Rect(pos[0] * CELL_SIZE + 15, pos[1] * CELL_SIZE + 15, 
                                 CELL_SIZE - 30, CELL_SIZE - 30)
                
                path_surf = pygame.Surface((CELL_SIZE - 30, CELL_SIZE - 30))
                path_surf.set_alpha(128)
                path_surf.fill(JEDI_GREEN)
                self.screen.blit(path_surf, (pos[0] * CELL_SIZE + 15, pos[1] * CELL_SIZE + 15))
    
    def draw_entities(self):
        """Draw all game entities"""
        # Draw key (if not collected)
        self.draw_key(self.maze.key_pos)
        
        # Draw goal
        self.draw_character(self.maze.goal_pos, "base")
        
        # Draw player
        if self.manual_mode:
            self.draw_character(self.player_pos, "rebel")
        else:
            self.draw_character(self.maze.start_pos, "rebel")
    
    def draw_ui(self):
        """Enhanced UI with level progression"""
        ui_x = GRID_WIDTH * CELL_SIZE + 20
        ui_y = 20
        
        # UI background
        ui_bg = pygame.Rect(ui_x - 10, ui_y - 10, 320, WINDOW_HEIGHT - 40)
        pygame.draw.rect(self.screen, DARK_GRAY, ui_bg)
        pygame.draw.rect(self.screen, HOLOGRAM_CYAN, ui_bg, 2)
        
        # Title with level info
        title_text = f"LEVEL {self.current_level}: {self.maze.get_level_name().upper()}"
        title = self.title_font.render(title_text, True, HOLOGRAM_CYAN)
        self.screen.blit(title, (ui_x, ui_y))
        
        # Progress indicator
        progress_text = f"PROGRESS: {self.current_level}/{self.max_level}"
        progress = self.console_font.render(progress_text, True, CONSOLE_GREEN)
        self.screen.blit(progress, (ui_x, ui_y + 35))
        
        ui_y += 70
        
        # Mission briefing
        briefing = [
            "MISSION: Collect key, reach base",
            f"KEY: {'COLLECTED' if self.maze.key_collected else 'FIND THE GOLDEN KEY'}",
            "",
            "CONTROLS:",
            "WASD/Arrows - Move pilot",
            "B - Rebel Scanner (BFS)",
            "D - Empire Probe (DFS)", 
            "R - Reset level",
            "N/P - Next/Previous level",
            "M - Toggle control mode",
            "",
            f"MODE: {('MANUAL PILOT' if self.manual_mode else 'AI NAVIGATION')}",
        ]
        
        if self.current_algorithm:
            briefing.extend([
                "",
                f"SCANNER: {self.current_algorithm}",
                f"SECTORS: {len(self.search.explored)}",
                f"STATUS: {'ROUTE FOUND' if self.solution_found else 'SEARCHING...'}",
            ])
        
        # Color coding for different info types
        for i, line in enumerate(briefing):
            if "LEVEL" in line or "MISSION:" in line:
                color = HOLOGRAM_CYAN
            elif "KEY:" in line:
                color = KEY_GOLD if not self.maze.key_collected else JEDI_GREEN
            elif "CONTROLS:" in line or "SCANNER:" in line:
                color = REBEL_ORANGE
            elif line.startswith("STATUS:") or line.startswith("MODE:"):
                color = CONSOLE_GREEN
            elif line == "":
                color = SPACE_BLACK
            else:
                color = HOTH_WHITE
                
            text = self.console_font.render(line, True, color)
            self.screen.blit(text, (ui_x, ui_y + i * 22))
        
        # Level completion status
        if self.manual_mode and self.maze.can_exit(self.player_pos):
            if self.current_level < self.max_level:
                win_text = "LEVEL COMPLETE!"
                win_color = JEDI_GREEN
            else:
                win_text = "MISSION COMPLETE!"
                win_color = FORCE_PURPLE
                
            win_bg = pygame.Rect(ui_x - 5, ui_y + len(briefing) * 22 + 20, 250, 40)
            pygame.draw.rect(self.screen, win_color, win_bg)
            pygame.draw.rect(self.screen, CONSOLE_GREEN, win_bg, 3)
            
            win_surface = self.title_font.render(win_text, True, SPACE_BLACK)
            self.screen.blit(win_surface, (ui_x, ui_y + len(briefing) * 22 + 30))
        
        # Game completion message
        elif self.game_completed:
            complete_bg = pygame.Rect(ui_x - 5, ui_y + len(briefing) * 22 + 20, 280, 60)
            pygame.draw.rect(self.screen, FORCE_PURPLE, complete_bg)
            pygame.draw.rect(self.screen, KEY_GOLD, complete_bg, 3)
            
            complete_text1 = self.title_font.render("ALL LEVELS", True, HOTH_WHITE)
            complete_text2 = self.title_font.render("COMPLETED!", True, HOTH_WHITE)
            self.screen.blit(complete_text1, (ui_x, ui_y + len(briefing) * 22 + 25))
            self.screen.blit(complete_text2, (ui_x, ui_y + len(briefing) * 22 + 45))
        
        # Key collection indicator
        if not self.maze.key_collected:
            key_indicator_y = ui_y + len(briefing) * 22 + 80
            key_text = "⚠ FIND THE KEY FIRST!"
            key_surface = self.console_font.render(key_text, True, KEY_GOLD)
            
            # Blinking effect
            alpha = int(128 + 127 * math.sin(math.radians(self.key_glow * 2)))
            key_surface.set_alpha(alpha)
            self.screen.blit(key_surface, (ui_x, key_indicator_y))
        
        # Scan lines effect
        for i in range(0, WINDOW_HEIGHT, 4):
            alpha = 20 if (i + self.scan_lines) % 8 < 4 else 10
            scan_surf = pygame.Surface((WINDOW_WIDTH, 1))
            scan_surf.set_alpha(alpha)
            scan_surf.fill(HOLOGRAM_CYAN)
            self.screen.blit(scan_surf, (0, i))
    
    def draw(self):
        """Main drawing function"""
        self.draw_grid()
        self.draw_entities()
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = StarWarsIceMazeGame()
    game.run()