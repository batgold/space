#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graph(name, lat, lon, alt, start_lon, stop_lon, target_name):
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    for n, item in enumerate(name):
        if 'R/B' in item:
            s = ax.scatter(lon[n], lat[n], zs=alt[n], s=20, c='r', marker='^')
        elif target_name in item:
            s = ax.scatter(lon[n], lat[n], zs=alt[n], s=25, c='g', alpha=0.5)
        else:
            s = ax.scatter(lon[n], lat[n], zs=alt[n], s=20, c='C0', alpha=0.5)

        ax.text(lon[n]+0.1, lat[n]+0.1, alt[n]+0.1, '%s'%(item[2:]), size = 6, zorder=1)

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
    #y = nmp.zeros(len(lon))
    #plt.plot(lon, y, '+')

    #plt.show()



