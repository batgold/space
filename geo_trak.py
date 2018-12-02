#!/usr/bin/python
from datetime import datetime
import pickle
import numpy as nmp
import space_track_api as api
import tle2teme as t2t
import teme2llh as t2g

#check out:
#pyorbital

#  ----------------------- request epoch -----------------------
#TODO: ask for future or past date
epoch = datetime.utcnow()

#  --------------- get tle from space_track.org ----------------

with open('geo_tle', 'rb') as f:
    tle_set = pickle.load(f)

print(len(tle_set)/3, ' objects found.\n')
#session = api.login()

#tle = api.get_tle(session)


#  ------------------- convert tle to pos/vel ------------------

pos = []
for n, item in enumerate(tle_set[900:909:3]):
    tle = tle_set[n*3+1:n*3+3]
    print(item)
    print(tle, '\n')

    pos.append(t2t.sgp4(tle, epoch))
print(pos)


#  ---------------- convert pos/vel to lat/lon -----------------

lat, lon, alt = t2g.teme2llh(pos, epoch)
print('lat: ', lat)
print('lon: ', lon)
print('alt: ', alt)

#api.close(session)
