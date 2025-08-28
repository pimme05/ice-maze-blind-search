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
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 350
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
    """Maze class with single level and collectible key"""
    
    def __init__(self):
        self.key_collected = False
        self.load_level()
        
    def load_level(self):
        """Load the single maze layout"""
        self.key_collected = False
        
        # Single level: Hoth Landing Site
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
        self.key_pos = (5, 3)
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

class SearchAlgorithm:
    """Search algorithms that consider key collection"""
    
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
    
    def get_neighbors(self, pos):
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
            
            # ADD THIS LINE: Update the main explored set for UI display
            self.explored.add(current_pos)
            
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
            
            # ADD THIS LINE: Update the main explored set for UI display
            self.explored.add(current_pos)
            
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
        pygame.display.set_caption("Star Wars: Hoth Ice Maze - Collect Key & Reach Base")
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
        
        # Load images
        self.images = self.load_images()
        
        self.maze = Maze()
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
        self.show_start_screen = True
    
    def load_images(self):
        """Load character and object images with fallback to drawn graphics"""
        images = {}
        image_files = {
            'player': 'pic1.png',
            'base': 'pic2.png',
            'key': 'key.png',
        }
        
        for name, filename in image_files.items():
            try:
                if os.path.exists(filename):
                    original_image = pygame.image.load(filename).convert_alpha()
                    scaled_image = pygame.transform.scale(original_image, (CELL_SIZE - 10, CELL_SIZE - 10))
                    images[name] = scaled_image
                    print(f"✓ Loaded {filename} for {name}")
                else:
                    images[name] = None
                    print(f"⚠ File {filename} not found, using drawn graphics for {name}")
            except Exception as e:
                images[name] = None
                print(f"⚠ Error loading {filename}: {e}")
        
        return images
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Start screen controls
                if self.show_start_screen:
                    if event.key == pygame.K_1:
                        self.manual_mode = True
                        self.show_start_screen = False
                        print("Human mode selected!")
                    elif event.key == pygame.K_2:
                        self.manual_mode = False
                        self.show_start_screen = False
                        print("AI mode selected!")
                    elif event.key == pygame.K_ESCAPE:
                        return False
                    return True
                
                # Game completion screen
                if self.game_completed:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        self.start_new_game()
                    elif event.key == pygame.K_m:
                        self.toggle_mode()  # Just toggle mode, don't reset
                    elif event.key == pygame.K_ESCAPE:
                        self.show_start_screen = True
                        self.reset_game()
                    return True
                
                # In-game controls
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
                            print("Key collected!")
                        
                        # Check for game completion
                        if self.maze.can_exit(self.player_pos):
                            self.game_completed = True
                            print("Mission Complete!")
                
                # Algorithm controls (available in both modes)
                if event.key == pygame.K_b and not self.animating:
                    if not self.manual_mode:
                        self.start_bfs()
                elif event.key == pygame.K_d and not self.animating:
                    if not self.manual_mode:
                        self.start_dfs()
                elif event.key == pygame.K_r:
                    self.start_new_game()
                elif event.key == pygame.K_m:
                    self.toggle_mode()  # Toggle mode in-game
                elif event.key == pygame.K_t:
                    self.show_possible_moves()
                elif event.key == pygame.K_h:
                    self.show_hint_path()
                elif event.key == pygame.K_ESCAPE:
                    self.show_start_screen = True
                    self.reset_game()
        
        return True
    
    def start_new_game(self):
        """Start a completely new game"""
        self.reset_game()
        self.show_start_screen = True
        print("Starting new game...")
    
    def reset_game(self):
        """Reset the game state"""
        self.maze.key_collected = False
        self.player_pos = self.maze.start_pos
        self.search.reset()
        self.current_algorithm = None
        self.visualization_step = 0
        self.animating = False
        self.solution_found = False
        self.game_completed = False
    
    def toggle_mode(self):
        """Toggle between manual and AI mode with visual feedback"""
        self.manual_mode = not self.manual_mode
        if self.manual_mode:
            self.animating = False
            self.search.reset()  # Clear any AI search data
            print("Switched to HUMAN mode - Take control of your AT-AT!")
        else:
            print("Switched to AI mode - Use B for BFS or D for DFS algorithms!")
    
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
    
    def show_possible_moves(self):
        """Debug function to show all possible moves from current position"""
        if self.manual_mode:
            print(f"\n=== POSSIBLE MOVES FROM {self.player_pos} ===")
            directions = ['up', 'down', 'left', 'right']
            for direction in directions:
                new_pos = self.maze.slide_move(*self.player_pos, direction)
                if new_pos:
                    print(f"{direction.upper()}: {self.player_pos} → {new_pos}")
                else:
                    print(f"{direction.upper()}: No movement possible")
            print(f"Key position: {self.maze.key_pos}")
            print(f"Goal position: {self.maze.goal_pos}")
            print(f"Key collected: {self.maze.key_collected}")
            print("=" * 50)
    
    def show_hint_path(self):
        """Show a hint about how to solve the level"""
        print(f"\n=== HOTH MAZE SOLUTION HINT ===")
        print("This maze has multiple solution paths!")
        print("Try different combinations of moves to collect the key first,")
        print("then navigate to the goal.")
        print(f"Key position: {self.maze.key_pos}")
        print(f"Goal position: {self.maze.goal_pos}")
        print("Remember: You slide until you hit a wall!")
        print("=" * 50)
    
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
        """Draw the collectible key"""
        if self.maze.key_collected:
            return
            
        x, y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
        center_x, center_y = x + CELL_SIZE // 2, y + CELL_SIZE // 2
        
        # Try to use loaded key image first
        if self.images.get('key') is not None:
            key_rect = self.images['key'].get_rect(center=(center_x, center_y))
            self.screen.blit(self.images['key'], key_rect)
        else:
            # Fallback to drawn key
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
            pygame.draw.circle(self.screen, SPACE_BLACK, (center_x, center_y), 4)
            pygame.draw.rect(self.screen, KEY_GOLD, (center_x + 8, center_y - 2, 8, 4))
    
    def draw_character(self, pos, char_type="rebel"):
        """Draw Star Wars characters"""
        x, y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
        center_x, center_y = x + CELL_SIZE // 2, y + CELL_SIZE // 2
        
        if char_type == "rebel":
            # Try to use loaded player image first
            if self.images.get('player') is not None:
                player_rect = self.images['player'].get_rect(center=(center_x, center_y))
                self.screen.blit(self.images['player'], player_rect)
                
                # Add key indicator if collected
                if self.maze.key_collected:
                    key_indicator_pos = (center_x + 20, center_y - 20)
                    pygame.draw.circle(self.screen, KEY_GOLD, key_indicator_pos, 8)
                    pygame.draw.circle(self.screen, (200, 180, 0), key_indicator_pos, 8, 2)
                    pygame.draw.circle(self.screen, SPACE_BLACK, key_indicator_pos, 3)
            else:
                # Fallback to drawn rebel pilot
                pygame.draw.circle(self.screen, REBEL_ORANGE, (center_x, center_y - 5), 18)
                pygame.draw.circle(self.screen, DARK_GRAY, (center_x, center_y - 5), 18, 3)
                pygame.draw.ellipse(self.screen, SABER_BLUE, (center_x - 12, center_y - 12, 24, 10))
                pygame.draw.ellipse(self.screen, REBEL_ORANGE, (center_x - 10, center_y + 5, 20, 15))
                
                if self.maze.key_collected:
                    pygame.draw.circle(self.screen, KEY_GOLD, (center_x + 15, center_y - 15), 6)
            
        elif char_type == "base":
            # Try to use loaded base image first
            if self.images.get('base') is not None:
                base_rect = self.images['base'].get_rect(center=(center_x, center_y))
                self.screen.blit(self.images['base'], base_rect)
            else:
                # Fallback to drawn base
                pygame.draw.polygon(self.screen, ICE_BLUE, [
                    (center_x, center_y - 15),
                    (center_x - 15, center_y + 10),
                    (center_x + 15, center_y + 10)
                ])
                level_surf = self.console_font.render("BASE", True, HOTH_WHITE)
                level_rect = level_surf.get_rect(center=(center_x, center_y))
                self.screen.blit(level_surf, level_rect)
    
    def draw_grid(self):
        """Draw the maze grid"""
        # Space background with stars
        self.screen.fill(SPACE_BLACK)
        
        # Add stars
        random.seed(42)
        for _ in range(50):
            x = random.randint(0, GRID_WIDTH * CELL_SIZE)
            y = random.randint(0, GRID_HEIGHT * CELL_SIZE)
            pygame.draw.circle(self.screen, HOTH_WHITE, (x, y), 1)
        
        # Draw maze
        for y in range(len(self.maze.grid)):
            for x in range(len(self.maze.grid[0])):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(self.screen, WALL_GRAY, rect)
                    pygame.draw.rect(self.screen, ICE_BLUE, rect, 2)
                else:
                    pygame.draw.rect(self.screen, HOTH_WHITE, rect)
                    pygame.draw.rect(self.screen, ICE_BLUE, rect, 1)
        
        # Draw search visualization
        if not self.manual_mode and self.search.search_order:
            for i in range(min(self.visualization_step, len(self.search.search_order))):
                pos = self.search.search_order[i]
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
                path_surf = pygame.Surface((CELL_SIZE - 30, CELL_SIZE - 30))
                path_surf.set_alpha(128)
                path_surf.fill(JEDI_GREEN)
                self.screen.blit(path_surf, (pos[0] * CELL_SIZE + 15, pos[1] * CELL_SIZE + 15))
    
    def draw_entities(self):
        """Draw all game entities"""
        self.draw_key(self.maze.key_pos)
        self.draw_character(self.maze.goal_pos, "base")
        
        if self.manual_mode:
            self.draw_character(self.player_pos, "rebel")
        else:
            self.draw_character(self.maze.start_pos, "rebel")
    
    def draw_start_screen(self):
        """Draw the start/mode selection screen"""
        self.screen.fill(SPACE_BLACK)
        
        # Add stars background
        random.seed(42)
        for _ in range(100):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            pygame.draw.circle(self.screen, HOTH_WHITE, (x, y), 1)
        
        # Main title
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("STAR WARS: HOTH ICE MAZE", True, HOLOGRAM_CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.title_font.render("Escape to Echo Base", True, CONSOLE_GREEN)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Mode selection
        mode_title = self.title_font.render("SELECT GAME MODE:", True, REBEL_ORANGE)
        mode_rect = mode_title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(mode_title, mode_rect)
        
        # Human mode option
        human_bg = pygame.Rect(WINDOW_WIDTH // 2 - 200, 250, 180, 80)
        pygame.draw.rect(self.screen, JEDI_GREEN, human_bg)
        pygame.draw.rect(self.screen, CONSOLE_GREEN, human_bg, 3)
        
        human_text1 = self.title_font.render("1 - HUMAN", True, SPACE_BLACK)
        human_text2 = self.console_font.render("Control AT-AT manually", True, SPACE_BLACK)
        human_rect1 = human_text1.get_rect(center=(human_bg.centerx, human_bg.centery - 10))
        human_rect2 = human_text2.get_rect(center=(human_bg.centerx, human_bg.centery + 15))
        self.screen.blit(human_text1, human_rect1)
        self.screen.blit(human_text2, human_rect2)
        
        # AI mode option
        ai_bg = pygame.Rect(WINDOW_WIDTH // 2 + 20, 250, 180, 80)
        pygame.draw.rect(self.screen, EMPIRE_RED, ai_bg)
        pygame.draw.rect(self.screen, (150, 0, 0), ai_bg, 3)
        
        ai_text1 = self.title_font.render("2 - AI", True, HOTH_WHITE)
        ai_text2 = self.console_font.render("Watch algorithms solve", True, HOTH_WHITE)
        ai_rect1 = ai_text1.get_rect(center=(ai_bg.centerx, ai_bg.centery - 10))
        ai_rect2 = ai_text2.get_rect(center=(ai_bg.centerx, ai_bg.centery + 15))
        self.screen.blit(ai_text1, ai_rect1)
        self.screen.blit(ai_text2, ai_rect2)
        
        # Instructions
        instructions = [
            "MISSION: Collect the golden key, then reach Echo Base",
            "Use WASD or Arrow keys to move your AT-AT",
            "Remember: You slide on ice until you hit a wall!",
            "",
            "Press 1 for Human Mode  |  Press 2 for AI Mode",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            color = HOTH_WHITE if instruction else SPACE_BLACK
            if "MISSION:" in instruction:
                color = KEY_GOLD
            elif "Press" in instruction:
                color = HOLOGRAM_CYAN
                
            text = self.console_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 380 + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_completion_screen(self):
        """Draw the game completion screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(SPACE_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Victory message
        victory_font = pygame.font.Font(None, 64)
        victory_text = victory_font.render("MISSION COMPLETE!", True, JEDI_GREEN)
        victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(victory_text, victory_rect)
        
        # Success message
        success_text = self.title_font.render("Welcome to Echo Base, Rebel!", True, CONSOLE_GREEN)
        success_rect = success_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(success_text, success_rect)
        
        # Options
        options = [
            "R or SPACE - Start New Game",
            "M - Toggle Mode (Human/AI)", 
            "ESC - Main Menu"
        ]
        
        for i, option in enumerate(options):
            option_text = self.console_font.render(option, True, HOLOGRAM_CYAN)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 30))
            self.screen.blit(option_text, option_rect)
    
    def draw_ui(self):
        """Simple UI for single level game"""
        ui_x = GRID_WIDTH * CELL_SIZE + 20
        ui_y = 20
        
        # UI background
        ui_bg = pygame.Rect(ui_x - 10, ui_y - 10, 320, WINDOW_HEIGHT - 40)
        pygame.draw.rect(self.screen, DARK_GRAY, ui_bg)
        pygame.draw.rect(self.screen, HOLOGRAM_CYAN, ui_bg, 2)
        
        # Title
        title = self.title_font.render("HOTH ICE MAZE", True, HOLOGRAM_CYAN)
        self.screen.blit(title, (ui_x, ui_y))
        
        mission = self.console_font.render("ESCAPE TO ECHO BASE", True, CONSOLE_GREEN)
        self.screen.blit(mission, (ui_x, ui_y + 35))
        
        ui_y += 70
        
        # Current mode indicator with toggle button
        mode_bg = pygame.Rect(ui_x - 5, ui_y - 5, 200, 35)
        mode_color = JEDI_GREEN if self.manual_mode else EMPIRE_RED
        pygame.draw.rect(self.screen, mode_color, mode_bg)
        pygame.draw.rect(self.screen, HOTH_WHITE, mode_bg, 2)
        
        mode_text = f"MODE: {'HUMAN' if self.manual_mode else 'AI'} (Press M to toggle)"
        mode_surface = self.console_font.render(mode_text, True, SPACE_BLACK if self.manual_mode else HOTH_WHITE)
        self.screen.blit(mode_surface, (ui_x, ui_y + 5))
        ui_y += 50
        
        # Mission briefing
        briefing = [
            "MISSION: Collect key, reach base",
            f"KEY: {'COLLECTED' if self.maze.key_collected else 'FIND THE GOLDEN KEY'}",
            "",
        ]
        
        if self.manual_mode:
            briefing.extend([
                "HUMAN CONTROLS:",
                "WASD/Arrows - Move AT-AT",
                "M - Switch to AI mode",
                "R - Start new game",
                "T - Show possible moves",
                "H - Show hints",
                "ESC - Main menu",
            ])
        else:
            briefing.extend([
                "AI CONTROLS:",
                "B - Run BFS (Breadth-First)",
                "D - Run DFS (Depth-First)",
                "M - Switch to Human mode", 
                "R - Start new game",
                "ESC - Main menu",
            ])
        
        if self.current_algorithm:
            briefing.extend([
                "",
                f"SCANNER: {self.current_algorithm}",
                f"SECTORS: {len(self.search.explored)}",
                f"STATUS: {'ROUTE FOUND' if self.solution_found else 'SEARCHING...'}",
            ])
        
        # Draw briefing
        for i, line in enumerate(briefing):
            if "MISSION:" in line:
                color = HOLOGRAM_CYAN
            elif "KEY:" in line:
                color = KEY_GOLD if not self.maze.key_collected else JEDI_GREEN
            elif "CONTROLS:" in line or "SCANNER:" in line:
                color = REBEL_ORANGE
            elif line.startswith("STATUS:"):
                color = CONSOLE_GREEN
            elif line == "":
                color = SPACE_BLACK
            else:
                color = HOTH_WHITE
                
            text = self.console_font.render(line, True, color)
            self.screen.blit(text, (ui_x, ui_y + i * 22))
        
        # Win condition
        if self.manual_mode and self.maze.can_exit(self.player_pos):
            win_bg = pygame.Rect(ui_x - 5, ui_y + len(briefing) * 22 + 20, 250, 40)
            pygame.draw.rect(self.screen, JEDI_GREEN, win_bg)
            pygame.draw.rect(self.screen, CONSOLE_GREEN, win_bg, 3)
            
            win_surface = self.title_font.render("MISSION COMPLETE!", True, SPACE_BLACK)
            self.screen.blit(win_surface, (ui_x, ui_y + len(briefing) * 22 + 30))
        
        # Key collection indicator
        if not self.maze.key_collected:
            key_indicator_y = ui_y + len(briefing) * 22 + 80
            key_text = "⚠ FIND THE KEY FIRST!"
            key_surface = self.console_font.render(key_text, True, KEY_GOLD)
            
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
        if self.show_start_screen:
            self.draw_start_screen()
        else:
            self.draw_grid()
            self.draw_entities()
            self.draw_ui()
            
            # Draw completion screen overlay if game is complete
            if self.game_completed:
                self.draw_completion_screen()
                
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