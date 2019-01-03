#!/usr/bin/python
import argparse
import sys
import pickle
import graph as grf
from satellite import Satellite
from satellite import GraphFrame
import coord_trans
import space_track_api as api
from datetime import datetime, timedelta
import numpy as nmp
from tqdm import tqdm

#TODO: check out pyorbital

def main():
    inputs = read_input()
    x = calc_orbits(inputs)
    #output(x)


def read_input():
    inputs = {}

    #  ------------------ parse input arguments --------------------

    parser = argparse.ArgumentParser()
    t1_arg = parser.add_mutually_exclusive_group()
    t2_arg = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '-u', '--update', action='store_true', help='update TLE')
    parser.add_argument(
        'lon0', type=float, help='starting longitude')
    parser.add_argument(
        'targ', type=str, help='target satellite name')
    t1_arg.add_argument(
        '-n', '--now', action='store_true', help='start date = now')
    t1_arg.add_argument(
        '-t1', type=_datetime_type, nargs=1, help='start date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument(
        '-t2', type=_datetime_type, help='stop date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument(
        '-tr', type=_time_type, nargs=1, help='relative time from start, hh:mm:ss')

    args = parser.parse_args()

    #  --------------- get tle from space_track.org ----------------

    if args.update:
        session = api.login()
        tle_list = api.get_tle(session)
    else:
        with open('geo.tle', 'rb') as f:
            tle_list = pickle.load(f)

    inputs['tle_list'] = tle_list

    #  ------------------------ get epochs -------------------------

    # start time, t1
    if args.now:
        epoch1 = datetime.utcnow()
    else:
        epoch1= args.t1

    # end time, t2
    if args.tr:
        h = args.tr[0].hour
        m = args.tr[0].minute
        s = args.tr[0].second

        #datetime.timedelta([d,] [sec,] [microsec,] [msec,] [min,] [hr,] [week])
        epoch2 = epoch1 + timedelta(0,s,0,0,m,h)
    else:
        epoch2 = args.t2

    inputs['epoch1'] = epoch1
    inputs['epoch2'] = epoch2

    #  ---------------------- get locations ------------------------

    inputs['lon0'] = args.lon0
    inputs['target_name'] = args.targ

    return inputs


def calc_orbits(inputs):

    # Epoch 0 is pulled from the TLE; gives the most accurate orbit
    # Epoch 1 is the start time of the simulation
    # Epoch 2 is the end time of the simulation

    tle_list = inputs['tle_list']
    lon0 = inputs['lon0']
    target_name = inputs['target_name']
    epoch1 = inputs['epoch1']
    epoch2 = inputs['epoch2']


    #  ------------------- build satellite list --------------------

    sat_list = [Satellite(epoch1, epoch2) for n in range(0, len(tle_list), 3)]

    for n, sat in enumerate(tqdm(sat_list, desc='Loading Satellites')):
        tle = tle_list[n*3:n*3+3]
        sat.load_tle(tle)

        if target_name in sat.name:
            sat.type = 'target'
            sat_target = sat


    #  --------------- parse out objects in region -----------------

    #TODO: account for sats initially out of region

    # lon0 is the global starting point; defined by user
    # lon1 is the tracked satellite's longitude
    # lon2 is the global ending point; target's longitude

    tmp_list = []
    for n, sat in enumerate(sat_list):
        lon1 = sat.lon[0]
        lon2 = sat_target.lon[0]

        if (lon1 >= lon0 and lon1 <= lon2 and lon2 > lon0) \
        or (lon1 <= lon0 and lon1 >= lon2 and lon2 < lon0):
            tmp_list.append(sat)

    sat_list = tmp_list     # only sats in region of interest


    #  ------------------- calculate all epochs --------------------

    for n, sat in enumerate(tqdm(sat_list, desc='Computing Motion')):
        sat.get_motion()


    #  ----------------------- reformat data -----------------------

    frame_cnt = sat_list[0].sim_cnt
    frame_list = [GraphFrame(sat_list) for n in range(0, frame_cnt)]

    for n, frame in enumerate(tqdm(frame_list, desc='Building Frames')):
        frame.load_data(n)

    grf.graph(frame_list)



    sys.exit()
    data = nmp.zeros((3, sim_cnt, len(sat_list)))
    #name = nmp.zeros((num_epochs, len(sat_list)), dtype=str)

    #name = []
    for n, sat in enumerate(sat_list):
        #name.append(sat.name[2:])
        for m in range(0, sim_cnt):
            data[0][m][n] = sat.lat[m]
            data[1][m][n] = sat.lon[m]
            data[2][m][n] = sat.alt[m]

    #  ----------------------- print results -----------------------

    print('\r')
    print('epoch start: ', epoch, '\r')
    print('epoch end: ', epoch_end, '\n')
    print(len(sat_list), ' objects found.\n')
    print(sat_target.name[2:], ' lon:', sat_target.lon[0], '\n')

    #grf.graph(sat_list, sat_target, lon0, data, num_epochs)
    grf.graph(data, num_epochs)


    #  ----------------------- close session -----------------------

    if args.update:
        api.close(session)

def _target_lon(name_list, target_name, lla_list):
    # get the lon of target from input name

    for n, name in enumerate(name_list):
        if target_name in name:
            return name, lla_list[n][1]

def _datetime_type(arg_datetime):
    return datetime.strptime(arg_datetime, '%x-%X')

def _time_type(arg_time):
    return datetime.strptime(arg_time, '%X')

if __name__ == '__main__':
    main()
