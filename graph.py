#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graph(name, lat, lon, alt):
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    for n, item in enumerate(name):
        if 'R/B' in item and nmp.abs(lon[n]) < 30:
            ax.scatter(lon[n], lat[n], zs=alt[n], s=10, c='r', marker='^')
        elif nmp.abs(lon[n]) < 30:
            ax.scatter(lon[n], lat[n], zs=alt[n], s=10, c='C0', alpha=0.5)

    ax.set_xlim([-30, 30])
    ax.set_zlim([32000, 40000])

    ax.set_xlabel('Longitude, deg')
    ax.set_ylabel('Latitude, deg')
    ax.set_zlabel('Altitude, km')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.show()
    #y = nmp.zeros(len(lon))
    #plt.plot(lon, y, '+')

    #plt.show()



