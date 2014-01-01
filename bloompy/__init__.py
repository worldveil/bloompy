import mmh3 # murmur hash algorithm
import random
import math

class BloomFilter():
    """
    A set of strings or integers implemented with a bloom filter.
    
    Given an approximate idea of number of elements 
    to hold and a desired false positive probability, 
    creates a set using a bloom filter.

    Hash family is built from different salts to the 
    Murmur hash (mmh3) and uses the optimal settings for 
    number of hash functions (k) and size of bit vector (m).
    """

    SALT_SIZE = 5

    def __init__(self, capacity, error_rate):
        assert error_rate > 0 and error_rate < 1
        assert capacity > 1
        self.p = error_rate
        self.n = int(capacity)
        self.m = int(-self.n * math.log(self.p) / math.log(2)**2)
        self.k = int(math.log(2) * self.m / self.n)
        self.vector = 0

        # create salts
        self.salts = set()
        while len(self.salts) < self.k:
            salt = ""
            for j in range(BloomFilter.SALT_SIZE):
                salt += chr(random.randint(0, 255))
            self.salts.add(salt)

    def _hash(self, item):
        """
        Hashes item k times and updates bit vector.
        """
        if not isinstance(item, (basestring, int, long, float, complex)):
            raise Exception("Item is of unsupported type.")
        bloom = 0
        for salt in self.salts:
            h = mmh3.hash128(salt + str(item)) % self.m
            bloom |= (1L << h)
        return bloom

    def add(self, item):
        """
        Adds item to set.
        """
        self.vector |= self._hash(item)

    def __contains__(self, item):
        """
        Test for membership in set.
        """
        h = self._hash(item)
        return ((h & self.vector) == h)
        
    def clear(self):
        """
        Empties the set. 
        """
        self.vector = 0
        
    def __repr__(self):
        return "<BloomFilter n=%d, k=%d, m=%d, p=%f>" % (self.n, self.k, self.m, self.p)
