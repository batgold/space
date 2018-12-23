#!/usr/bin/python
import argparse
import sys
import pickle
import graph as grf
from satellite import Satellite
import coord_trans
import space_track_api as api
from datetime import datetime, timedelta
import numpy as nmp
from tqdm import tqdm

#TODO: check out pyorbital

def _target_lon(name_list, target_name, lla_list):
    # get the lon of target from input name

    for n, name in enumerate(name_list):
        if target_name in name:
            return name, lla_list[n][1]

def _datetime_type(arg_datetime):
    return datetime.strptime(arg_datetime, '%x-%X')

def main():

    #  --------------- get user inputs ----------------

    parser = argparse.ArgumentParser()
    t1_arg = parser.add_mutually_exclusive_group()
    t2_arg = parser.add_mutually_exclusive_group()
    parser.add_argument('-u', '--update', action='store_true', help='update TLE')
    parser.add_argument('lon0', type=float, help='starting longitude')
    parser.add_argument('targ', type=str, help='target satellite name')
    t1_arg.add_argument('-n', '--now', action='store_true', help='start date = now')
    t1_arg.add_argument('-t1', type=_datetime_type, nargs=1, help='start date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument('-t2', type=_datetime_type, help='stop date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument('-hr', type=int, nargs=1, help='relative time from start, hr')

    args = parser.parse_args()

    #  --------------- get tle from space_track.org ----------------

    if args.update:
        session = api.login()
        tle_list = api.get_tle(session)
    else:
        with open('geo.tle', 'rb') as f:
            tle_list = pickle.load(f)

    #  ----------------------- request epoch -----------------------

    if args.now:
        epoch = datetime.utcnow()
    else:
        #TODO: accept datetime input
        epoch = False

    #TODO: calc # hours from T1 to T2
    if args.hr:
        epoch_end = epoch + timedelta(hours=args.hr[0])
        num_epochs = args.hr[0]
    else:
        epoch_end = args.t2.day

    lon_start = args.lon0
    name_target = args.targ


    #  ------------------- build satellite list --------------------

    tmp_list = []
    sat_list = [Satellite(epoch, num_epochs) for n in range(0, len(tle_list), 3)]

    for n, sat in enumerate(tqdm(sat_list, desc='Loading Satellites')):
        sat.load_tle(tle_list[n*3:n*3+3])
        sat.get_lla(0)

        if name_target in sat.name:
            sat_target = sat


    #  --------------- parse out objects in region -----------------

    for n, sat in enumerate(sat_list):
        # check if sat longitude is outside bounds
        lon = sat.lon[0]
        target_lon = sat_target.lon[0]

        #if (sat.lon >= lon_start and sat.lon <= sat_target.lon and sat_target.lon > lon_start) \
        #or (sat.lon <= lon_start and sat.lon >= sat_target.lon and sat_target.lon < lon_start):
            #tmp_list.append(sat)
        if (lon >= lon_start and lon <= target_lon and target_lon > lon_start) \
        or (lon <= lon_start and lon >= target_lon and target_lon < lon_start):
            tmp_list.append(sat)

    sat_list = tmp_list


    #  ------------------- calculate all epochs --------------------

    for n, sat in enumerate(tqdm(sat_list, desc='Computing Motion')):
        sat.get_motion()


    #  ----------------------- reformat data -----------------------

    data = nmp.zeros((3, num_epochs, len(sat_list)))
    #name = nmp.zeros((num_epochs, len(sat_list)), dtype=str)

    #name = []
    for n, sat in enumerate(sat_list):
        #name.append(sat.name[2:])
        for m in range(0, num_epochs):
            data[0][m][n] = sat.lat[m]
            data[1][m][n] = sat.lon[m]
            data[2][m][n] = sat.alt[m]

    #  ----------------------- print results -----------------------

    print('\r')
    print('epoch start: ', epoch, '\r')
    print('epoch end: ', epoch_end, '\n')
    print(len(sat_list), ' objects found.\n')
    print(sat_target.name[2:], ' lon:', sat_target.lon[0], '\n')

    #grf.graph(sat_list, sat_target, lon_start, data, num_epochs)
    grf.graph(data, num_epochs)


    #  ----------------------- close session -----------------------

    if args.update:
        api.close(session)

if __name__ == '__main__':
    main()
