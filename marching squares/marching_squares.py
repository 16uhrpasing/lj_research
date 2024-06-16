import numpy as np
from noise import pnoise3
import matplotlib.pyplot as plt
from itertools import product, combinations

# Function to create a grid of spheres inside the cube
def create_sphere_grid(grid_size, sphere_count, color_min=0, color_max=1):
    #equal subdivisions for each axis
    x = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    y = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    z = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    xv, yv, zv = np.meshgrid(x, y, z) #3 lists, x-, y-, z-coordinates for all points, subarray-ed per axis
    colors = np.linspace(color_min, color_max, sphere_count**3).reshape((sphere_count, sphere_count, sphere_count))
    return xv.flatten(), yv.flatten(), zv.flatten(), colors.flatten()

# Function to draw the wireframe cube
def draw_cube(ax, size):
    r = [-size / 2, size / 2] # e.g. size 50: -25 <-> 25
    cartesian = list(product(r, r, r)) #liste der kartesischen produkte erzeugen
    arr = np.array(cartesian) #als numpy array
    comb = combinations(arr, 2) #alle möglichen 2er paare (reihenfolge egal)
    for s, e in comb:
        if np.sum(np.abs(s-e)) == r[1]-r[0]: #abstand zwischen 2er paaren = size? -> seite
            ax.plot3D(*zip(s, e), color="black")

# Main function to set up the plot
def main():
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    size = 50

    # Drawing the cube
    draw_cube(ax, size)

    # Create linspaces
    x = np.linspace(0, 5, 5)  # 5 points from 0 to 1
    y = np.linspace(0, 5, 5)  # 5 points from 0 to 1

    # Generate 3D meshgrid
    X, Y = np.meshgrid(x, y)

    # Creating a grid of spheres
    sphere_count = 10
    xs, ys, zs, colors = create_sphere_grid(size, sphere_count)

    # Plotting the spheres
    sphere_size = 5  # Adjust if needed
    colors_normalized = (colors - colors.min()) / (colors.max() - colors.min())
    scatter = ax.scatter(xs, ys, zs, c=colors_normalized, cmap='gray', s=sphere_size)

    # Setting aspect to be equal
    ax.set_box_aspect([1,1,1])

    plt.show()

# Run the main function
if __name__ == "__main__":
    main()