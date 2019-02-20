#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
import matplotlib.gridspec as grs
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

class Graph():

    def __init__(self, frame_list, lon0, lon2, epoch1):
        self.frame_list = frame_list
        self.lon0 = lon0
        self.lon2 = lon2
        self.epoch1 = epoch1
        self.fig, self.ax, self.txt = self._setup_fig()
        self.frame_cnt = len(self.frame_list)

    def _setup_fig(self):
        gs = grs.GridSpec(1, 2, width_ratios=[4,1])
        fig = plt.figure()
        fig.set_size_inches(14, 8, True)
        ax = fig.add_subplot(gs[0], projection='3d')
        ax2 = fig.add_subplot(gs[1])
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        #plt.axis('off')
        #plt.tight_layout(pad=0)
        plt.subplots_adjust(wspace=0.00001)
        return fig, ax, ax2

    def run(self):
        ani = animation.FuncAnimation(
                fig=self.fig,
                init_func=self._init_graph,
                func=self._update_graph,
                frames=self.frame_cnt,
                interval=200)

        plt.show()
        #ani.save('orb3.gif', writer='imagemagick', fps=5, dpi=128)

    def _init_graph(self):
        self.ax.set_xlabel('Latitude, $\circ$E')
        self.ax.set_ylabel('Longitude, $\circ$E')
        self.ax.set_zlabel('Altitude, km')
        self.ax.set_xlim3d(-15,15)
        self.ax.set_zlim3d(35600,36100)
        if self.lon2 > self.lon0:
            self.ax.set_ylim3d(self.lon0-2, self.lon2+2)
        else:
            self.ax.set_ylim3d(self.lon0+2, self.lon2-2)
        #self.txt.axis('off')
        self.txt.grid(False)
        self.txt.set_xticks([])
        self.txt.set_yticks([])

    def _update_graph(self, f):
        frame = self.frame_list[f]

        self.ax.clear()
        self.txt.clear()
        self._init_graph()

        self._update_sats(frame)
        self._update_text(frame)

    def _update_sats(self, frame):
        for n in range(len(frame.lon)):
            x, y, z, s, c, m, name = frame.get_params(n)

            center = (self.lon2+self.lon0)/2
            self.ax.scatter(x, y, z, s=s, c=c, marker=m)
            self.ax.text(x, y, z+10, '%s'%(name), size=5, zorder=1)

    def _update_text(self, frame):
        self.txt.text(0.0,0.92,'Epoch Start:', size=8)
        self.txt.text(0.1,0.90,'%s'%(self.epoch1), size=8)
        self.txt.text(0.0,0.87,'Mission Time:', size=8)
        self.txt.text(0.1,0.85,'%.2f hr'%(frame.mission_time), size=8)
        self.txt.text(0.0,0.82,'RSGS Longitude:', size=8)
        self.txt.text(0.1,0.8,'%.2f deg'%(frame.lon[-1]), size=8)
        self.txt.text(0.0,0.75,'Range to Object, km:', size=8)

        for n, r in enumerate(frame.range[0:10]):
            name = frame.name_sorted[n]
            color = frame.range_color[n]
            self.txt.text(0.1, 0.73-n*0.015,'%.2f'%(r), size=8, color=color)
            self.txt.text(0.4, 0.73-n*0.015,'%s'%(name), size=8, color=color)

class GraphFrame():

    def __init__(self, sat_list):
        self.sat_list = sat_list
        self.dt = self.sat_list[0].dt
        self.lat = []
        self.lon = []
        self.alt = []
        self.size = []
        self.name = []
        self.color = []
        self.range = []
        self.marker = []
        self.mission_time = 0

    def load_data(self, epoch):

        self.mission_time = epoch * self.dt / 3600  # days

        for sat in self.sat_list:
            self.name.append(sat.name[2:])      # remove leading zero
            self.lat.append(sat.lat[epoch])
            self.lon.append(sat.lon[epoch])
            self.alt.append(sat.alt[epoch])
            self.range.append(sat.range[epoch])

            if sat.type == 'RB':
                self.size.append(30)
                self.color.append('r')
                self.marker.append('^')
            elif sat.type == 'RSGS':
                self.size.append(60)
                self.color.append('b')
                self.marker.append('s')
            elif sat.type == 'target':
                #self.name[-1] = 'RSO-1'
                self.size.append(40)
                self.color.append('C2')
                self.marker.append('o')
            else:
                self.size.append(16)
                self.color.append('C0')
                self.marker.append('o')

        self.range, self.name_sorted = zip(*sorted(zip(self.range,self.name)))
        self.range = self.range[1:]             # Remove RSGS from List
        self.name_sorted = self.name_sorted[1:]

        red_lim = 250
        yel_lim = 500
        self.range_color = ['C3' if r < red_lim else 'C4' if r < yel_lim else 'C0' for r in self.range]

    def get_params(self, n):
        return [self.lat[n],
                self.lon[n],
                self.alt[n],
                self.size[n],
                self.color[n],
                self.marker[n],
                self.name[n]]
