import numpy as np
from noise import pnoise3
import matplotlib.pyplot as plt
from itertools import product, combinations

def create_noise_array(size):
    noise_array = np.zeros((size, size, size)) #dimensions
    scale = 5 #"Zoom" der Perlin Noise

    # Generate the noise
    for x in range(size):
        for y in range(size):
            for z in range(size):
                nx = x / scale
                ny = y / scale
                nz = z / scale
                noise_array[x][y][z] = pnoise3(nx, ny, nz, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, repeatz=1024, base=0)

    # Normalize the noise array to the range [0, 1]
    min_val = np.min(noise_array)
    max_val = np.max(noise_array)
    normalized_noise_array = (noise_array - min_val) / (max_val - min_val)

    return normalized_noise_array

# Function to create a grid of spheres inside the cube
def create_sphere_grid(grid_size, sphere_count):
    #equal subdivisions for each axis
    x = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    y = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    z = np.linspace(-grid_size/2, grid_size/2, sphere_count)
    xv, yv, zv = np.meshgrid(x, y, z) #3 lists, x-, y-, z-coordinates for all points, subarray-ed per axis
    return xv.flatten(), yv.flatten(), zv.flatten()

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

    create_noise_array(10)
        
    draw_cube(ax, size) # Drawing the cube

    # Creating a grid of spheres
    sphere_count = 15
    xs, ys, zs,  = create_sphere_grid(size, sphere_count)
    colors = create_noise_array(sphere_count)
    # Make the noise binary for better visibility
    colors[colors > 0.5] = 1
    colors[colors <= 0.5] = 0

    # Plotting the spheres
    sphere_size = 5  
    scatter = ax.scatter(xs, ys, zs, c=colors.flatten(), cmap='gray', s=sphere_size)

    # Setting aspect to be equal
    ax.set_box_aspect([1,1,1])

    plt.show()

# Run the main function
if __name__ == "__main__":
    main()