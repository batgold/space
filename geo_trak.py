#!/usr/bin/python
import sys
import pickle
import space_track_api as api
import tle2teme as t2t
import teme2llh as t2g
import graph as grf
from datetime import datetime

#check out:
#pyorbital

def _target_lon(name_list, target_name, llh):
    # get the lon of target from input name
    for n, name in enumerate(name_list):
        if target_name in name:
            return llh[n][1]

def main():

    #  --------------- get tle from space_track.org ----------------

    if tle_file == '-l':
        session = api.login()
        tle_list = api.get_tle(session)

    else:
        with open('geo.tle', 'rb') as f:
            tle_list = pickle.load(f)


    #  ----------------------- request epoch -----------------------

    if epoch_start == '-now':
        epoch = datetime.utcnow()
    elif epoch_start == '-tle':
        epoch = False
    else:
        #TODO: get input datetime
        return None


    #  ------------------- convert tle to pos/vel ------------------

    pos_list = []
    name_list = []
    epoch_list = []

    for n in range(0, len(tle_list), 3):
        tle = tle_list[n:n+3]
        pos, name, epoch = t2t.sgp4(tle, epoch)

        pos_list.append(pos)
        name_list.append(name)
        epoch_list.append(epoch)


    #  ---------------- convert pos/vel to lat/lon -----------------

    lla_list = []
    for n, pos in enumerate(xyzs):
        if epoch_start == '-tle':
            epoch = epochs_tle[n]

        tmp = t2g.teme2llh(pos, epoch)
        llh.append(tmp)


    #  --------------- parse out objects in region -----------------
    lat = []
    lon_list = []
    alt = []
    tmp = []

    target_lon = _target_lon(name_list, name_target, llh)

    for n, item in enumerate(llh):
        lon = item[1]
        if (lon >= lon_start and lon <= target_lon and target_lon > lon_start) \
        or (lon <= lon_start and lon >= target_lon and target_lon < lon_start):
            lat.append(item[0])
            lon_list.append(lon)
            alt.append(item[2])
            tmp.append(name_list[n])
    name = tmp


    #  ----------------------- print results -----------------------

    print(len(lon_list), ' objects found.\n')
    print('target lon:', target_lon)


    #  ----------------------- graph results -----------------------

    grf.graph(name, lat, lon_list, alt, lon_start, target_lon, name_target)

    if tle_file == '-l':
        api.close(session)

if __name__ == '__main__':
    tle_file = sys.argv[1]
    lon_start = float(sys.argv[2])
    name_target = sys.argv[3]
    epoch_start = sys.argv[4]

    main()
