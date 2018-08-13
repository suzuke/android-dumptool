#!/usr/bin/env python

from subprocess import check_output
import sys

def get_pid(name):
    """
    Get the PID of a given process name via adb shell and ps

    name - Name of process

    Returns: PID of process

    """

    ps_list = check_output(['adb', 'shell', 'ps']).splitlines()

    for process in ps_list:
        if name in process:
            pid = process.split()[1]
            print "Found PID: {0} of process {1}".format(pid, name)
            return pid


def get_map(pid):
    """
    Get the memory map for a given PID as a list

    Returns: List of tuples: (start_address, end_address, pathname)
    """

    map_list = check_output(['adb', 'shell', 'su', '-c', 'cat', '/proc/' + str(pid) + '/maps']).splitlines()
    #print map_list
    splitted_list = [map.split() for map in map_list]
    splitted_list = list(filter(None, splitted_list))
    #print splitted_list
    
    final_list = []

    for map in splitted_list:
        #print map
        memory_range = map[0].split('-')
        start_addr = memory_range[0]
        end_addr = memory_range[1]

        if len(map) == 6:
            path = map[5]
        else:
            path = "(anonymous)"

        if not path.startswith('/system'):
            final_list.append((start_addr, end_addr, path))
        
    return final_list


def search_memory(pid, start, end, string, ascii=True):
    """
    Search a memory range of a PID for a given UTF-16 string

    """
    if ascii is True:
        search = '-a'
    else:
        search = '-u'

    output = check_output(['adb', 'shell', '/data/local/tmp/dumptool', pid, start, end, '-s', search, string])
    if len(output) != 0:
        print "At memory range {0}-{1} in path {2}:".format(map[0], map[1], map[2])
        print output

def dump_to_file(pid, start, end, file="memdump"):
    """
    Dump a memory range of a PID to a file, using the dumptool executable on the device

    Pulls the dumpfile to the local machine

    Deletes the dumpfile on the device

    """
    print check_output(['adb', 'shell', '/data/local/tmp/dumptool', pid, start, end, '-d', '/data/local/tmp/' + file])

    print check_output(['adb', 'pull', '/data/local/tmp/' + file])

    print check_output(['adb', 'shell', 'rm', '/data/local/tmp/' + file])


if __name__ == "__main__":
    
    PID_NAME = "com.test"
    SEARCH_STRING = "9460301" #0x905a4d #9460301
    pid = get_pid(PID_NAME)
    
    maps = get_map(pid)
    #dump_to_file(pid, maps[0][0], maps[0][1])
    
    #print "Searching ASCII strings"
    for map in maps:
        search_memory(pid, map[0], map[1], SEARCH_STRING)

    #print "Searching UTF-16 strings"
    for map in maps:
        search_memory(pid, map[0], map[1], SEARCH_STRING, ascii=False) 


