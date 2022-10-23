from concurrent.futures import thread
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import combinations, product
from pyquaternion import Quaternion

import serial
import struct
from threading import Thread
import time

from matplotlib.animation import FuncAnimation


def plot_cube_quaternion(q):
    ''' Plot cube with quaternion orientation '''
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
        v = np.array([r[i % 2], r[(i//2) % 2], r[(i//4) % 2]])
        v_rot = q.rotate(v)
        draw_vector(v, v_rot, color="g", a=0.1)

    # draw the edges of the rotated cube
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            v0 = q.rotate(s)
            v1 = q.rotate(e)
            draw_vector(v0, v1, color="r")

    return


def receive_quaternion():
    ''' Receive quaternion from Serial connection '''
    # read quaternion, each quaternion is 4bytes-float numbers
    q1 = uart_mcu.read(4)
    q2 = uart_mcu.read(4)
    q3 = uart_mcu.read(4)
    q4 = uart_mcu.read(4)
    # convert to float
    q1 = struct.unpack('f', q1)[0]
    q2 = struct.unpack('f', q2)[0]
    q3 = struct.unpack('f', q3)[0]
    q4 = struct.unpack('f', q4)[0]
    # create quaternion
    q = Quaternion(q1, q2, q3, q4)
    return q


def plot_animation(i):
    ''' Animation function callback to plot the cube '''
    global q
    # clearing the figure
    ax.clear()
    # plot the cube
    plot_cube_quaternion(q)


def receive_data():
    ''' Thread function to receive data from Serial connection indefinitely '''
    global q
    while True:
        q = receive_quaternion()


if __name__ == "__main__":
    # Create figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect("equal")
    # set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    # Create animation callback
    ani = FuncAnimation(fig, plot_animation, frames=100,
                        interval=10, blit=False)

    # uart comport
    uart_mcu = serial.Serial('COM7', 115200, parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    uart_thread = Thread(target=receive_data, daemon=True)
    uart_thread.start()
    plt.show()

    #q = Quaternion(0.5, 0.5, 0.5, 0)
    #q = Quaternion(axis=[1, 0, 0], angle=np.pi/4)
    #q = receive_quaternion()
    # Plot the cube
    # plot_cube_quaternion(q)
