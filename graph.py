#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graph(name, lat, lon, alt):
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    for n, item in enumerate(name):
        if 'R/B' in item:
            ax.scatter(lon[n], alt[n], zs=lat[n], s=10, c='r', marker='^')
        else:
            ax.scatter(lon[n], alt[n], zs=lat[n], s=10, c='C0', alpha=0.5)

    ax.set_xlim([-30, 30])
    ax.set_ylim([30000, 40000])

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.show()
    #y = nmp.zeros(len(lon))
    #plt.plot(lon, y, '+')

    #plt.show()



