import numpy as np
import plotly.graph_objects as go
import datetime


class Representation:
    def __init__(self, radius=0.1, num_circle_points=20):
        self.radius = radius
        self.num_circle_points = num_circle_points
        self.tube_x = []
        self.tube_y = []
        self.tube_z = []
        self.faces = []
        self.trace = None
        self.trace_traj1 = None
        self.trace_traj2 = None
        self.trace_proj1 = None
        self.trace_proj2 = None

    def draw_tube(self, x, y, z):
        # Initialize arrays to store the tube coordinates
        tube_x = []
        tube_y = []
        tube_z = []

        # Generate the tube coordinates
        for i in range(len(x)):
            # Define the angle for the circle
            theta = np.linspace(0, 2 * np.pi, self.num_circle_points)

            # Circle in the xy-plane
            circle_x = self.radius * np.cos(theta)
            circle_y = self.radius * np.sin(theta)

            # Compute the circle in 3D by adding the circle coordinates to the current point (x, y, z)
            for j in range(self.num_circle_points):
                point_x = x[i] + circle_x[j]
                point_y = y[i] + circle_y[j]
                point_z = z[i]

                tube_x.append(point_x)
                tube_y.append(point_y)
                tube_z.append(point_z)

        return tube_x, tube_y, tube_z

    def draw_all(self, x1, y1, z1, x2, y2, z2):
        # Draw the first trajectory
        tube_x1, tube_y1, tube_z1 = self.draw_tube(x1, y1, z1)

        # Draw the second trajectory
        tube_x2, tube_y2, tube_z2 = self.draw_tube(x2, y2, z2)

        # Combine the coordinates for both trajectories
        self.tube_x = tube_x1 + tube_x2
        self.tube_y = tube_y1 + tube_y2
        self.tube_z = tube_z1 + tube_z2

        # Generate the mesh faces
        self.faces = []
        num_points_traj1 = len(tube_x1)
        num_points_traj2 = len(tube_x2)
        for i in range(len(x1) - 1):
            for j in range(self.num_circle_points):
                next_j = (j + 1) % self.num_circle_points
                self.faces.append([i * self.num_circle_points + j, (i + 1) *
                                  self.num_circle_points + j, (i + 1) * self.num_circle_points + next_j])
                self.faces.append([i * self.num_circle_points + j, (i + 1) *
                                  self.num_circle_points + next_j, i * self.num_circle_points + next_j])

        for i in range(len(x2) - 1):
            for j in range(self.num_circle_points):
                next_j = (j + 1) % self.num_circle_points
                self.faces.append([num_points_traj1 + i * self.num_circle_points + j, num_points_traj1 + (
                    i + 1) * self.num_circle_points + j, num_points_traj1 + (i + 1) * self.num_circle_points + next_j])
                self.faces.append([num_points_traj1 + i * self.num_circle_points + j, num_points_traj1 + (
                    i + 1) * self.num_circle_points + next_j, num_points_traj1 + i * self.num_circle_points + next_j])

        # Flatten the face list
        i, j, k = np.array(self.faces).T

        # Create the mesh trace
        self.trace = go.Mesh3d(x=self.tube_x, y=self.tube_y, z=self.tube_z,
                               i=i, j=j, k=k, opacity=0.5, color='lightblue')

        # Add the original trajectories for reference
        self.trace_traj1 = go.Scatter3d(
            x=x1, y=y1, z=z1, mode='lines', line=dict(color='red', width=3))
        self.trace_traj2 = go.Scatter3d(
            x=x2, y=y2, z=z2, mode='lines', line=dict(color='green', width=3))

        # Add the projection of the two trajectories on the plane XY
        self.trace_proj1 = go.Scatter3d(x=x1, y=y1, z=np.zeros_like(
            z1), mode='lines', line=dict(color='red', dash='dash'))
        self.trace_proj2 = go.Scatter3d(x=x2, y=y2, z=np.zeros_like(
            z2), mode='lines', line=dict(color='green', dash='dash'))

    def show(self):
        # Create the plot
        fig = go.Figure(data=[self.trace, self.trace_traj1,
                        self.trace_traj2, self.trace_proj1, self.trace_proj2])
        fig.show()

    def record(self, filename):
        # Create the plot
        fig = go.Figure(data=[self.trace, self.trace_traj1,
                        self.trace_traj2, self.trace_proj1, self.trace_proj2])
        fig.write_html(filename)


# Define the trajectories
# Define the trajectories
t = np.linspace(0, 1, 100)
x1 = t
y1 = t**2
z1 = t
x2 = np.cos(t)
y2 = np.sin(t)
z2 = t

rep = Representation()
rep.num_circle_points = 20
rep.draw_all(x1, y1, z1, x2, y2, z2)
rep.show()
rep.record("test/save_3D/" +
           datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".html")
