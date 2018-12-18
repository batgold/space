#!/usr/bin/python
import coord_trans

class Satellite():

    def __init__(self, epoch):
        self.epoch = epoch

    #  ---------------- convert pos/vel to lat/lon -----------------

    def load_tle(self, tle):
        self.name = tle[0]
        self.line1 = tle[1]
        self.line2 = tle[2]

        self.pos, self.vel, self.epoch_tle = coord_trans.sgp4(
                self.line1, self.line2, self.epoch)

        self.x = self.pos[0]
        self.y = self.pos[1]
        self.z = self.pos[2]


    #  ---------------- convert pos/vel to lat/lon -----------------

    def get_lla(self):
        self.lat, self.lon, self.alt = coord_trans.teme2lla(self.pos, self.epoch)
