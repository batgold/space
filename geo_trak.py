#!/usr/bin/python
import sys
import pickle
import space_track_api as api
import tle2teme
import teme2lla
import graph as grf
from datetime import datetime

#check out:
#pyorbital

def _target_lon(name_list, target_name, lla_list):
    # get the lon of target from input name

    for n, name in enumerate(name_list):
        if target_name in name:
            return name, lla_list[n][1]

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
        pos, name, epoch = tle2teme.sgp4(tle, epoch)

        pos_list.append(pos)
        name_list.append(name)
        epoch_list.append(epoch)


    #  ---------------- convert pos/vel to lat/lon -----------------

    lla_list = []

    for n, pos in enumerate(pos_list):
        if epoch_start == '-tle':
            epoch = epoch_list[n]

        lla = teme2lla.teme2lla(pos, epoch)
        lla_list.append(lla)


    #  --------------- parse out objects in region -----------------

    lat_list = []
    lon_list = []
    alt_list = []
    tmp_list = []

    id_target, lon_target = _target_lon(name_list, name_target, lla_list)

    for n, item in enumerate(lla_list):
        lon = item[1]
        if (lon >= lon_start and lon <= lon_target and lon_target > lon_start) \
        or (lon <= lon_start and lon >= lon_target and lon_target < lon_start):
            lat_list.append(item[0])
            lon_list.append(item[1])
            alt_list.append(item[2])
            tmp_list.append(name_list[n])

    name_list = tmp_list


    #  ----------------------- print results -----------------------

    print(len(lon_list), ' objects found.\n')
    print(id_target[2:], ' lon:', lon_target)


    #  ----------------------- graph results -----------------------

    grf.graph(
            name_list, lat_list, lon_list, alt_list, name_target)

    if tle_file == '-l':
        api.close(session)

if __name__ == '__main__':
    tle_file = sys.argv[1]
    lon_start = float(sys.argv[2])
    name_target = sys.argv[3]
    epoch_start = sys.argv[4]

    main()
