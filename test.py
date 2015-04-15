#!/usr/bin/env python

import all_global
import os

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def mytest(c):

    s = ""
    for (index, char) in c:
        s += char

    if s in all_global.tests.keys():
        return all_global.tests[s]
     
    """
    map = {}
    for (index, char) in c:
        map[index] = char

    x = ""
    for i in range(len(all_global.circumstances)):
        if map.has_key(i):
            x += map[i]
        else:
            x += "."

    print "%02i" % (len(all_global.tests.keys()) + 1), "Testing", `x`,
        
    tmp_file = open('tmp.xml', 'w')
    tmp_file.write(s)               
    tmp_file.close()
    """
	
    status = os.system("python xpcmd.py tmp.xml")

    if os.WIFEXITED(status):
        exit_status = os.WEXITSTATUS(status)
	if 0 == exit_status:
            print PASS
            all_global.tests[s] = PASS
            return PASS
	elif 1 == exit_status:
            print FAIL
            all_global.tests[s] = FAIL
            return FAIL
        else:
            print UNRESOLVED
            all_global.tests[s] = UNRESOLVED
            return UNRESOLVED
    else:
        print UNRESOLVED
        all_global.tests[s] = UNRESOLVED
        return UNRESOLVED
