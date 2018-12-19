#!/usr/bin/python
import numpy as nmp
import coord_trans
from datetime import timedelta

class Satellite():

    def __init__(self, epoch, num_epochs):
        self.epoch = epoch
        self.num_epochs = num_epochs
        self.start_epoch = self.epoch
        self.lat = nmp.zeros(self.num_epochs)
        self.lon = nmp.zeros(self.num_epochs)
        self.alt = nmp.zeros(self.num_epochs)

    #  ---------------- convert pos/vel to lat/lon -----------------

    def load_tle(self, tle):
        self.name = tle[0]
        self.line1 = tle[1]
        self.line2 = tle[2]

        self.pos, self.vel, self.epoch_tle = coord_trans.sgp4(
                self.line1, self.line2, self.epoch)


    #  ---------------- convert pos/vel to lat/lon -----------------

    def get_lla(self, ndx):
        self.lat[ndx], self.lon[ndx], self.alt[ndx] = coord_trans.teme2lla(self.pos, self.epoch)


    #  ---------------- get motion, pos/epoch -----------------

    def get_motion(self):

        for n in range(0, self.num_epochs):
            self.epoch = self.start_epoch + timedelta(minutes=n)

            self.pos, self.vel, self.epoch_tle = coord_trans.sgp4(
                self.line1, self.line2, self.epoch)

            self.get_lla(n)
