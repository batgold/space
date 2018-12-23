#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d.axes3d as p3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def update2(num, dots, data, text, title):

    lat = data[0][num][:]
    lon = data[1][num][:]
    alt = data[2][num][:]

    dots._offsets3d = (lon, lat, alt)

#    for n, sat in enumerate(sat_list):
#        tlat = data[0][num][n]
#        tlon = data[1][num][n]
#        talt = data[2][num][n]
#        text[n].set_position((tlon, tlat, talt))
#        #text[n] = ax.text(tlon, tlat, talt, '%s'%(sat.name), size=5, zorder=1)

#    n = 0
#    for x in ax.texts:
#        tlat = data[0][num][n]
#        tlon = data[1][num][n]
#        talt = data[2][num][n]
#        x._offset3d = (tlon, tlat, talt)
#        x.set_position((tlon, tlat, talt))
#        n += 1
#        #x.set_visible(False)

    title.set_text(num)

    #return text

def update(num, dots, data, dot_txt, ax):
    y = data[0][num][:]
    x = data[1][num][:]
    z = data[2][num][:]

    dots._offsets3d = (x, y, z)

    dot_txt = nmp.ones(nmp.size(data,2), dtype=str)
    for n in range(0,nmp.size(data, 2)):
        dot_txt[n] = ax.text(data[1][num][n], data[0][num][n], data[2][num][n],'%s'%(n))

def graph(data, update_cnt):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    dots = ax.scatter(data[1][0][:], data[0][0][:], data[2][0][:])
    dot_txt = nmp.ones(nmp.size(data,2), dtype=str)
    #dot_txt = []
    for n in range(0,nmp.size(data, 2)):
        dot_txt[n] = ax.text(data[1][0][n], data[0][0][n], data[2][0][n],'%s'%(n))

    ani = animation.FuncAnimation(fig, update, update_cnt, fargs=(dots, data,
        dot_txt, ax), interval=300)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.show()

def graph2(sat_list, target, lon_start, data, num_epochs):

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

    sat_names = []
    for n, sat in enumerate(sat_list):
        sat_names.append(sat.name[2:])

    dots = ax.scatter(data[1][0][:], data[0][0][:], data[2][0][:])
    #text = ax.text(data[1][0][:], data[0][0][:], data[2][0][:], '%s'%(sat_names), size=5)
    text = ax.text(data[1][0][0], data[0][0][0], data[2][0][0], '%s'%(sat_names), size=5)
    #text = 0

    #ani = animation.FuncAnimation(fig, update, num_epochs, fargs=(dots, data, text, title), interval=300, blit=False)

    #ani.save('animation.gif', writer='imagemagick')

    #plt.tight_layout(pad=0)
    plt.show()

"""
    text = []
    for n, sat in enumerate(sat_list):
        #text[n] = ax.text(data[1][0][n], data[0][0][n], data[2][0][n], '%s'%(sat.name), size=5, zorder=1)
        text.append(ax.text(data[1][0][n], data[0][0][n], data[2][0][n],
            '%s'%(sat.name), size=5, zorder=1))

    #ax.set_xlim(start_lon, stop_lon + 2)
    #ax.set_zlim(32000, 40000)
"""
