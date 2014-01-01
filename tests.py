from bloompy import BloomFilter
import random
import math
import time

def test_error_rate():
    n = 10000
    p = 0.001
    b = BloomFilter(n, p)
    print "Creating BloomFilter for %d elements and false positive probability = %f ..." % (n, p)
    print "Optimal values are m = %d, k = %d" % (b.m, b.k)
    elt = 'apple'
    
    print "Testing..."
    assert elt not in b
    
    print "After adding '%s'..." % elt
    b.add(elt)
    
    print "Testing..."
    assert elt in b
    
    # create random strings
    strings = set()
    string_size = 20
    for i in range(n):
    	string = ""
    	for j in range(string_size):
    		string += chr(random.randint(0, 255))
    	strings.add(string)
    
    # other strings
    other_strings = set()
    for i in range(n):
    	string = ""
    	for j in range(string_size):
    		string += chr(random.randint(0, 255))
    	other_strings.add(string)
    
    # add all to set
    for s in list(strings):
    	b.add(s)
    
    # test for collisions
    other_strings = other_strings - strings
    collisions = 0
    for s in list(other_strings):
    	if s in b:
    		collisions += 1
    
    print "False positive rate was %d / %d = %f" % (
    	collisions, len(other_strings), 
    	float(collisions) / float(len(other_strings)))
    
def test_speed():
    
    n = 10000
    p = 0.0001
    b = BloomFilter(n, p)
    print b
    
    strings = set()
    string_size = 20
    for i in range(n):
    	string = ""
    	for j in range(string_size):
    		string += chr(random.randint(0, 255))
        strings.add(string)
    
    total_time = 0
    starttime = time.time()
    for string in strings:
    	b.add(string)
    total_time = (time.time() - starttime)
    	
    ns = float(len(strings))
    k = float(b.k)
    total_time = float(total_time)
    
    print "Number of hash functions: %d" % b.k
    print "Speed per hash: %f seconds" % (total_time / ns / k)
    print "Speed per add: %f seconds" % (total_time / ns)
    
def test_performance():

    n = 100000
    p = 0.001
    
    # create set of strings to use
    strings = set()
    string_size = 50    # make this number higher 
                        # if performance test is taking too long
    while len(strings) < n:
    	string = ""
    	for j in range(string_size):
    		string += chr(random.randint(0, 255))
        strings.add(string)
        
    # create another set
    otherstrings = set()
    while len(otherstrings) < n:
        string = ""
    	for j in range(string_size):
    		string += chr(random.randint(0, 255))
        
        if string not in strings:
            otherstrings.add(string)
    
    print "[*] Strings created."
    
    ### 1) pybloom
    import pybloom
    bf1 = pybloom.BloomFilter(capacity=n, error_rate=p)
    
    ### 2) pybloomfilter
    import pybloomfilter
    bf2 = pybloomfilter.BloomFilter(n, p)
    
    ### 3) bloompy
    import bloompy
    bf3 = bloompy.BloomFilter(capacity=n, error_rate=p)
    
    # add them
    bfs = [("pybloom", bf1), ("pybloomfilter", bf2), ("bloompy", bf3)]
    for s in strings:
        for _, b in bfs:
            b.add(s)
            
    print "[*] Bloom filters to compare performance:\n %s\n\n" % bfs
    
    # add all strings
    for _, bf in bfs:
        for string in strings:
            bf.add(string)
    
    # then test for collisions
    # add all strings
    print "[*] Now testing with %d unique strings and desired error rate of %f" % (n, p)
    print "[*] Performance results: "
    for name, bf in bfs:
        collisions = 0
        starttime = time.time()
        for string in otherstrings:
            if string in bf:
                collisions += 1
        elapsed = time.time() - starttime
        error_rate = float(collisions) / float(n)
        print "%s: %f seconds with error rate = %f" % (name, elapsed, error_rate)
