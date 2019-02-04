#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def _graphA(frame_list):

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    frame_cnt = len(frame_list)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.draw()

    for f in range(frame_cnt):

        frame = frame_list[f]

        for n in range(0, len(frame.marker)):
            x, y, z, s, c, m, name = frame.get_params(n)

            ax.scatter(x, y, z, s=s, c=c, marker=m, alpha=0.6)
            ax.text(x+0.1, y+0.1, z+0.1, '%s'%(name), size=6, zorder=1)

            #title.set_text('%s / %s'%(f+1, frame_cnt))
        ax.text(-15,166,36500,'%s / %s'%(f+1, frame_cnt),size=20)
        fig.canvas.draw_idle()
        plt.pause(0.1)
        ax.clear()

    plt.waitforbuttonpress()

def _graphB(frame_list):
    """
    Plot Results
    Text Items & Marker Styles must be added singly in a loop :(
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    update_graph(0, frame_list, ax)
    frame_cnt = len(frame_list)

    ani = animation.FuncAnimation(fig, update_graph, frame_cnt, fargs=(frame_list, ax), interval=300)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.show()

def _update_graphB(f, frame_list, ax):

    frame = frame_list[f]

    for n in range(0, len(frame.marker)):
        x, y, z, s, c, m, name = frame.get_params(n)

        #WORKING
        ax.scatter(x, y, z, s=s, c=c, marker=m, alpha=0.5)
        if f == 0:
            ax.text(x+0.1, y+0.1, z+0.1, '%s'%(name), size=6, zorder=1)

def _graphC(sat_list, target, lon_start, data, num_epochs):

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



    #ani = animation.FuncAnimation(fig, update, num_epochs, fargs=(dots, data, text, title), interval=300, blit=False)

    #ani.save('animation.gif', writer='imagemagick')

    #plt.tight_layout(pad=0)
    #plt.show()
    pass

def graph(frame_list):

    fig = plt.figure()
    fig.set_size_inches(10, 8, True)
    ax = fig.add_subplot(111, projection='3d')

    frame_cnt = len(frame_list)

    ani = animation.FuncAnimation(fig, update_graph, frame_cnt,
            fargs=(frame_list, ax, frame_cnt), interval=600)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.tight_layout(pad=0)
    plt.show()
    #ani.save('orb3.gif', writer='imagemagick', fps=10, dpi=128)

def update_graph(f, frame_list, ax, cnt):

    ax.clear()
    f = nmp.mod(f, cnt)
    frame = frame_list[f]
    dt = frame.dt/3600

    for n in range(len(frame.marker)):
        x, y, z, s, c, m, name = frame.get_params(n)

        #WORKING
        ax.scatter(x, y, z, s=s, c=c, marker=m)
        ax.text(x+0.1, y+0.1, z+0.1, '%s'%(name), size=5, zorder=1)
        ax.text(0,155,36250,'Mission Time: %.2f hr'%(f*dt), size=20)
        #ax.text(0,155,36000,'%s / %s'%(f, cnt-1), size=20)

        ax.set_xlabel('Latitude, deg')
        ax.set_ylabel('Longitude, $\circ$E')
        ax.set_zlabel('Altitude, km')

        ax.set_xlim3d(-3,13)
        ax.set_ylim3d(150, 167)
        ax.set_zlim3d(35600,36100)
