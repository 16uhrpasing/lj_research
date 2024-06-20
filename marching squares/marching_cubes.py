import numpy as np
from noise import pnoise3
import matplotlib.pyplot as plt
from itertools import product, combinations
from tables import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

size = 50
# Creating a grid of spheres
sphere_count = 7
step_size = size/(sphere_count-1)

def render_isosurface(colorGrid, ax):
    maxCubeOffset = sphere_count-1

    for xoffset in range(maxCubeOffset):
        for yoffset in range(maxCubeOffset):
            for zoffset in range(maxCubeOffset):
                binaryIndex = 1
                triTableIndex = 0
                for i in vertexIndices:
                    #iteriere durch die farben per https://paulbourke.net/geometry/polygonise/ liste
                    color = colorGrid[i[0]+xoffset][i[1]+yoffset][i[2]+zoffset]
                    triTableIndex += int(color) * binaryIndex
                    binaryIndex *= 2

                #The Edge Table contains the order of the edgepoints to be drawn
                cubeEdgeTable = triTable[triTableIndex]
                currentEdgeIndex = 0
                terminate = 0
                while terminate != -1:
                    firstEdgePoint = np.array(edgePoints[cubeEdgeTable[currentEdgeIndex]])*step_size 
                    secondEdgePoint = np.array(edgePoints[cubeEdgeTable[currentEdgeIndex+1]])*step_size
                    thirdEdgePoint = np.array(edgePoints[cubeEdgeTable[currentEdgeIndex+2]])*step_size 
                    vertices = np.array([firstEdgePoint, secondEdgePoint, thirdEdgePoint])-(size/2.0)+ np.array([xoffset*step_size,yoffset*step_size,zoffset*step_size])
                    triangle = Poly3DCollection([vertices], color='red', alpha=1.0)
                    ax.add_collection3d(triangle)
                    
                    currentEdgeIndex += 3
                    terminate = cubeEdgeTable[currentEdgeIndex]

def create_noise_array(size, scale):
    noise_array = np.zeros((size, size, size)) #dimensions

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
            ax.plot3D(*zip(s, e), color="black") #draw the line

# Main function to set up the plot
def main():
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    draw_cube(ax, size) # Drawing the cube

    
    xs, ys, zs,  = create_sphere_grid(size, sphere_count)
    colors = create_noise_array(sphere_count, 2)
    # Make the noise binary for better visibility
    colors[colors > 0.5] = 1
    colors[colors <= 0.5] = 0 

    render_isosurface(colors,ax)

    # Plotting the spheres
    sphere_size = 5  
    #scatter = ax.scatter(xs, ys, zs, c=colors.flatten(), cmap='gray', s=sphere_size)

    # Setting aspect to be equal
    ax.set_box_aspect([1,1,1])

    plt.show()

# Run the main function
if __name__ == "__main__":
    main()