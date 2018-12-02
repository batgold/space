#!/usr/bin/python
from datetime import datetime
import pickle
import numpy as nmp
import space_track_api as api
import tle2teme as t2t
import teme2llh as t2g
import graph as grf

#check out:
#pyorbital

#  ----------------------- request epoch -----------------------
#TODO: ask for future or past date
epoch = datetime.utcnow()

#  --------------- get tle from space_track.org ----------------

session = api.login()
#with open('geo_tle', 'rb') as f:
    #tle_set = pickle.load(f)

tle_set = api.get_tle(session)


#  ------------------- convert tle to pos/vel ------------------

name = []
pos = []
#for n, item in enumerate(tle_set[825:921:3]):
for n, item in enumerate(tle_set[0::3]):
    tle = tle_set[n*3+1:n*3+3]
    name.append(item)
    pos.append(t2t.sgp4(tle, epoch))


#  ---------------- convert pos/vel to lat/lon -----------------

lat = []
lon = []
alt = []
for n, item in enumerate(pos):
    lla = t2g.teme2llh(item, epoch)
    lat.append(lla[0])
    lon.append(lla[1])
    alt.append(lla[2])


#  ---------------- print results -----------------

print(len(tle_set)/3, ' objects found.\n')
#for n in range(len(pos)):
    #print('\n', name[n])
    #print('lat: ', lat[n])
    #print('lon: ', lon[n])
    #print('alt: ', alt[n])

#  ---------------- graph results -----------------

grf.graph(name, lat, lon, alt)

api.close(session)
