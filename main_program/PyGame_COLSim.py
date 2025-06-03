import pygame
import random
import sys
from DStarLiteCOLREG import DStarLiteCOLREG
from generate_grid import *

# Constants
WIDTH, HEIGHT = 1000,800
GRID_SIZE = 30
BUTTON_HEIGHT = 50
G_WIDTH, G_HEIGHT = WIDTH, HEIGHT - BUTTON_HEIGHT # grid width and height

# --- Colours ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEEP_BLUE = (25, 118, 210)
SHALLOW_BLUE = (100, 181, 246)
DARK_GREEN = (0, 100, 0)
SAND = (239, 221, 111)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
HOT_PINK = (255, 0, 234)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COLSim")
clock = pygame.time.Clock()
running = True
current_step = 0
grid = generate_grid(G_WIDTH,G_HEIGHT) # generate grid coordinates using provided grid constraints
player = False

# Buttons setup
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - BUTTON_HEIGHT + 10, 150, 30)
player_button_rect = pygame.Rect(WIDTH - 200, HEIGHT - BUTTON_HEIGHT + 10, 150, 30)
environment_button = pygame.Rect(WIDTH - 375, HEIGHT - BUTTON_HEIGHT + 10, 150, 30)
button_text = "Start Simulation"

# Controllable vessel setup
player_pos = [WIDTH // 2, HEIGHT // 2]  # Starting position
player_speed = 2
player_size = 15
future_pos = [0,0] # 
last_key = pygame.K_SPACE # last direction key

# Simulation
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT - BUTTON_HEIGHT))
    for y in range(0, HEIGHT - BUTTON_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH , y))

def draw_path(path):
    pygame.draw.lines(screen, GRAY, False, path, 10)

def draw_obstacle(obstacle):
    for (x,y) in (obstacle):
        pygame.draw.circle(screen, GRAY, (x, y), 1, 1)

def draw_agent(position):
    global current_color_index
    pygame.draw.circle(screen, colors[current_color_index % len(colors)], position, 10)
    current_color_index += 1  

def draw_player():
    global player, collision_risk
    if player:
        if collision_risk:
            colour = HOT_PINK
        else:
            colour = ORANGE
        pygame.draw.circle(screen, colour, (int(player_pos[0]), int(player_pos[1])), player_size)

def remove_agent(position):
    x, y = position
    pygame.draw.circle(screen, WHITE, (x, y), 10)

def draw_goal(goal):
    x, y = goal
    pygame.draw.circle(screen, colors[current_color_index % len(colors)], (x, y), 15)

def draw_player_button():
    pygame.draw.rect(screen, ORANGE if current_player == State.PLAYER else GRAY, player_button_rect)
    font = pygame.font.SysFont(None, 24)
    if current_player == State.PLAYER:
        button_text = "Player Active"
    else:
        button_text = "Player Not Active"
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=player_button_rect.center)
    screen.blit(text, text_rect)

def draw_button():
    pygame.draw.rect(screen, BLUE if current_state == State.SETTING_AGENTS else GRAY, button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def draw_env_button():
    global current_env
    pygame.draw.rect(screen, DARK_GREEN if current_env == State.ENVIRONMENT else GRAY, environment_button)
    font = pygame.font.SysFont(None, 24)
    if current_env == State.ENVIRONMENT:
        button_text = "Env Active"
    else:
        button_text = "Env Not Active"
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=environment_button.center)
    screen.blit(text, text_rect)

def draw_text():
    # Display current state
    font = pygame.font.SysFont(None, 24)
    state_texts = {
        State.SETTING_AGENTS: "Please select agent starting location",
        State.SETTING_GOAL: "Please select agent goal",
        State.SIMULATING: "Simulation running",
        State.Calculating: "Calculating Paths",
    }
    text = font.render(state_texts[current_state], True, BLACK)
    screen.blit(text, (10, HEIGHT - BUTTON_HEIGHT + 15))

def draw_objects():
    for goal in goals:
        x, y = goal
        colour = goal_colours.get(goal, RED)
        pygame.draw.circle(screen, colour, (x, y), 15)
    
    # Draw agents and their paths
    for agent_pos, _ in agents_pos.items():
        # Draw agent
        colour = agent_colors.get(agent_pos, RED) # find colour assigned to agent, if not default to red
        pygame.draw.circle(screen, colour, (agent_pos[0], agent_pos[1]), 10)

def calculate_paths(agents):
    global agent_paths, searched
    for agent, start in agents:
        path = agent.move_and_replan(start)
        agent_paths.update({agent: path})
        path_list.append(path)
        searched = agent.searched_nodes()

def midpoint_displacement(start, end, roughness, vertical_displacement, num_of_iterations):
    """Generate a fractal line using midpoint displacement algorithm."""
    points = [start, end]
    
    for _ in range(num_of_iterations):
        for i in range(len(points)-1, 0, -1):
            mid = ((points[i-1][0] + points[i][0])/2, 
                   (points[i-1][1] + points[i][1])/2 + random.uniform(-1, 1) * vertical_displacement)
            points.insert(i, mid)
        vertical_displacement *= roughness
    
    return points

def draw_environment(coastline):
    """Draw the entire environment with water, land, and islands."""
    # Draw gradient water background
    for y in range(HEIGHT):
        # Interpolate between deep and shallow blue
        ratio = y / HEIGHT
        r = int(SHALLOW_BLUE[0] * ratio + DEEP_BLUE[0] * (1 - ratio))
        g = int(SHALLOW_BLUE[1] * ratio + DEEP_BLUE[1] * (1 - ratio))
        b = int(SHALLOW_BLUE[2] * ratio + DEEP_BLUE[2] * (1 - ratio))
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    
    # Draw the land (polygon from coastline to screen bottom)
    land_polygon = coastline + [(WIDTH, HEIGHT), (0, HEIGHT)]
    pygame.draw.polygon(screen, SAND, land_polygon)
    
    # Draw the coastline
    pygame.draw.lines(screen, DARK_GREEN, False, coastline, 3)

class State:
    SETTING_AGENTS = 0
    SETTING_GOAL = 1
    SIMULATING = 2
    Calculating = 3
    PLAYER = 4
    NOT_PLAYER = 5
    ENVIRONMENT = 6
    NOT_ENVIRONMENT = 7

#Simulation Flags
current_state = State.SETTING_AGENTS
current_player = State.NOT_PLAYER
current_env = State.NOT_ENVIRONMENT

# Grid Data
searched = []
obstacles = []
agents = []
current_vessels = []
agents_pos = {}
agent_paths = {}
current_agent_key = []
path_list=[]
goals = set()
agent_colors = {}  # To track different colors for agents
goal_colours = {}
colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
current_color_index = 0
generated = False
collision_risk = False

def reset_simulation():
    global current_state, agents, goals, agent_colors, current_color_index, goal_colours, generated
    global agents_pos, current_agent_key, path_list, current_step, agent_paths, current_player, current_env
    
    current_state = State.SETTING_AGENTS
    current_player = State.NOT_PLAYER
    current_env = State.NOT_ENVIRONMENT
    agents = []
    agents_pos = {}
    agent_paths = {}
    current_agent_key = []
    path_list=[]
    goals = set()
    agent_colors = {}
    goal_colours = {}
    current_color_index = 0
    current_step = 0
    generated = False
    
def future_player_pos():
    """Return predicated future position based upon last recorded key press"""
    global last_key, future_pos

    keys = last_key
    if keys[pygame.K_LEFT] and player_pos[0] > player_size:
        future_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        future_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > player_size:
        future_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - BUTTON_HEIGHT - player_size:
        future_pos[1] += player_speed

    return future_pos

def handle_player_movement():
    global last_key

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player_pos[0] > player_size:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > player_size:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - BUTTON_HEIGHT - player_size:
        player_pos[1] += player_speed

    last_key = keys #record last key press

def main():
    global running, current_step, path_list, current_state, current_color_index, generated, obstacles, collision_risk
    global button_text, agent_paths, agent_colors, searched, player_pos, current_player, player, coastline, current_env

    while running:
        screen.fill(WHITE)
        
        # Handle player movement
        handle_player_movement()
        
        # Event handling:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() 

                #Check if the mouse was clicked on a button
                if button_rect.collidepoint(mouse_pos) and current_state != State.SIMULATING:
                    if current_state == State.SETTING_AGENTS: 
                        current_state = State.Calculating
                        button_text = "Reset"
                        if current_env == State.ENVIRONMENT:
                            draw_environment(coastline)
                        draw_grid()
                        draw_button()
                        draw_player_button()
                        draw_env_button()
                        draw_objects()  
                        draw_text()
                        
                        pygame.display.flip() # update simulator visually
                        # Create paths for all agents
                        for agent_start in agents_pos:
                            print(agent_start)
                            agent = DStarLiteCOLREG(G_WIDTH, G_HEIGHT, agent_start, agents_pos.get(agent_start, (0,0)), grid, obstacles, is_powered=True)
                            agents.append((agent, agent_start))
                        calculate_paths(agents)
                        current_state = State.SIMULATING
                    continue
                elif button_rect.collidepoint(mouse_pos) and current_state == State.SIMULATING:
                    reset_simulation()
                    button_text = "Start Simulation"
                    continue
                elif player_button_rect.collidepoint(mouse_pos):
                    if  current_player == State.PLAYER and player:
                        player = False
                        current_player = State.NOT_PLAYER 
                    else:
                        current_player = State.PLAYER
                        player = True
                elif environment_button.collidepoint(mouse_pos):
                    if current_state == State.SIMULATING:
                        continue
                    if  current_env == State.ENVIRONMENT:
                        current_env = State.NOT_ENVIRONMENT
                        generated = False
                    else:
                        current_env = State.ENVIRONMENT

                grid_pos = mouse_pos

                if grid_pos[1] > HEIGHT - BUTTON_HEIGHT or grid_pos in obstacles: # check if y-coordinate is of the mouse click is greater than max allowed height/in non-grid zone
                    continue # if true, then disregard mouse click

                if current_state == State.SETTING_AGENTS:
                    if grid_pos in agents_pos: # check if potential new agent is already in list - if so, remove agent.
                        del agents_pos[grid_pos]
                        del agent_colors[grid_pos]
                    elif grid_pos not in obstacles and grid_pos not in agents_pos: # if agent doesnt already exist 
                        agents_pos[grid_pos] = [] # attach current grid pos to an empty list
                        agent_colors[grid_pos] = colors[current_color_index % len(colors)] # attach current grid pos to a colour from list
                        current_color_index += 1 # go to next colour
                        current_state = State.SETTING_GOAL # change state to set goal pos for this agent
                        current_agent_key = grid_pos # grid pos associated with agent
                
                elif current_state == State.SETTING_GOAL:
                    if grid_pos in goals: #
                        goals.remove(grid_pos)
                    elif grid_pos not in obstacles and grid_pos not in agents_pos and grid_pos not in goals:
                        agents_pos.update({current_agent_key: grid_pos})
                        goals.add(grid_pos)
                        goal_colours[grid_pos] = colors[(current_color_index % len(colors)) - 1]
                        current_state = State.SETTING_AGENTS
            

         # Generate coastline
        if current_env == State.ENVIRONMENT:
            #generate initial coastline
            if not generated:
                temp_obstacles = []
                obstacles.clear()
                coastline = midpoint_displacement(
                    start=(0, HEIGHT-100),
                    end=(WIDTH, HEIGHT-120),
                    roughness=0.5,
                    vertical_displacement=100,
                    num_of_iterations=8
                )
                for point in coastline:
                    x,y = point
                    obstacles.append(y)
                temp_obstacles = obstacles.copy()
                obstacles.clear()
                obstacles.append(min(temp_obstacles))
                print(obstacles)
                generated = True
            # draw environment    
            draw_environment(coastline)
        
        if path_list != [] and State.SIMULATING:
            reset_counter = False
            screen.fill(WHITE)
            if current_env == State.ENVIRONMENT:
                draw_environment(coastline)
            for path in path_list:
                if path:
                    draw_path(path)
            draw_goal(agent.goal)
            draw_grid()
            draw_button()
            draw_player_button()
            draw_env_button()
            current_step += 1
            current_color_index = 0
            current_vessels.clear()
            collision_risk = False

            if player:
                current_vessels.append((player_pos, future_pos))

            for agent, path in agent_paths.items():
                    try:
                        position = path[current_step]
                        future_position = path[current_step+1]
                        draw_agent(position)
                        current_vessels.append((position,future_position))
                    except IndexError as e: # if path ends, continue running program
                        continue          
            print("--------------------------")
            for agent, path in agent_paths.items():
                    try:
                        position = path[current_step]
                        print("Pos:", position)
                        future_position = path[current_step+1]
                        working_copy = current_vessels.copy()
                        working_copy.remove((position,future_position))
                        agent.update_other_vessels(working_copy)

                        if (agent.collision_risk(position)):
                            print("Collision risk")
                            collision_risk = True
                            agent.apply_colreg_rules(position, future_position)
                            agent.detect_edge_changes(position)
                            path = agent.move_and_replan(position)
                            agent_paths.update({agent: path})
                            path_list.append(path)
                            reset_counter = True
                    except IndexError as e: # if path ends, continue running program
                        continue

            if (reset_counter):
                print("Reset")
                current_step = 0

        draw_grid()
        draw_button()
        draw_player_button()
        draw_env_button()
        draw_objects()
        draw_text()
        draw_player()

        pygame.display.flip()
        clock.tick(60)/1000  # Slow down movement for visibility - higher number is higher tick speed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()