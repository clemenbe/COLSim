"""Kalami Heris, Mostapha (2023). Python Implementation of Path Planning and Obstacle Avoidance using PSO [Computer software]. 
Retrieved from https://github.com/smkalami/path-planning
"""
from calcul_tools import *
from draw import *
from algo_potential_fields import *
from algo_astar import *
from algo_astar2 import *
from algo_aco import *
from algo_dstar_lite import *
from algo_pso import *

import numpy as np
import time


def Jφ0(p):
    """ Jacobian Matrix of φ0 """
    p1, p2 = p.flatten()
    return array([[-3 * p1 ** 2 - p2 ** 2 + 1, -2 * p1 * p2 - 1],
                  [-2 * p1 * p2 + 1, -3 * p2 ** 2 - p2 ** 2 + 1]])

def dφ(x, c, D):
    p1, p2, v, θ = x.flatten()
    z = inv(D) @ array([[p1 - c[0,0]], [p2 - c[1,0]]])
    dv = D @ Jφ0(z) @ inv(D) @ array([[cos(θ)], [sin(θ)]])
    return dv.flatten()


def control(x, φ, c, D, k, r):
    dφ1, dφ2 = dφ(x, c, D)
    x, y, v, θ = x.flatten()
    φ1, φ2 = φ(x, y, c, D, k, r)
    u1 = 0
    u2 = -sawtooth(θ - arctan2(φ2, φ1)) - (φ2 * dφ1 - φ1 * dφ2) / ((φ1 ** 2) + (φ2 ** 2))
    return array([[u1], [u2]])


class SeaObject:
    # x, y are positions, v is speed, theta is direction, algo is the algorithm for path plaaning, destination_distance is the straight distance to the final destination
    def __init__(self, mmsi, x, y, v, theta, algo, destination_distance):
        self.mmsi = mmsi
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        self.algo = algo
        self.destination_distance = destination_distance

        self.phat = array([[self.x + self.destination_distance * cos(self.theta)], [self.y + self.destination_distance * sin(self.theta)]])
        print("Destination for sea_object, mmsi:", self.mmsi, "is at ", self.phat[0][0], ",", self.phat[1][0])
        self.privilege = 0
        self.r = 2 # collision avoidance radius for the object
        self.cross_path = False
        self.final = 0  #0 if the destination is not reached, 1 if the destination is reached (printing purpose)


    # Update the position of an object based on up controller
    def update(self, u, dt):
        x, y, v, theta = self.x, self.y, self.v, self.theta
        self.x += dt * v * cos(theta) 
        self.y += dt * v * sin(theta) 
        self.v = v + dt * u[0][0]
        #ici, on pourrait limiter la vitesse de rot des ships for more realism 
        self.theta += dt * u[1][0]

    # Return the object's x, y, speed and direction in a state vector
    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))
    
    # Move the object straight when there is no risk of collision
    # Called by move()
    def move_straight_apf(self):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[self.x], [self.y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])

        up = array([[0], [10*arctan(tan(0.5*(thetabar_p - self.theta)))]])
        self.update(up, 0.1)
        return up
    
    # Called by move(), when there is risk of collision
    def avoid_collision_apf(self, record_data, obstacle, mmsi_list, rules, table, ax, eps, s, r, k):

        px, py, pv, ptheta = self.get_state_vector().flatten()
        qx, qy, qv, qtheta = obstacle.get_state_vector().flatten()
        
        scalar_pdt = geo_scalar_prod(qv, pv, qtheta, ptheta)

        c = array([[qx],
                [qy]])
        D = array([[r, 0],
                [0, r]])

        # Different cases of collision avoidance
        if dist(array([[qx], [qy]]), array([[px], [py]])) < r + eps:
            if scalar_pdt >= 0:
                #print('------------------Boats with close directions------------------')
                # Tests to find where the boat is compared with the obstacle

                if (px < qx - eps) and self.cross_path:
                    #print('------------------Left Repulsion------------------')
                    φ = φrep
                    rule = 1

                elif (px > qx - eps) and self.cross_path:
                    #print('------------------Right Repulsion------------------')
                    φ = φrep
                    rule = 1

                elif py > qy + eps:
                    # The boat is in the front zone of the obstacle
                    #print('------------------Front zone------------------')
                    φ = φrep
                    rule = 1

                elif (py < qy + eps) and (px < qx):
                    # The boat is in the left lower zone compared with the obstacle
                    #print('------------------Left lower zone------------------')
                    φ = φcw
                    rule = 2

                elif (py < qy + eps) and (px < qx) and (self.phat[0, 1] < qy + eps) and (self.phat[0, 0] > qx):
                    # The boat is in the left lower zone compared with the obstacle
                    #print('------------------Left lower zone --> Destination Right lower zone------------------')
                    φ = φccw
                    self.cross_path = True
                    rule = 4

                elif (py < qy + eps) and (px > qx) and (self.phat[1] < qy + eps) and (self.phat[0] < qx):
                    # The boat is in the right lower zone compared with the obstacle
                    #print('------------------Right lower zone-> Destination Left lower zone------------------')
                    φ = φcw
                    self.cross_path = True
                    rule = 3

                else:
                    # The boat is in the right lower zone compared with the obstacle
                    #print('------------------Right lower zone------------------')
                    φ = φccw
                    rule = 3

                up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                #print('up = ',up)
                # We display the simulation if record_data=False
                if not record_data:
                    # Reinitialize the situation in the table
                    for row in arange(len(rules)):
                        table[row, mmsi_list.index(self.mmsi) + 1].set_facecolor('white')
                    # Put in green the current applied rule in the table
                    table[rule, mmsi_list.index(self.mmsi) + 1].set_facecolor('green')
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.9, c, D, k, r)

            else:
                #print('------------------Boats in opposite directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if (py > qy - eps):
                    # The boat is in the front zone of the obstacle
                    #print('------------------Left front zone------------------')
                    φ = φccw
                    rule = 4
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    #print('up = ', up)

                elif (py > qy - eps) and (px > qx) and (scalar_pdt < abs(qv * pv) * cos(2.5)):
                    # The boat is in the front zone of the obstacle
                    #print('------------------Right front zone (align)------------------')
                    up = array([[0], [0]])
                    rule = 4

                elif py > qy - eps and px > qx and scalar_pdt > abs(qv * pv) * cos(2.5):
                    # The boat is in the front zone of the obstacle
                    #print('------------------Right front zone------------------')
                    φ = φccw
                    rule = 4
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    #print('up = ', up)

                else:
                    # The boat is in the right lower zone compared with the obstacle
                    #print('------------------Lower zone------------------')
                    φ = φrep
                    rule = 1
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    #print('up = ', up)


        #print('cross_path =', self.cross_path)

        # We display the simulation if record_data=False
        if not record_data:
            # Reinitialize the situation in the table
            for row in arange(len(rules)):
                table[row, mmsi_list.index(self.mmsi) + 1].set_facecolor('white')
            # Put in green the current applied rule in the table
            table[rule, mmsi_list.index(self.mmsi) + 1].set_facecolor('green')
            draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.9, c, D, k, r)
        return up

   
    # Moves the object every iteration
    def move_apf(self, record_data, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt):
        in_collision = False

        # Check risks of collision with every other object
        for other_object in sea_objects:

            if self != other_object:
                # When distance is smaller than collision radius
                if dist(array([[other_object.x], [other_object.y]]), array([[self.x], [self.y]])) < max(self.r, other_object.r) + eps:
                    # Object with smaller privilege avoids collision
                    if self.privilege <= other_object.privilege:
                        up = self.avoid_collision_apf(record_data, other_object, mmsi_list, rules, table, ax, eps, s, max(self.r, other_object.r), k)
                        in_collision = True

        # If there is no need to avoid collision
        if not in_collision:
            up = self.move_straight_apf()

        #sea_object stops if goal is reached
        if sqrt((self.phat[0]-self.x)**2 + (self.phat[1]-self.y)**2)<1:
            up=array([[0], [0]])
            if self.final==0:
                self.final=1
                print("Destination reached for 1 sea_object, mmsi:", self.mmsi, "at final time", time.time())
        else :
            # Update position
            self.update(up, dt)
        return [self.mmsi, self.x,self.y,self.v,self.theta]
    

    def create_grid(self, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt,grid):
        """
        Create a grid with 0 (available) and 1 (non available) cases.
        Returns: the grid, the start and the end points.
        """
        grid_w,grid_h=len(grid[0]),len(grid)

        for row in range(grid_w):
            for col in range(grid_h):
                for other_object in sea_objects:
                    if self != other_object:
                        xx=(grid_w-row)*(s+s)/grid_w-s
                        yy=col*(s+s)/grid_h-s
                        # When distance is smaller than collision radius
                        if dist(array([[other_object.x], [other_object.y]]), array([[xx], [yy]])) < self.r + eps:
                            grid[row][col]=1
        
        start=(int(-(round(self.x)+s)*grid_w/(s+s)+grid_w), int((round(self.y)+s)*grid_h/(s+s)))
        end=(int(-(round(self.phat[0][0])+s)*grid_w/(s+s)+grid_w), int((round(self.phat[1][0])+s)*grid_h/(s+s)))
        
        # Set show to True and see one path with self.num_steps = 1
        show=False
        if show:
            print("start (3) is at",start)
            print("end (4) is at", end)
            grid[start[0],start[1]]='3'
            grid[end[0],end[1]]='4'
            print(grid)
            grid[start[0],start[1]]='0'
            grid[end[0],end[1]]='0'
            
        return grid,start,end

    def go_to(self,path,s,grid):
        grid_w, grid_h = len(grid[0]), len(grid)
        next_point = (grid_w-path[1][0])*(s+s)/grid_w-s , path[1][1]*(s+s)/grid_h-s
        # print(next_point)
        thetabar = arctan2(next_point[1]-self.y , next_point[0]-self.x)
        # print("theta des ", thetabar, "et theta ", self.theta)
        error = 2* arctan(tan(thetabar-self.theta)/2)
        #print("error", error)
        if error> np.pi/4: u2=1
        if error< -np.pi/4: u2=-1
        else : u2=0.5 * error

        up=array([[0], [u2]])
        # print("upp :", up)
        return up

    def create_graph(self,map):
        w=len(map[0])
        graph = GridWithWeights(w,w)
        for row in range(w):
            for col in range(w):
                if map[row][col]==1:
                    graph.walls.append((row,col))
        return graph
            
    def move_astar(self, record_data, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt):
        '''
        start=(round(self.x),round(self.y))
        end=(round(self.phat[0][0]),round(self.phat[1][0]))
        print("start in coord ",start)
        print("end in coord", end)
          '''   
        step=2
        empty_grid=np.zeros((int(2*s/step),int(2*s/step)))  #with a square grid as shown
        #t0=time.time()
        map0,start,end=self.create_grid(sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt,empty_grid)
        # with algo A*1
        path = astar(map0, start, end,True)
        #tf=time.time()-t0
        
        # Uncomment and see one path with self.num_steps = 1
        # print_maze(path,map0,start, end)
        """
        t0=time.time()
        # with algo A*2     but doesn't work well
        map=self.create_graph(map0)
        came_from, cost_so_far = a_star_search(map, start, end)
        # Uncomment and see one grid and a path with self.num_steps = 1
        # draw_grid(map, point_to=came_from, start=start, goal=end)
        # draw_grid(map, path=reconstruct_path(came_from, start=start, goal=end))
        path=reconstruct_path(came_from, start=start, goal=end)
        tf=time.time()-t0
        #print("tempss", tf)
        """

        #print("debug", path[0], path[-1])
        #print("path is ", path)
        if path==None:
            up=array([[0], [0]])
            self.update(up, dt)
            return [self.mmsi, self.x,self.y,self.v,self.theta]

        if path[0]==path[-1]:
            up=array([[0], [0]])
            if self.final==0:
                self.final=1
                print("Destination reached for 1 sea_object, mmsi:", self.mmsi, "at final time", time.time())
        else :
            up=self.go_to(path,s,map0)
            # Update position
            self.update(up, dt)
        
        return [self.mmsi, self.x,self.y,self.v,self.theta]

    
    def move_aco(self, record_data, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt):
        step=2
        grid_w,grid_h=int(2*s/step),int(2*s/step)
        Obstacles = []
        for row in range(grid_w):
            for col in range(grid_h):
                for other_object in sea_objects:
                    if self != other_object:
                        xx=(grid_w-row)*(s+s)/grid_w-s
                        yy=col*(s+s)/grid_h-s
                        # When distance is smaller than collision radius
                        if dist(array([[other_object.x], [other_object.y]]), array([[xx], [yy]])) < self.r + eps:
                            Obstacles.append((row,col))
        
        start=(int(-(round(self.x)+s)*grid_w/(s+s)+grid_w), int((round(self.y)+s)*grid_h/(s+s)))
        end=(int(-(round(self.phat[0][0])+s)*grid_w/(s+s)+grid_w), int((round(self.phat[1][0])+s)*grid_h/(s+s)))
        
        # width, height, obstacles, ant_count, step_count, alpha, beta, gamma, evaporation_rate, start, end, brushfire_iter, colony_iter):
        aco_pdg = ACO_PDG(grid_w, grid_h, Obstacles, 10, 50, 1, 10, 0.01, 0.5, start, end, 3, 10)
        heuristic_grid = aco_pdg.heuristic_grid
        #plt.figure("Heuristic grid")
        #plt.imshow(heuristic_grid)
        #plt.show()
        path1 = aco_pdg.move_ant()
        #print("path1", path1)
        #aco_pdg.plot(path1)
        path2 = aco_pdg.geometric_path_optimizer(path1)
        #aco_pdg.plot(path2)
        #print("path2", path2)
        o = aco_pdg.run_ant_colony_noshow(10)  #path sorted by length
        #aco_pdg.plot(o[0][1])
        path=o[0][1]
        #print("path is ", path)


        if path[0]==path[-1]:
            up=array([[0], [0]])
            if self.final==0:
                self.final=1
                print("Destination reached for 1 sea_object, mmsi:", self.mmsi, "at final time", time.time())
        else :
            next_point = (grid_w-path[1][0])*(s+s)/grid_w-s , path[1][1]*(s+s)/grid_h-s
            thetabar = arctan2(next_point[1]-self.y , next_point[0]-self.x)
            error = 2* arctan(tan(thetabar-self.theta)/2)
            if error> np.pi/4: u2=1
            if error< -np.pi/4: u2=-1
            else : u2=0.5 * error

            up=array([[0], [u2]])
                # Update position
            self.update(up, dt)
        
        return [self.mmsi, self.x,self.y,self.v,self.theta]

    

    def init_dstarlite(self, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt,grid):
        """
        Returns: lists of obstacles, the start and the end points.
        """
        grid_w,grid_h=len(grid[0]),len(grid)
        ox,oy = [],[]
        s=s*2       #ici le pb est que en fonction du pas, le max de la grille est plus grand que le max des coordonnées et donc 
                    #on ne peut pas avoir les coordonnées des obstacles dans la grille pour les exterieurs
                    #max * pas - min ?? pour delimitation ++?
        for i in range(-s,s+1):
            ox.append(i)
            oy.append(s)
            ox.append(s)
            oy.append(i)
            ox.append(i)
            oy.append(-s)
            ox.append(-s)
            oy.append(i)
        
        for row in range(grid_w):
            for col in range(grid_h):
                for other_object in sea_objects:
                    if self != other_object:
                        xx=(grid_w-row)*(s+s)/grid_w-s
                        yy=col*(s+s)/grid_h-s
                        # When distance is smaller than collision radius
                        if dist(array([[other_object.x], [other_object.y]]), array([[xx], [yy]])) < self.r + eps:
                            grid[row][col]=1
                            ox.append(row)
                            oy.append(col)
        
        start=(int(-(round(self.x)+s)*grid_w/(s+s)+grid_w), int((round(self.y)+s)*grid_h/(s+s)))
        end=(int(-(round(self.phat[0][0])+s)*grid_w/(s+s)+grid_w), int((round(self.phat[1][0])+s)*grid_h/(s+s)))
        #print("start in coord ",start)
        #print("end in coord", end)

        return grid,ox,oy,start,end

    def move_dstarl(self, record_data, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt):
        step=2
        empty_grid=np.zeros((int(2*s/step),int(2*s/step)))  #with a square grid as shown
        
        map0,ox,oy,start,end=self.init_dstarlite(sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt,empty_grid)
        
        # Lists of obstacles
        dstarlite = DStarLite(ox,oy)
        #print(Node(x=end[0], y=end[1]))
        path=dstarlite.dstarl(Node(x=start[0], y=start[1]), Node(x=end[0], y=end[1]))
        
        if path[1]==path[-1]:
            up=array([[0], [0]])
            if self.final==0:
                self.final=1
                print("Destination reached for 1 sea_object, mmsi:", self.mmsi, "at final time", time.time())
        else :
            up=self.go_to(path,s,map0)
            # Update position
            self.update(up, dt)
        
        return [self.mmsi, self.x,self.y,self.v,self.theta]
    

    def move_pso(self, record_data, sea_objects, mmsi_list, rules, table, ax, eps, s, k, dt):
        # Define start, goal, and limits
        start = (self.x,self.y)
        goal = (self.phat[0][0],self.phat[1][0])
        limits = [-s, s, -s, s]
        layout = PathPlanning(start, goal, limits)

        for other_object in sea_objects:
            if self != other_object:
                layout.add_circle(x=other_object.x, y=other_object.y, r=other_object.r + eps, Kv=100)
        
        nRun = 2            #between 1 and 15 for figure
        nPts = 3            # Number of points along the path (excluding the start and goal points).
        d = 30              # ns = 301 (points along the spline)
        nPop = 50           # Number of particles (agents) (one for each path).
        epochs = 50        # Number of iterations.
        f_interp = 'linear'
        Xinit = None

        np.random.seed(1294404794)
        np.seterr(all='ignore')
        ns = 1 + (nPts + 1) * d         # Number of points along the spline
        best_L = np.inf                 # Best length (minimum)
        best_run = 0                    # Run corresponding to the best length
        best_count = 0                  # count corresponding to the best length
        paths = [None] * nRun           # List with the results from all runs

        for run in range(nRun):
            # Optimize (the other PSO parameters have always their default values)
            layout.optimize(nPts=nPts, ns=ns, nPop=nPop, epochs=epochs,
                            f_interp=f_interp, Xinit=Xinit)

            # Save run
            paths[run] = deepcopy(layout)

            # Print results
            L = layout.sol[1]               # Length
            count = layout.sol[2]           # Number of violated obstacles
            # print("\nrun={0:d}, L={1:.2f}, count={2:d}".format(run+1, L, count), end='', flush=True)

        # Save if best result (regardless the violations)
        if (L < best_L):
            best_L = L
            best_run = run
            best_count = count

        # print("\nBest:", end='')
        # print(" run={0:d}, L={1:.2f}, count={2:d}".format(best_run+1, best_L, best_count))

        show=False   #run simu with if num_steps=1
        if show:
            fig, axs = plt.subplots(3, 5)
            axs = axs.flatten()
            for run in range(nRun):

                layout = paths[run]         # Layout to plot
                ax = axs[run]               # Subplot

                L = layout.sol[1]           # Length
                count = layout.sol[2]       # Number of violated obstacles

                # Text position on the plots (lower left corner)
                xt = layout.limits[0] + 0.05 * (layout.limits[1] - layout.limits[0])
                yt = layout.limits[2] + 0.05 * (layout.limits[3] - layout.limits[2])

                layout.plot_obs(ax)         # Plot obstacles
                layout.plot_path(ax)        # Plot path

                # Plot run, length, and count
                title = "run=" + str(run+1) + ", L=" + str("{:.2f}".format(L)) + \
                        ", count=" + str(count)
                ax.text(xt, yt, title, fontsize=10)

            fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
            plt.show()

        path=[]
        for i in range(len(paths[best_run].sol[3][0])):
            path.append([paths[best_run].sol[3][0][i],paths[best_run].sol[4][0][i]])
        # print("the path is",path)

        if sqrt((self.phat[0]-self.x)**2 + (self.phat[1]-self.y)**2)<1:
            up=array([[0], [0]])
            if self.final==0:
                self.final=1
                print("Destination reached for 1 sea_object, mmsi:", self.mmsi, "at final time", time.time())
        
        else :
            next_point = (path[1][0],path[1][1])
            thetabar = arctan2(next_point[1]-self.y , next_point[0]-self.x)
            error = 2* arctan(tan(thetabar-self.theta)/2)
            if error> np.pi/4: u2=1
            if error< -np.pi/4: u2=-1
            else : u2= 0.5 *error

            up=array([[0], [u2]])

            # Update position
            self.update(up, dt)      

        return [self.mmsi, self.x,self.y,self.v,self.theta]

