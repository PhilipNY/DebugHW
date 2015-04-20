#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from split import split
from listsets import listminus
import re, os

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    
    assert test([]) == PASS
    assert test(circumstances) == FAIL

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances



if __name__ == "__main__":
    tests = {}
    circumstances = []

    error_file = open('demo/urls.xml', 'r')
    file_content = error_file.read()

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    def mytest(c):
	
	global circumstances
	global tests
       
	s = ""
        for (index, char) in c:
            s += char

        if s in tests.keys():
            return tests[s]
     
    
        map = {}
        for (index, char) in c:
            map[index] = char

        x = ""
        for i in range(len(circumstances)):
            if map.has_key(i):
                x += map[i]
            else:
                x += "."

        print "%02i" % (len(tests.keys()) + 1), "Testing", `x`,
        
        tmp_file = open('tmp.xml', 'w')
        tmp_file.write(s)               
        tmp_file.close()
  
	
        status = os.system("python xpcmd.py tmp.xml")

        if os.WIFEXITED(status):
            exit_status = os.WEXITSTATUS(status)
	    if 0 == exit_status:
                print PASS
                tests[s] = PASS
                return PASS
	    elif 1 == exit_status:
                print FAIL
                tests[s] = FAIL
                return FAIL
            else:
                print UNRESOLVED
                tests[s] = UNRESOLVED
                return UNRESOLVED
        else:
            print UNRESOLVED
            tests[s] = UNRESOLVED
            return UNRESOLVED

    circumstances = string_to_list(file_content)
    mytest(circumstances)

    print ddmin(circumstances, mytest)
