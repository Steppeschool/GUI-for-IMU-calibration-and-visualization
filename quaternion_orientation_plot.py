import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import combinations, product
from pyquaternion import Quaternion


def plot_cube_quaternion(q):
    # Plot the cube
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect("equal")
    #set limities
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    # draw cube
    r = [-0.5, 0.5]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color="b", alpha=0.2)
    # draw a vector
    def draw_vector(v0, v1, color="r", a=1.0):
        ax.plot3D(*zip(v0, v1), color=color, alpha=a)
    # draw the cube rotated by the quaternion
    for i in range(8):
        v = np.array([r[i%2], r[(i//2)%2], r[(i//4)%2]])
        v_rot = q.rotate(v)
        draw_vector(v, v_rot, color="g", a=0.1)
    
    #draw the edges of the rotated cube
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            v0 = q.rotate(s)
            v1 = q.rotate(e)
            draw_vector(v0, v1, color="r")

    plt.show()
    return

if __name__ == "__main__":
    q = Quaternion(0.5, 0.5, 0.5, 0)

    #q = Quaternion(axis=[1, 0, 0], angle=np.pi/4)
    # Plot the cube
    plot_cube_quaternion(q)