import heapq
import math
import pygame as pg
from generate_grid import *

class COLREGRules():
    """States for COLREG rule types"""
    HEAD_ON = 1
    CROSSING_PORT = 2
    CROSSING_STARBOARD = 3
    OVERTAKING = 4

class DStarLiteCOLREG(pg.sprite.Sprite):
    def __init__(self, width, height, start, goal, grid, obstacles, is_powered=True):
        pg.sprite.Sprite.__init__(self)
        self.current_pos = start
        self.width = width # width of grid
        self.height = height # height of grid
        self.grid = grid # a list of all the possible grid coordinates
        self.costs = {} # a dictionary of all the costs between nodes, a cache to reduce lookup time
        self.heap_size = 100 # a max size for the priority queue
        self.start = start  # (x, y)
        self.goal = goal  # (x, y)
        self.U = []  # Priority queue
        self.km = 0  # Key modifier
        self.g = {}  # g-values
        self.rhs = {}  # rhs-values
        self.last_start = start 
        self.is_powered = is_powered  # True for powered vessel, False for sailboat
        self.other_vessels = []  # List of other vessels (position, course)
        self.safety_radius = 100  # Minimum safe distance from other vessels
        self.counter = 0
        self.changed_edges = []
        self.path = []
        if obstacles:
            self.obstacles = obstacles
        else:
            self.obstacles = [height]
        self.initialize()

    def initialize(self):
        """Initialize D* Lite."""
        self.U = []
        self.km = 0
        for (x,y) in self.grid:
            self.g.update({(x,y): float('inf')})
            self.rhs.update({(x,y): float('inf')})
        if self.goal not in self.grid or self.start not in self.grid:
            raise IndexError("Start/Goal not in domain")
        self.rhs[self.goal] = 0 
        heapq.heappush(self.U, (self.calculate_key(self.goal), self.goal))

    def remove_node(self, n):
        self.U = [(k, node) for (k, node) in self.U if node != n]
        heapq.heapify(self.U)

    def calculate_key(self, s):
        """Calculate the priority key."""
        k1 = min(self.g[s], self.rhs[s]) + self.heuristic(s, self.start) + self.km
        k2 = min(self.g[s], self.rhs[s])
        return (k1, k2)

    def heuristic(self, s1, s2):
        """Euclidean distance heuristic."""
        return ((s1[0] - s2[0])**2 + (s1[1] - s2[1])**2)
    
    def check_size(self, list):
        top_min = heapq.nsmallest(self.heap_size, list)
        list = top_min
        return list
    
    def get_neighbors(self, u): # get nodes connected to u if they are within the grid width and height
        """Return a list of nodes connected to provided node and are within the grid constraints """
        x, y = u

        return [(x+dx, y+dy) 
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,1),(1,-1),(-1,-1)]
                if 0 <= x+dx < self.width 
                and 0 <= y+dy < self.height
                and y+dy < min(self.obstacles)] 

    def calculate_cost(self, u, v):
        """Cost between adjacent nodes with COLREG considerations."""
        # if (u, v) in self.costs.keys():
        #     print("Cost found")
        #     return self.costs.get((u,v))

        dx = abs(u[0] - v[0])
        dy = abs(u[1] - v[1])
        
        if dx + dy == 1:  # Adajcent
            cost = 1.0 
        elif dx == 1 and dy == 1:  # Diagonal
            cost = math.sqrt(2)
        else:  # Not neighbors
            cost = float('inf')
        
        # Apply COLREG-based cost adjustments
        if cost < float('inf'):
            # Check for nearby vessels and apply COLREG rules
            colreg_cost = self.apply_colreg_rules(u, v)
            cost += colreg_cost
            
            # Add cost for proximity to other vessels
            for vessel in self.other_vessels:
                vessel_pos, _ = vessel
                dist = math.sqrt(self.heuristic(v, vessel_pos))
                if dist < self.safety_radius:
                    cost += (self.safety_radius - dist) * 10  # Exponential cost as distance decreases
        
        # self.costs.update({(u, v): cost}) 
        # print("Cost for point:", (u,v), cost)
        return cost
    
    def collision_risk(self, current_pos):

        for vessel in self.other_vessels:
            vessel_pos, _ = vessel
            dist = math.sqrt(self.heuristic(current_pos, vessel_pos))
            print("Distance:", dist)
            
        
            if dist and dist < self.safety_radius:
                return True
            else:
                return False
        
    def apply_colreg_rules(self, current_pos, next_pos):
        """
        Apply COLREG rules to modify path costs based on other vessels.
        Returns additional cost to add based on COLREG compliance.
        """
        additional_cost = 0
        my_course = self.calculate_course(current_pos, next_pos)
        
        for vessel in self.other_vessels:
            vessel_pos, vessel_course = vessel

            dist = math.sqrt(self.heuristic(current_pos, vessel_pos))
  
            # Determine relative bearing and COLREG situation
            rel_bearing = self.relative_bearing(my_course, current_pos, vessel_pos)
            # print("REL BEARING:", rel_bearing)
            situation = self.determine_colreg_situation(rel_bearing)
            print("COLREG Situation:", situation)
            
            # Apply COLREG-based cost adjustments
            if situation == COLREGRules.HEAD_ON:
                # Rule 14: Both vessels should alter course to starboard
                preferred_dir = self.get_starboard_turn_dir(current_pos, next_pos)
                self.changed_edges.append((preferred_dir, next_pos))
                if preferred_dir != next_pos:
                    additional_cost += 50  # Penalize not turning starboard
                    
            elif situation == COLREGRules.CROSSING_PORT:
                # Rule 15: We are give-way vessel (crossing from port)
                # Should alter course to starboard or slow down
                preferred_dir = self.get_starboard_turn_dir(current_pos, next_pos)
                self.changed_edges.append((preferred_dir, next_pos))
                if preferred_dir != next_pos:
                    additional_cost += 80  # Strong penalty for not giving way
                    
            elif situation == COLREGRules.CROSSING_STARBOARD:
                # Rule 15: We are stand-on vessel (crossing from starboard)
                # Maintain course but be cautious

                if dist < 100:
                    additional_cost += 2  # Small penalty for risky proximity
                    
            elif situation == COLREGRules.OVERTAKING:
                # Rule 13: Overtaking vessel must keep clear
                if self.is_overtaking(current_pos, next_pos, vessel_pos, vessel_course):
                    preferred_dir = self.get_away_turn_dir(current_pos, next_pos, vessel_pos)
                    self.changed_edges.append((preferred_dir, next_pos))
                    if preferred_dir != next_pos:
                        additional_cost += 6  # Penalize not keeping clear
        
        return additional_cost

    def calculate_course(self, from_pos, to_pos):
        """Calculate course angle (in degrees) from one position to another - this follows traditional quadrant rules"""
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        return math.degrees(math.atan2(dy, dx)) % 360

    def relative_bearing(self, my_course, my_pos, other_pos):
        """
        Calculate relative bearing of other vessel from our perspective.
        Returns angle in degrees (0 = dead ahead, +ve to starboard, -ve to port)
        """
        absolute_bearing = self.calculate_course(my_pos, other_pos)
        relative = (absolute_bearing - my_course) % 360
        if relative > 180:
            relative -= 360
        return relative

    def determine_colreg_situation(self, rel_bearing):
        """
        Determine which COLREG rule applies to the situation.
        """
        # Head-on situation (Rule 14)
        if abs(rel_bearing) < 5:
            return COLREGRules.HEAD_ON
            
        # Crossing situation (Rule 15)
        if -112.5 <= rel_bearing <= -5:  # Other vessel on port side
            return COLREGRules.CROSSING_PORT
        elif 5 <= rel_bearing <= 112.5:  # Other vessel on starboard side
            return COLREGRules.CROSSING_STARBOARD
            
        # Overtaking situation (Rule 13)
        if abs(rel_bearing) > 112.5:
            return COLREGRules.OVERTAKING
            
        return None

    def get_starboard_turn_dir(self, current_pos, next_pos):
        """Determine which direction is a starboard turn from current course"""
        # Current course vector
        current_course = (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
        
        # Starboard turn is 90 degrees clockwise
        starboard_dir = (-current_course[1], current_course[0])  # Rotate 90 degrees
        
        # Find the grid cell that best matches this direction
        best_dir = None
        best_dot = -float('inf')
        for neighbor in self.get_neighbors(current_pos):
            dir_vec = (neighbor[0] - current_pos[0], neighbor[1] - current_pos[1])
            dot = starboard_dir[0]*dir_vec[0] + starboard_dir[1]*dir_vec[1]
            if dot > best_dot:
                best_dot = dot
                best_dir = neighbor
                
        return best_dir if best_dir is not None else next_pos

    def get_away_turn_dir(self, current_pos, next_pos, vessel_pos):
        """Determine direction to turn away from another vessel"""
        # Vector from us to the other vessel
        to_vessel = (vessel_pos[0] - current_pos[0], vessel_pos[1] - current_pos[1])
        
        # Best direction is opposite of this
        away_dir = (-to_vessel[0], -to_vessel[1])
        
        # Find the grid cell that best matches this direction
        best_dir = None
        best_dot = -float('inf')
        for neighbor in self.get_neighbors(current_pos):
            dir_vec = (neighbor[0] - current_pos[0], neighbor[1] - current_pos[1])
            dot = away_dir[0]*dir_vec[0] + away_dir[1]*dir_vec[1]
            if dot > best_dot:
                best_dot = dot
                best_dir = neighbor
                
        return best_dir if best_dir is not None else next_pos

    def is_overtaking(self, my_pos, my_next_pos, vessel_pos, vessel_course):
        """Determine if we are overtaking another vessel"""
        # Calculate if we're approaching from more than 22.5 degrees abaft the beam
        rel_bearing = self.relative_bearing(
            self.calculate_course(my_pos, my_next_pos), 
            my_pos, 
            vessel_pos
        )
        return abs(rel_bearing) > 112.5

    def update_other_vessels(self, vessels):
        """Update information about other vessels in the area"""
        new_vessels = []

        for vessel in vessels:
            current_pos, future_pos = vessel
            course = self.calculate_course(current_pos,future_pos)
            new_vessels.append((current_pos, course))
    
        self.other_vessels.clear()
        self.other_vessels = new_vessels

        
        # Invalidate affected parts of the cost map
        for vessel in new_vessels:
            vessel_pos, _= vessel
            for neighbor in self.get_neighbors(vessel_pos):
                u,v = neighbor
                # print("vessel pos", vessel_pos)
                # print("Neigh", neighbor)
                # if (u, v) in self.costs.keys():
                #     self.costs.
                self.costs.update({(u, v): float('inf')})
                # del self.costs[(neighbor, vessel_pos)]
                # else:
                #     self.costs.update({(u, v): float('inf')})
                # if (vessel_pos, neighbor) in self.costs:
                #     del self.costs[(vessel_pos, neighbor)]

    def update_vertex(self, u):
        """Update vertex `u` in the priority queue."""
        if (self.g.get(u, float('inf')) != self.rhs.get(u, float('inf'))):
            if self.U != []:
                temp = []
                for (_, node) in self.U:
                    temp.append(node) # list of the current nodes in the queue
                if u in temp: # check if u is in list of current nodes
                    self.remove_node(u)
                    heapq.heappush(self.U, (self.calculate_key(u), u))
                else:
                    heapq.heappush(self.U, (self.calculate_key(u), u))
            else:
                heapq.heappush(self.U, (self.calculate_key(u), u))
        else:
            for (k, node) in self.U:
                if node == u:
                    self.remove_node(u)

    def compute_shortest_path(self):
        """Compute the shortest path using D* Lite."""
        while self.U and (self.U[0][0] < self.calculate_key(self.start) or self.rhs[self.start] > self.g[self.start]):
            if (len(self.U) > 100):
                self.U = self.check_size(self.U) # check the size of the queue and shorten if its greater than max allowed size
            self.counter += 1
            k_old, u = heapq.heappop(self.U) # pull out key and node u from the top of the priority queue
            k_new = self.calculate_key(u) # recalculate key for node u

            if k_old < k_new: # if the current key is less than the newly calculated key; remove the node
                heapq.heappush(self.U, (k_new, u))

            elif self.g[u] > self.rhs[u]: # if the look ahead cost is less than the known cost
                self.g[u] = self.rhs[u] # set the known cost to the look ahead cost
                for s in self.get_neighbors(u):
                    if s != self.goal:
                        new_rhs = self.calculate_cost(s,u) + self.g[u]
                        self.rhs[s] = min(self.rhs[s], new_rhs)
                    self.update_vertex(s)
            else:
                g_old = self.g[u]
                self.g[u] = float('inf')
                for v in self.get_neighbors(u) + [u]:
                    if self.rhs[v] == (self.calculate_cost(v, u) + g_old):
                        if s != self.goal:
                            self.rhs[v] = min(self.calculate_cost(v, s) + self.g[s] 
                                        for s in self.get_neighbors(v))
                    self.update_vertex(v)

    def move_and_replan(self,start):
        """Move the robot and replan if edge costs change."""
        self.path = []
        if start:
            self.start = start
        self.last_start = self.start
        self.compute_shortest_path()
        while self.start != self.goal:
            if len(self.U) == 0 and self.g[self.start] == float('inf'):
                print("No path exists!")
                return []
            self.start = min(
                self.get_neighbors(self.start),
                key=lambda n: self.g.get(n, float('inf')), default=self.start)
            self.path.append(self.start)
        self.path = self.path + [self.goal]
        return self.path
    
    def detect_edge_changes(self, current_pos):
        """Simulate detecting edge cost changes (e.g., new obstacles)."""
        self.changed_edges.clear()
        self.km += math.sqrt(self.heuristic(self.last_start, self.start))
        self.last_start = self.start
        for neighbour in self.get_neighbors(current_pos):
            self.changed_edges.append((current_pos,neighbour))
        for (u, v) in self.changed_edges:
            print((u,v))
            old_cost = self.costs.get((u,v), float('inf'))
            new_cost = self.calculate_cost(u,v)
            print("Node and cost:", u, v, new_cost)
            if old_cost > new_cost:
                if u != self.goal:
                    self.rhs[u] = min(self.rhs.get(u,float('inf')), new_cost + self.g.get(v, float('inf')))
            elif self.rhs.get(u,float('inf')) == old_cost + self.g.get(v, float('inf')):
                if u != self.goal:
                    temp_val = []
                    for x in self.get_neighbors(u):
                        temp_val.append(self.calculate_cost(u,x) + self.g.get(x, float('inf')))
                    temp_min = min(temp_val)
                    self.rhs.update({u:temp_min})
            self.update_vertex(u)
        self.compute_shortest_path()



