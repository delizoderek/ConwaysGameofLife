import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Set the size of the grid
n = 10

# Create a binary colormap
cmap = colors.ListedColormap(['black', 'white'])
bounds = [0, 0.5, 1]
norm = colors.BoundaryNorm(bounds, cmap.N)

# Create the grid of colored squares
grid = np.random.rand(n, n)
fig, ax = plt.subplots()
ax.imshow(grid, cmap=cmap, norm=norm)

# Set the ticks and ticklabels
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(np.arange(1, n+1))
ax.set_yticklabels(np.arange(1, n+1))

# Ensure the grid is square
ax.set_aspect('equal')

def invert_square(event):
    if event.inaxes == ax:
        x, y = int(round(event.xdata)), int(round(event.ydata))
        grid[y, x] = 1 - grid[y, x]
        ax.imshow(grid, cmap=cmap, norm=norm)
        fig.canvas.draw()

# Connect the function to the click event
fig.canvas.mpl_connect('button_press_event', invert_square)

plt.show()


