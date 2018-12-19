#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d.axes3d as p3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def update(num, dots, data, title):

    lat = data[0][num][:]
    lon = data[1][num][:]
    alt = data[2][num][:]

    dots._offsets3d = (lon, lat, alt)
    #for n, sat in enumerate(sat_list):
        #ax.text(data[1][0][n], data[0][0][n], data[2][0][n], '%s'%(sat.name), size=5, zorder=1)
    title.set_text(num)

def graph(sat_list, target, lon_start, data, num_epochs):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

#    # start location
#    s = ax.scatter(lon_start, 0, zs=35786, s=60, c='C2', marker='s', alpha=0.9)
#
#    # target location
#    s = ax.scatter(target.lon, target.lat, zs=target.alt, s=60, c='C2', marker='s', alpha=0.9)
#
#    # all sats in region
#    for n, sat in enumerate(sat_list):
#
#        if 'R/B' in sat.name:
#            s = ax.scatter(sat.lon, sat.lat, zs=sat.alt, s=20, c='r', marker='^')
#
#        else:
#            s = ax.scatter(sat.lon, sat.lat, zs=sat.alt, s=20, c='C0', alpha=0.5)
#
#        ax.text(sat.lon+0.1, sat.lat+0.1, sat.alt+0.1, '%s'%(sat.name[2:]), size=6, zorder=1)

    ax.set_xlabel(r'Longitude, $\circ$E')
    ax.set_ylabel('Latitude, deg')
    ax.set_zlabel('Altitude, km')
    title = ax.set_title('frogger')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    dots = ax.scatter(data[1][0][:], data[0][0][:], data[2][0][:])
    for n, sat in enumerate(sat_list):
        ax.text(data[1][0][n], data[0][0][n], data[2][0][n], '%s'%(sat.name), size=5, zorder=1)

    #ax.set_xlim(start_lon, stop_lon + 2)
    #ax.set_zlim(32000, 40000)

    ani = animation.FuncAnimation(
            fig, update, num_epochs, fargs=(dots, data, title), interval=300, blit=False)
    #ani.save('animation.gif', writer='imagemagick')

    #plt.tight_layout(pad=0)
    plt.show()
