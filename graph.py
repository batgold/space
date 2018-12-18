#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graph(sat_list, target, lon_start):

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    for n, sat in enumerate(sat_list):

        if 'R/B' in sat.name:
            s = ax.scatter(sat.lon, sat.lat, zs=sat.alt, s=20, c='r', marker='^')

        else:
            s = ax.scatter(sat.lon, sat.lat, zs=sat.alt, s=20, c='C0', alpha=0.5)

        ax.text(sat.lon+0.1, sat.lat+0.1, sat.alt+0.1, '%s'%(sat.name[2:]), size=6, zorder=1)

    # start location
    s = ax.scatter(lon_start, 0, zs=35786, s=60, c='C2', marker='s', alpha=0.9)

    # target location
    s = ax.scatter(target.lon, target.lat, zs=target.alt, s=60, c='C2', marker='s', alpha=0.9)

    #ax.set_xlim(start_lon, stop_lon + 2)
    #ax.set_zlim(32000, 40000)

    ax.set_xlabel(r'Longitude, $\circ$E')
    ax.set_ylabel('Latitude, deg')
    ax.set_zlabel('Altitude, km')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.tight_layout(pad=0)
    plt.show()
